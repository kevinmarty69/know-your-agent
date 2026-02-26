import { readFileSync, readdirSync } from "node:fs"
import path from "node:path"

import { describe, expect, it } from "vitest"

import { canonicalize } from "../src/canonical.js"
import { sha256Hex } from "../src/crypto.js"

type Vector = {
  name: string
  input: Record<string, unknown>
  expected: {
    canonical_json: string
    sha256_hex: string
    signature_encoding: string
  }
}

function loadVectors(): Vector[] {
  const vectorsDir = path.resolve(__dirname, "../../../shared-test-vectors/verify")
  return readdirSync(vectorsDir)
    .filter((name) => name.endsWith(".json"))
    .sort()
    .map((name) => {
      const raw = readFileSync(path.join(vectorsDir, name), "utf-8")
      return JSON.parse(raw) as Vector
    })
}

describe("shared verify vectors", () => {
  const vectors = loadVectors()

  it("loads at least one vector", () => {
    expect(vectors.length).toBeGreaterThan(0)
  })

  for (const vector of vectors) {
    it(`matches canonical+hash for ${vector.name}`, () => {
      const canonical = canonicalize(vector.input)
      const digestHex = sha256Hex(Buffer.from(canonical, "utf-8"))

      expect(canonical).toBe(vector.expected.canonical_json)
      expect(digestHex).toBe(vector.expected.sha256_hex)
      expect(vector.expected.signature_encoding).toBe("base64")
    })
  }

  it("uses deterministic lexicographic key ordering (including non-ASCII)", () => {
    const canonical = canonicalize({
      é: 1,
      z: 2,
      a: 3,
      ä: 4,
    })
    expect(canonical).toBe("{\"a\":3,\"z\":2,\"ä\":4,\"é\":1}")
  })
})
