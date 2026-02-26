from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PolicyCreateRequest(BaseModel):
    workspace_id: UUID = Field(description="Workspace identifier (must match X-Workspace-Id).")
    name: str = Field(min_length=1, max_length=255, description="Policy name.")
    version: int = Field(ge=1, description="Policy version, unique per (workspace, name).")
    schema_version: int = Field(ge=1, default=1, description="Policy schema version.")
    policy_json: dict[str, object] = Field(description="Policy payload.")


class PolicyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    workspace_id: UUID
    name: str
    version: int
    is_active: bool
    schema_version: int
    policy_json: dict[str, object]
    created_at: datetime
