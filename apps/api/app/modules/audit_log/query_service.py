from collections.abc import Sequence

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.audit_event import AuditEvent
from app.schemas.audit import AuditExportQueryParams, AuditQueryParams


def _apply_filters(
    stmt: Select[tuple[AuditEvent]],
    query: AuditQueryParams | AuditExportQueryParams,
) -> Select[tuple[AuditEvent]]:
    stmt = stmt.where(AuditEvent.workspace_id == query.workspace_id)

    if query.from_time is not None:
        stmt = stmt.where(AuditEvent.event_time >= query.from_time)
    if query.to_time is not None:
        stmt = stmt.where(AuditEvent.event_time <= query.to_time)
    if query.event_type is not None:
        stmt = stmt.where(AuditEvent.event_type == query.event_type)
    if query.subject_id is not None:
        stmt = stmt.where(AuditEvent.subject_id == query.subject_id)
    if query.decision is not None:
        stmt = stmt.where(
            func.jsonb_extract_path_text(AuditEvent.event_data, "decision") == query.decision
        )

    return stmt


def list_audit_events(db: Session, query: AuditQueryParams) -> tuple[Sequence[AuditEvent], int]:
    filtered_stmt = _apply_filters(select(AuditEvent), query)

    count_stmt = select(func.count()).select_from(filtered_stmt.subquery())
    total_count = db.scalar(count_stmt) or 0

    rows = db.scalars(
        filtered_stmt.order_by(AuditEvent.event_time.desc(), AuditEvent.id.desc())
        .limit(query.limit)
        .offset(query.offset)
    ).all()

    return rows, int(total_count)


def list_audit_events_for_export(
    db: Session, query: AuditExportQueryParams
) -> Sequence[AuditEvent]:
    filtered_stmt = _apply_filters(select(AuditEvent), query)
    return db.scalars(
        filtered_stmt.order_by(AuditEvent.event_time.desc(), AuditEvent.id.desc()).limit(
            settings.audit_export_max_rows
        )
    ).all()
