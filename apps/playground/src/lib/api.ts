import type { ApiCallInput, ApiCallResult } from "@/lib/types"

const SENSITIVE_PATH_PREFIXES = [
  "/agents",
  "/policies",
  "/capabilities",
  "/verify",
  "/audit",
  "/workspaces/",
]

function requiresWorkspaceHeader(path: string): boolean {
  return SENSITIVE_PATH_PREFIXES.some((prefix) => path.startsWith(prefix))
}

function requiresBootstrapHeader(method: "GET" | "POST", path: string): boolean {
  return method === "POST" && path === "/workspaces"
}

function safeJsonParse(rawText: string): unknown {
  if (!rawText) {
    return null
  }

  try {
    return JSON.parse(rawText) as unknown
  } catch {
    return { raw: rawText }
  }
}

export async function callApi(input: ApiCallInput): Promise<ApiCallResult> {
  const trimmedBase = input.baseUrl.replace(/\/$/, "")
  const path = input.path.startsWith("/") ? input.path : `/${input.path}`
  const url = `${trimmedBase}${path}`

  const headers: Record<string, string> = {
    Accept: "application/json",
  }

  if (input.body !== undefined) {
    headers["Content-Type"] = "application/json"
  }

  if (input.workspaceId && requiresWorkspaceHeader(path)) {
    headers["X-Workspace-Id"] = input.workspaceId
  }

  if (input.bootstrapToken && requiresBootstrapHeader(input.method, path)) {
    headers["X-Bootstrap-Token"] = input.bootstrapToken
  }

  const started = performance.now()
  const response = await fetch(url, {
    method: input.method,
    headers,
    body: input.body !== undefined ? JSON.stringify(input.body) : undefined,
  })
  const rawText = await response.text()
  const durationMs = Math.round(performance.now() - started)

  return {
    request: {
      id: crypto.randomUUID(),
      title: input.title,
      method: input.method,
      url,
      startedAt: new Date().toISOString(),
      durationMs,
      status: response.status,
      ok: response.ok,
      requestBody: input.body,
      responseBody: safeJsonParse(rawText),
    },
    rawText,
  }
}
