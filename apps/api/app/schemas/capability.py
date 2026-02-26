from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CapabilityRequest(BaseModel):
    workspace_id: UUID = Field(description="Workspace identifier (must match X-Workspace-Id).")
    agent_id: UUID
    action: str = Field(min_length=1, max_length=128, description="Requested action.")
    target_service: str = Field(min_length=1, max_length=255, description="Target service id.")
    requested_scopes: list[str] = Field(description="Requested capability scopes.")
    requested_limits: dict[str, object] = Field(
        default_factory=dict,
        description="Requested limits.",
    )
    ttl_minutes: int | None = Field(default=None, ge=5, le=30, description="Capability TTL.")


class CapabilityIssueResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    capability_id: UUID
    token: str
    jti: str
    issued_at: datetime
    expires_at: datetime
