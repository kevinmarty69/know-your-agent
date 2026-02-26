import { createHash } from "node:crypto"

import nacl from "tweetnacl"

import { canonicalize } from "./canonical.js"
import type { GenerateKeysResult, SignActionInput, SignActionResult } from "./types.js"

function toBase64(bytes: Uint8Array): string {
  return Buffer.from(bytes).toString("base64")
}

function fromBase64(input: string): Uint8Array {
  try {
    return new Uint8Array(Buffer.from(input, "base64"))
  } catch {
    throw new Error("Invalid base64 input")
  }
}

function ensureLength(bytes: Uint8Array, expected: number, label: string): void {
  if (bytes.length !== expected) {
    throw new Error(`${label} must decode to ${expected} bytes`)
  }
}

export function generateKeys(): GenerateKeysResult {
  const keyPair = nacl.sign.keyPair()
  return {
    publicKeyBase64: toBase64(keyPair.publicKey),
    privateKeyBase64: toBase64(keyPair.secretKey),
  }
}

export function sha256Bytes(message: Uint8Array): Uint8Array {
  const digest = createHash("sha256").update(message).digest()
  return new Uint8Array(digest)
}

export function sha256Hex(message: Uint8Array): string {
  return Buffer.from(sha256Bytes(message)).toString("hex")
}

export function signAction(input: SignActionInput): SignActionResult {
  const envelope = {
    agent_id: input.agent_id,
    workspace_id: input.workspace_id,
    action_type: input.action_type,
    target_service: input.target_service,
    payload: input.payload,
    capability_jti: input.capability_jti,
  }

  const canonicalJson = canonicalize(envelope)
  const digest = sha256Bytes(Buffer.from(canonicalJson, "utf-8"))

  const secretKey = fromBase64(input.privateKeyBase64)
  ensureLength(secretKey, 64, "privateKeyBase64")

  const signature = nacl.sign.detached(digest, secretKey)

  return {
    signatureBase64: toBase64(signature),
    canonicalJson,
    sha256Hex: Buffer.from(digest).toString("hex"),
  }
}

export function extractCapabilityJti(capabilityToken: string): string {
  const parts = capabilityToken.split(".")
  if (parts.length < 2) {
    throw new Error("Invalid capability token format")
  }

  const payloadRaw = Buffer.from(parts[1], "base64url").toString("utf-8")
  const payload = JSON.parse(payloadRaw) as Record<string, unknown>
  const jti = payload.jti
  if (typeof jti !== "string" || !jti) {
    throw new Error("Capability token has no valid jti")
  }
  return jti
}

export function verifySignature(
  publicKeyBase64: string,
  signatureBase64: string,
  canonicalJson: string,
): boolean {
  const publicKey = fromBase64(publicKeyBase64)
  const signature = fromBase64(signatureBase64)
  const digest = sha256Bytes(Buffer.from(canonicalJson, "utf-8"))

  ensureLength(publicKey, 32, "publicKeyBase64")
  ensureLength(signature, 64, "signatureBase64")

  return nacl.sign.detached.verify(digest, signature, publicKey)
}
