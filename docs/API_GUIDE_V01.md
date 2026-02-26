# KYA API Guide (V01)

## Start Here
Interactive docs:
- OpenAPI: `/openapi.json`
- Swagger UI: `/docs`
- ReDoc: `/redoc`

Detailed ReDoc/OpenAPI navigation guide:
- `docs/OPENAPI_REDOC_V01.md`

## Authentication (MVP)
Sensitive endpoints require header:
- `X-Workspace-Id: <workspace_uuid>`

The body/query `workspace_id` must match this header.

Workspace bootstrap endpoint:
- `POST /workspaces` requires `X-Bootstrap-Token: <bootstrap_token>`
- if bootstrap token is not configured server-side, API returns `503 WORKSPACE_BOOTSTRAP_DISABLED`

## Core Endpoint Map
- Agents:
  - `POST /agents`
  - `GET /agents/{agent_id}`
  - `POST /agents/{agent_id}/revoke`
- Workspaces:
  - `POST /workspaces`
  - `GET /workspaces/{workspace_id}`
- Policies:
  - `POST /policies`
  - `POST /agents/{agent_id}/bind_policy`
- Capabilities:
  - `POST /capabilities/request`
- Verification:
  - `POST /verify`
- Audit:
  - `GET /audit/events`
  - `GET /audit/export.json`
  - `GET /audit/export.csv`
  - `GET /audit/integrity/check`

## Verify Response Contract
`POST /verify` always returns:
- `decision`: `ALLOW` or `DENY`
- `reason_code`: `null` on ALLOW, otherwise a denial reason
- `audit_event_id`: decision audit event id

## Common Reason Codes (Examples)
- `AGENT_REVOKED`
- `POLICY_NOT_BOUND`
- `CAPABILITY_INVALID`
- `CAPABILITY_EXPIRED`
- `CAPABILITY_REVOKED`
- `CAPABILITY_SCOPE_MISMATCH`
- `SIGNATURE_INVALID`
- `SPEND_LIMIT_EXCEEDED`
- `RATE_LIMIT_EXCEEDED`

## Common Error Shape
```json
{
  "detail": {
    "code": "WORKSPACE_MISMATCH",
    "message": "Workspace does not match authenticated context"
  }
}
```
