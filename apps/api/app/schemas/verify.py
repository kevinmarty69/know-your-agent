from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class VerifyRequest(BaseModel):
    workspace_id: UUID = Field(description="Workspace identifier (must match X-Workspace-Id).")
    agent_id: UUID
    action_type: str = Field(min_length=1, max_length=128)
    target_service: str = Field(min_length=1, max_length=255)
    payload: dict[str, object]
    signature: str = Field(description="Base64-encoded Ed25519 signature.")
    capability_token: str = Field(description="JWT capability token.")
    request_context: dict[str, object] = Field(default_factory=dict)


class VerifyResponse(BaseModel):
    decision: Literal["ALLOW", "DENY"]
    reason_code: str | None = Field(
        default=None,
        description="Reason code when decision is DENY, otherwise null.",
    )
    audit_event_id: UUID
