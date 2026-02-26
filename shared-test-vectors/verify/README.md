# Shared Verify Vectors

These vectors lock compatibility between backend and SDK canonicalization/signature inputs.
They include ASCII and non-ASCII key scenarios.

Schema:
```json
{
  "name": "vector_name",
  "input": {
    "agent_id": "uuid",
    "workspace_id": "uuid",
    "action_type": "string",
    "target_service": "string",
    "payload": {},
    "capability_jti": "uuid"
  },
  "expected": {
    "canonical_json": "{...}",
    "sha256_hex": "...",
    "signature_encoding": "base64"
  }
}
```

Canonical key ordering rule:
- pure lexicographic ordering (`<` / `>`)
- no locale-based ordering (`localeCompare` forbidden)
