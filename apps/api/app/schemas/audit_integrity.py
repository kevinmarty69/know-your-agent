from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel

from app.core.errors import raise_http_error


class AuditIntegrityQueryParams(BaseModel):
    workspace_id: UUID
    from_time: datetime | None = None
    to_time: datetime | None = None


class AuditIntegrityResponse(BaseModel):
    workspace_id: UUID
    status: Literal["OK", "BROKEN", "PARTIAL"]
    checked_count: int
    broken_at_event_id: UUID | None
    message: str


def get_audit_integrity_query_params(
    workspace_id: Annotated[UUID, Query(description="Workspace identifier")],
    from_time: Annotated[datetime | None, Query(alias="from", description="Start datetime")] = None,
    to_time: Annotated[datetime | None, Query(alias="to", description="End datetime")] = None,
) -> AuditIntegrityQueryParams:
    if from_time is not None and to_time is not None and from_time > to_time:
        raise_http_error(422, "VALIDATION_ERROR", "Query param 'from' must be <= 'to'")

    return AuditIntegrityQueryParams(
        workspace_id=workspace_id,
        from_time=from_time,
        to_time=to_time,
    )
