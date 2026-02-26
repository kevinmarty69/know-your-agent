from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class WorkspaceCreateRequest(BaseModel):
    name: str = Field(min_length=3, max_length=255, description="Human readable workspace name.")
    slug: str | None = Field(
        default=None,
        min_length=3,
        max_length=80,
        description="Optional unique slug. Lowercase letters, numbers and dashes.",
    )

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, value: str | None) -> str | None:
        if value is None:
            return None

        normalized = value.strip().lower()
        if normalized != value:
            raise ValueError("slug must be lowercase and must not have surrounding spaces")

        allowed = set("abcdefghijklmnopqrstuvwxyz0123456789-")
        if any(char not in allowed for char in value):
            raise ValueError("slug must contain only lowercase letters, numbers and dashes")

        if "--" in value or value.startswith("-") or value.endswith("-"):
            raise ValueError("slug format is invalid")

        return value


class WorkspaceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    slug: str
    status: str
    created_at: datetime
