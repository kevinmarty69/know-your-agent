from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field

from app.core.errors import raise_http_error

DecisionValue = Literal["ALLOW", "DENY"]


class AuditEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    event_time: datetime
    event_type: str
    workspace_id: UUID
    actor_type: str
    actor_id: UUID | None
    subject_type: str
    subject_id: UUID | None
    event_data: dict[str, object]
    prev_hash: str | None
    event_hash: str | None


class AuditEventsListResponse(BaseModel):
    items: list[AuditEventResponse]
    count: int
    limit: int
    offset: int


class AuditQueryParams(BaseModel):
    workspace_id: UUID
    from_time: datetime | None = None
    to_time: datetime | None = None
    event_type: str | None = None
    subject_id: UUID | None = None
    decision: DecisionValue | None = None
    limit: int = Field(default=50, ge=1, le=200)
    offset: int = Field(default=0, ge=0)


class AuditExportQueryParams(BaseModel):
    workspace_id: UUID
    from_time: datetime | None = None
    to_time: datetime | None = None
    event_type: str | None = None
    subject_id: UUID | None = None
    decision: DecisionValue | None = None


def _validate_date_window(from_time: datetime | None, to_time: datetime | None) -> None:
    if from_time is not None and to_time is not None and from_time > to_time:
        raise_http_error(422, "VALIDATION_ERROR", "Query param 'from' must be <= 'to'")


def get_audit_query_params(
    workspace_id: Annotated[UUID, Query(description="Workspace identifier")],
    from_time: Annotated[datetime | None, Query(alias="from", description="Start datetime")] = None,
    to_time: Annotated[datetime | None, Query(alias="to", description="End datetime")] = None,
    event_type: Annotated[str | None, Query(description="Filter by event type")] = None,
    subject_id: Annotated[UUID | None, Query(description="Filter by subject id")] = None,
    decision: Annotated[DecisionValue | None, Query(description="ALLOW or DENY filter")] = None,
    limit: Annotated[int, Query(ge=1, le=200, description="Page size")]=50,
    offset: Annotated[int, Query(ge=0, description="Page offset")]=0,
) -> AuditQueryParams:
    _validate_date_window(from_time, to_time)
    return AuditQueryParams(
        workspace_id=workspace_id,
        from_time=from_time,
        to_time=to_time,
        event_type=event_type,
        subject_id=subject_id,
        decision=decision,
        limit=limit,
        offset=offset,
    )


def get_audit_export_query_params(
    workspace_id: Annotated[UUID, Query(description="Workspace identifier")],
    from_time: Annotated[datetime | None, Query(alias="from", description="Start datetime")] = None,
    to_time: Annotated[datetime | None, Query(alias="to", description="End datetime")] = None,
    event_type: Annotated[str | None, Query(description="Filter by event type")] = None,
    subject_id: Annotated[UUID | None, Query(description="Filter by subject id")] = None,
    decision: Annotated[DecisionValue | None, Query(description="ALLOW or DENY filter")] = None,
) -> AuditExportQueryParams:
    _validate_date_window(from_time, to_time)
    return AuditExportQueryParams(
        workspace_id=workspace_id,
        from_time=from_time,
        to_time=to_time,
        event_type=event_type,
        subject_id=subject_id,
        decision=decision,
    )
