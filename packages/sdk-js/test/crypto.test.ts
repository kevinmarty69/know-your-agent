import { describe, expect, it } from "vitest"

import {
  extractCapabilityJti,
  generateKeys,
  signAction,
  verifySignature,
} from "../src/crypto.js"
import { buildSignedRequest } from "../src/client.js"

function fakeJwt(payload: object): string {
  const header = Buffer.from(JSON.stringify({ alg: "none", typ: "JWT" })).toString("base64url")
  const body = Buffer.from(JSON.stringify(payload)).toString("base64url")
  return `${header}.${body}.sig`
}

describe("crypto helpers", () => {
  it("generateKeys returns base64 key material with valid lengths", () => {
    const keys = generateKeys()
    expect(Buffer.from(keys.publicKeyBase64, "base64")).toHaveLength(32)
    expect(Buffer.from(keys.privateKeyBase64, "base64")).toHaveLength(64)
  })

  it("signAction produces a verifiable signature", () => {
    const keys = generateKeys()
    const signed = signAction({
      agent_id: "11111111-1111-1111-1111-111111111111",
      workspace_id: "22222222-2222-2222-2222-222222222222",
      action_type: "purchase",
      target_service: "stripe_proxy",
      payload: { amount: 18, currency: "EUR", tool: "purchase" },
      capability_jti: "33333333-3333-3333-3333-333333333333",
      privateKeyBase64: keys.privateKeyBase64,
    })

    expect(signed.signatureBase64.length).toBeGreaterThan(10)
    expect(
      verifySignature(keys.publicKeyBase64, signed.signatureBase64, signed.canonicalJson),
    ).toBe(true)
  })

  it("extractCapabilityJti reads jti from token payload", () => {
    const token = fakeJwt({ jti: "my-jti" })
    expect(extractCapabilityJti(token)).toBe("my-jti")
  })

  it("buildSignedRequest signs using capability jti", () => {
    const keys = generateKeys()
    const token = fakeJwt({ jti: "cap-jti-1" })

    const request = buildSignedRequest({
      workspace_id: "22222222-2222-2222-2222-222222222222",
      agent_id: "11111111-1111-1111-1111-111111111111",
      action_type: "purchase",
      target_service: "stripe_proxy",
      payload: { amount: 18, currency: "EUR", tool: "purchase" },
      capability_token: token,
      privateKeyBase64: keys.privateKeyBase64,
    })

    expect(request.signature.length).toBeGreaterThan(10)
    expect(request.request_context).toEqual({})
  })
})
