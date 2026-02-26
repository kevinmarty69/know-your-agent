import base64
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AgentCreateRequest(BaseModel):
    workspace_id: UUID = Field(description="Workspace identifier (must match X-Workspace-Id).")
    name: str = Field(min_length=1, max_length=255, description="Human readable agent name.")
    public_key: str = Field(description="Base64-encoded Ed25519 public key (32 bytes).")
    runtime_type: str | None = Field(
        default=None,
        max_length=64,
        description="Optional runtime label (e.g. codex, internal-bot).",
    )
    metadata: dict[str, object] = Field(default_factory=dict, description="Free-form metadata.")

    @field_validator("public_key")
    @classmethod
    def validate_public_key(cls, value: str) -> str:
        try:
            decoded = base64.b64decode(value, validate=True)
        except Exception as exc:  # pragma: no cover - explicit conversion to validation error
            raise ValueError("public_key must be valid base64") from exc

        if len(decoded) != 32:
            raise ValueError("public_key must decode to 32 bytes for Ed25519")

        return value


class AgentRevokeRequest(BaseModel):
    workspace_id: UUID = Field(description="Workspace identifier (must match X-Workspace-Id).")
    reason: str = Field(min_length=1, max_length=255, description="Reason for revocation.")


class AgentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    workspace_id: UUID
    name: str
    status: str
    public_key: str
    key_alg: str
    fingerprint: str
    runtime_type: str | None
    metadata: dict[str, object]
    created_at: datetime
    revoked_at: datetime | None
    revoke_reason: str | None


class AgentRevokeResponse(BaseModel):
    id: UUID
    status: str
    revoked_at: datetime
