import { useMemo, useState } from "react"

import { callApi } from "@/lib/api"
import { parseJsonInput, prettyJson } from "@/lib/json"
import { generateDevKeypair, signVerifyPayload } from "@/lib/signing"
import type { ApiCallInput, PlaygroundRequest } from "@/lib/types"

const DEFAULT_PUBLIC_KEY = "AQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQE="
const DEFAULT_VERIFY_PAYLOAD = { amount: 18, currency: "EUR", tool: "purchase" }

type RequestInput = Pick<ApiCallInput, "title" | "method" | "path" | "body">
type RequestSuccess = (data: Record<string, unknown>) => void

function errorMessage(error: unknown, fallback: string): string {
  return error instanceof Error ? error.message : fallback
}

export function usePlayground() {
  const [baseUrl, setBaseUrl] = useState(
    import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
  )
  const [bootstrapToken, setBootstrapToken] = useState(
    import.meta.env.VITE_BOOTSTRAP_TOKEN || "",
  )
  const [workspaceId, setWorkspaceId] = useState<string>(() => crypto.randomUUID())
  const [workspaceKey, setWorkspaceKey] = useState("")
  const [workspaceName, setWorkspaceName] = useState("Playground Workspace")
  const [workspaceSlug, setWorkspaceSlug] = useState("")
  const [workspaceLookupId, setWorkspaceLookupId] = useState("")

  const [agentId, setAgentId] = useState("")
  const [agentName, setAgentName] = useState("agent-playground")
  const [publicKey, setPublicKey] = useState(DEFAULT_PUBLIC_KEY)
  const [devPrivateKey, setDevPrivateKey] = useState<CryptoKey | null>(null)

  const [policyId, setPolicyId] = useState("")
  const [policyName, setPolicyName] = useState("purchase_playground")
  const [policyVersion, setPolicyVersion] = useState("1")
  const [policyJson, setPolicyJson] = useState(() =>
    prettyJson({
      allowed_tools: ["purchase"],
      spend: { currency: "EUR", max_per_tx: 50 },
      rate_limits: { max_actions_per_min: 10 },
    }),
  )

  const [capabilityToken, setCapabilityToken] = useState("")
  const [capabilityAction, setCapabilityAction] = useState("purchase")
  const [capabilityTarget, setCapabilityTarget] = useState("stripe_proxy")
  const [capabilityScopes, setCapabilityScopes] = useState(() => prettyJson(["purchase"]))
  const [capabilityLimits, setCapabilityLimits] = useState(() =>
    prettyJson({ amount: 18, currency: "EUR" }),
  )
  const [ttlMinutes, setTtlMinutes] = useState("15")

  const [verifyAction, setVerifyAction] = useState("purchase")
  const [verifyTarget, setVerifyTarget] = useState("stripe_proxy")
  const [verifyPayload, setVerifyPayload] = useState(() => prettyJson(DEFAULT_VERIFY_PAYLOAD))
  const [verifySignature, setVerifySignature] = useState("")

  const [auditMode, setAuditMode] = useState<"events" | "export-json" | "export-csv">(
    "events",
  )
  const [decisionFilter, setDecisionFilter] = useState<"ALL" | "ALLOW" | "DENY">("ALL")

  const [history, setHistory] = useState<PlaygroundRequest[]>([])
  const [selectedRequestId, setSelectedRequestId] = useState<string | null>(null)
  const [errorText, setErrorText] = useState("")

  const selectedRequest = useMemo(
    () => history.find((item) => item.id === selectedRequestId) ?? history[0] ?? null,
    [history, selectedRequestId],
  )

  async function runRequest(createInput: () => RequestInput, onSuccess?: RequestSuccess) {
    setErrorText("")
    try {
      const input = createInput()
      const { request } = await callApi({
        ...input,
        baseUrl,
        workspaceId,
        workspaceKey,
        bootstrapToken,
      })
      setHistory((previous) => [request, ...previous].slice(0, 20))
      setSelectedRequestId(request.id)

      if (request.ok && onSuccess) {
        onSuccess(request.responseBody as Record<string, unknown>)
      }
    } catch (error) {
      setErrorText(errorMessage(error, "Unknown error"))
    }
  }

  function syncWorkspace(data: Record<string, unknown>) {
    if (!data?.id) return
    const nextWorkspaceId = String(data.id)
    setWorkspaceId(nextWorkspaceId)
    setWorkspaceLookupId(nextWorkspaceId)
    if (typeof data.api_key === "string") setWorkspaceKey(data.api_key)
  }

  const actions = {
    createWorkspace: () =>
      runRequest(
        () => ({
          title: "Create Workspace",
          method: "POST",
          path: "/workspaces",
          body: {
            name: workspaceName,
            ...(workspaceSlug.trim() ? { slug: workspaceSlug.trim() } : {}),
          },
        }),
        syncWorkspace,
      ),
    getWorkspace: () =>
      runRequest(
        () => ({
          title: "Get Workspace",
          method: "GET",
          path: `/workspaces/${workspaceLookupId}`,
        }),
        syncWorkspace,
      ),
    createAgent: () =>
      runRequest(
        () => ({
          title: "Create Agent",
          method: "POST",
          path: "/agents",
          body: {
            workspace_id: workspaceId,
            name: agentName,
            public_key: publicKey,
            metadata: {},
          },
        }),
        (data) => {
          if (data?.id) setAgentId(String(data.id))
        },
      ),
    getAgent: () =>
      runRequest(() => ({
        title: "Get Agent",
        method: "GET",
        path: `/agents/${agentId}`,
      })),
    revokeAgent: () =>
      runRequest(() => ({
        title: "Revoke Agent",
        method: "POST",
        path: `/agents/${agentId}/revoke`,
        body: { workspace_id: workspaceId, reason: "playground_revoke" },
      })),
    createPolicy: () =>
      runRequest(
        () => ({
          title: "Create Policy",
          method: "POST",
          path: "/policies",
          body: {
            workspace_id: workspaceId,
            name: policyName,
            version: Number(policyVersion),
            schema_version: 1,
            policy_json: parseJsonInput(policyJson),
          },
        }),
        (data) => {
          if (data?.id) setPolicyId(String(data.id))
        },
      ),
    bindPolicy: () =>
      runRequest(() => ({
        title: "Bind Policy",
        method: "POST",
        path: `/agents/${agentId}/bind_policy`,
        body: { workspace_id: workspaceId, policy_id: policyId },
      })),
    requestCapability: () =>
      runRequest(
        () => ({
          title: "Request Capability",
          method: "POST",
          path: "/capabilities/request",
          body: {
            workspace_id: workspaceId,
            agent_id: agentId,
            action: capabilityAction,
            target_service: capabilityTarget,
            requested_scopes: parseJsonInput(capabilityScopes),
            requested_limits: parseJsonInput(capabilityLimits),
            ttl_minutes: Number(ttlMinutes),
          },
        }),
        (data) => {
          if (data?.token) setCapabilityToken(String(data.token))
        },
      ),
    generateDevKeypair: async () => {
      setErrorText("")
      try {
        const keyPair = await generateDevKeypair()
        setPublicKey(keyPair.publicKey)
        setDevPrivateKey(keyPair.privateKey)
        setVerifySignature("")
      } catch (error) {
        setErrorText(errorMessage(error, "Failed to generate keypair"))
      }
    },
    setAllowPreset: () => setVerifyPayload(prettyJson(DEFAULT_VERIFY_PAYLOAD)),
    setDenySpendPreset: () =>
      setVerifyPayload(prettyJson({ amount: 999, currency: "EUR", tool: "purchase" })),
    signVerifyRequest: async () => {
      setErrorText("")
      try {
        setVerifySignature(
          await signVerifyPayload({
            privateKey: devPrivateKey,
            agentId,
            workspaceId,
            action: verifyAction,
            target: verifyTarget,
            payloadText: verifyPayload,
            capabilityToken,
          }),
        )
      } catch (error) {
        setErrorText(errorMessage(error, "Failed to sign verify request"))
      }
    },
    verifyAction: () =>
      runRequest(() => ({
        title: "Verify Action",
        method: "POST",
        path: "/verify",
        body: {
          workspace_id: workspaceId,
          agent_id: agentId,
          action_type: verifyAction,
          target_service: verifyTarget,
          payload: parseJsonInput(verifyPayload),
          signature: verifySignature,
          capability_token: capabilityToken,
          request_context: {},
        },
      })),
    runAuditQuery: () =>
      runRequest(() => {
        const basePath =
          auditMode === "events"
            ? "/audit/events"
            : auditMode === "export-json"
              ? "/audit/export.json"
              : "/audit/export.csv"
        const search = new URLSearchParams({ workspace_id: workspaceId })
        if (decisionFilter !== "ALL") search.set("decision", decisionFilter)

        return {
          title: `Audit ${auditMode}`,
          method: "GET",
          path: `${basePath}?${search.toString()}`,
        }
      }),
    checkAuditIntegrity: () =>
      runRequest(() => ({
        title: "Audit Integrity",
        method: "GET",
        path: `/audit/integrity/check?workspace_id=${workspaceId}`,
      })),
    readMetrics: () =>
      runRequest(() => ({ title: "Metrics", method: "GET", path: "/metrics" })),
  }

  return {
    connection: {
      baseUrl,
      setBaseUrl,
      bootstrapToken,
      setBootstrapToken,
      workspaceId,
      setWorkspaceId,
      workspaceKey,
      setWorkspaceKey,
    },
    workspace: {
      name: workspaceName,
      setName: setWorkspaceName,
      slug: workspaceSlug,
      setSlug: setWorkspaceSlug,
      lookupId: workspaceLookupId,
      setLookupId: setWorkspaceLookupId,
    },
    agent: {
      id: agentId,
      setId: setAgentId,
      name: agentName,
      setName: setAgentName,
      publicKey,
      setPublicKey,
    },
    policy: {
      id: policyId,
      setId: setPolicyId,
      name: policyName,
      setName: setPolicyName,
      version: policyVersion,
      setVersion: setPolicyVersion,
      json: policyJson,
      setJson: setPolicyJson,
    },
    capability: {
      token: capabilityToken,
      setToken: setCapabilityToken,
      action: capabilityAction,
      setAction: setCapabilityAction,
      target: capabilityTarget,
      setTarget: setCapabilityTarget,
      scopes: capabilityScopes,
      setScopes: setCapabilityScopes,
      limits: capabilityLimits,
      setLimits: setCapabilityLimits,
      ttlMinutes,
      setTtlMinutes,
    },
    verification: {
      action: verifyAction,
      setAction: setVerifyAction,
      target: verifyTarget,
      setTarget: setVerifyTarget,
      payload: verifyPayload,
      setPayload: setVerifyPayload,
      signature: verifySignature,
      setSignature: setVerifySignature,
      hasDevKey: Boolean(devPrivateKey),
    },
    audit: { mode: auditMode, setMode: setAuditMode, decisionFilter, setDecisionFilter },
    requests: { history, selectedRequest, setSelectedRequestId },
    errorText,
    actions,
  }
}

export type PlaygroundController = ReturnType<typeof usePlayground>

