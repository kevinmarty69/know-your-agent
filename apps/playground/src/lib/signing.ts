import { parseJsonInput } from "@/lib/json"

const encoder = new TextEncoder()

function sortJsonValue(value: unknown): unknown {
  if (Array.isArray(value)) {
    return value.map(sortJsonValue)
  }

  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value as Record<string, unknown>)
        .sort(([left], [right]) => (left < right ? -1 : left > right ? 1 : 0))
        .map(([key, item]) => [key, sortJsonValue(item)]),
    )
  }

  return value
}

function toBase64(bytes: Uint8Array): string {
  let binary = ""
  for (const byte of bytes) {
    binary += String.fromCharCode(byte)
  }
  return btoa(binary)
}

function extractJtiFromToken(token: string): string | null {
  const parts = token.split(".")
  if (parts.length < 2) {
    return null
  }

  try {
    const normalized = parts[1].replace(/-/g, "+").replace(/_/g, "/")
    const padding = normalized.length % 4 === 0 ? "" : "=".repeat(4 - (normalized.length % 4))
    const payload = JSON.parse(atob(normalized + padding)) as Record<string, unknown>
    return typeof payload.jti === "string" ? payload.jti : null
  } catch {
    return null
  }
}

export async function generateDevKeypair(): Promise<{
  privateKey: CryptoKey
  publicKey: string
}> {
  const keyPair = await crypto.subtle.generateKey(
    { name: "Ed25519" },
    true,
    ["sign", "verify"],
  )
  const publicRaw = await crypto.subtle.exportKey("raw", keyPair.publicKey)

  return {
    privateKey: keyPair.privateKey,
    publicKey: toBase64(new Uint8Array(publicRaw)),
  }
}

export async function signVerifyPayload(input: {
  privateKey: CryptoKey | null
  agentId: string
  workspaceId: string
  action: string
  target: string
  payloadText: string
  capabilityToken: string
}): Promise<string> {
  if (!input.privateKey) {
    throw new Error("Generate a dev keypair first")
  }
  if (!input.agentId.trim()) {
    throw new Error("Missing agent id")
  }
  if (!input.workspaceId.trim()) {
    throw new Error("Missing workspace id")
  }
  if (!input.capabilityToken.trim()) {
    throw new Error("Missing capability token")
  }

  const payload = parseJsonInput(input.payloadText)
  if (!payload || typeof payload !== "object" || Array.isArray(payload)) {
    throw new Error("Verify payload must be a JSON object")
  }

  const capabilityJti = extractJtiFromToken(input.capabilityToken)
  if (!capabilityJti) {
    throw new Error("Cannot extract capability jti from token")
  }

  const canonical = JSON.stringify(
    sortJsonValue({
      agent_id: input.agentId,
      workspace_id: input.workspaceId,
      action_type: input.action,
      target_service: input.target,
      payload,
      capability_jti: capabilityJti,
    }),
  )
  const digest = await crypto.subtle.digest("SHA-256", encoder.encode(canonical))
  const signature = await crypto.subtle.sign("Ed25519", input.privateKey, digest)

  return toBase64(new Uint8Array(signature))
}
