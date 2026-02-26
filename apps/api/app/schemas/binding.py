from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PolicyBindRequest(BaseModel):
    workspace_id: UUID = Field(description="Workspace identifier (must match X-Workspace-Id).")
    policy_id: UUID = Field(description="Policy id to bind.")


class PolicyBindingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    workspace_id: UUID
    agent_id: UUID
    policy_id: UUID
    status: str
    bound_at: datetime
    unbound_at: datetime | None
