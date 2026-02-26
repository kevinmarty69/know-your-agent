import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.core.auth import AuthContext, ensure_workspace_match, get_auth_context
from app.core.openapi import COMMON_ERROR_RESPONSES
from app.db.session import get_db
from app.modules.audit_log.export_service import build_audit_csv
from app.modules.audit_log.integrity_service import check_audit_integrity
from app.modules.audit_log.query_service import list_audit_events, list_audit_events_for_export
from app.observability.metrics import observe_audit_integrity
from app.schemas.audit import (
    AuditEventResponse,
    AuditEventsListResponse,
    AuditExportQueryParams,
    AuditQueryParams,
    get_audit_export_query_params,
    get_audit_query_params,
)
from app.schemas.audit_integrity import (
    AuditIntegrityQueryParams,
    AuditIntegrityResponse,
    get_audit_integrity_query_params,
)

router = APIRouter(tags=["audit"])
DbSession = Annotated[Session, Depends(get_db)]
Auth = Annotated[AuthContext, Depends(get_auth_context)]
AuditQuery = Annotated[AuditQueryParams, Depends(get_audit_query_params)]
AuditExportQuery = Annotated[AuditExportQueryParams, Depends(get_audit_export_query_params)]
AuditIntegrityQuery = Annotated[
    AuditIntegrityQueryParams, Depends(get_audit_integrity_query_params)
]
logger = logging.getLogger("kya.audit")


@router.get(
    "/audit/events",
    response_model=AuditEventsListResponse,
    summary="List Audit Events",
    description="Returns paginated audit events with optional filters.",
    responses=COMMON_ERROR_RESPONSES,
)
def list_audit_events_endpoint(
    query: AuditQuery,
    auth: Auth,
    db: DbSession,
) -> AuditEventsListResponse:
    ensure_workspace_match(auth.workspace_id, query.workspace_id)
    events, count = list_audit_events(db, query)
    return AuditEventsListResponse(
        items=[AuditEventResponse.model_validate(event) for event in events],
        count=count,
        limit=query.limit,
        offset=query.offset,
    )


@router.get(
    "/audit/export.json",
    response_model=list[AuditEventResponse],
    summary="Export Audit Events (JSON)",
    description="Exports filtered audit events as JSON.",
    responses=COMMON_ERROR_RESPONSES,
)
def export_audit_json_endpoint(
    query: AuditExportQuery,
    auth: Auth,
    db: DbSession,
) -> list[AuditEventResponse]:
    ensure_workspace_match(auth.workspace_id, query.workspace_id)
    events = list_audit_events_for_export(db, query)
    return [AuditEventResponse.model_validate(event) for event in events]


@router.get(
    "/audit/export.csv",
    summary="Export Audit Events (CSV)",
    description="Exports filtered audit events as CSV.",
    responses=COMMON_ERROR_RESPONSES,
)
def export_audit_csv_endpoint(
    query: AuditExportQuery,
    auth: Auth,
    db: DbSession,
) -> Response:
    ensure_workspace_match(auth.workspace_id, query.workspace_id)
    events = list_audit_events_for_export(db, query)
    content = build_audit_csv(events)
    return Response(content=content, media_type="text/csv")


@router.get(
    "/audit/integrity/check",
    response_model=AuditIntegrityResponse,
    summary="Check Audit Chain Integrity",
    description=(
        "Verifies hash-chain continuity in a workspace. Returns OK, BROKEN or PARTIAL."
    ),
    responses=COMMON_ERROR_RESPONSES,
)
def check_audit_integrity_endpoint(
    query: AuditIntegrityQuery,
    auth: Auth,
    db: DbSession,
) -> AuditIntegrityResponse:
    ensure_workspace_match(auth.workspace_id, query.workspace_id)
    result = check_audit_integrity(db, query)
    observe_audit_integrity(result.status)
    logger.info(
        "audit_integrity_checked",
        extra={
            "event_name": "audit_integrity_checked",
            "workspace_id": str(query.workspace_id),
            "status": result.status,
            "checked_count": result.checked_count,
            "broken_at_event_id": (
                str(result.broken_at_event_id) if result.broken_at_event_id else None
            ),
            "path": "/audit/integrity/check",
            "method": "GET",
        },
    )
    return result
