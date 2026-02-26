from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.audit_event import AuditEvent
from app.modules.audit_log.hash_chain import recompute_event_hash
from app.schemas.audit_integrity import AuditIntegrityQueryParams, AuditIntegrityResponse


def check_audit_integrity(db: Session, query: AuditIntegrityQueryParams) -> AuditIntegrityResponse:
    stmt = select(AuditEvent).where(AuditEvent.workspace_id == query.workspace_id)

    if query.from_time is not None:
        stmt = stmt.where(AuditEvent.event_time >= query.from_time)
    if query.to_time is not None:
        stmt = stmt.where(AuditEvent.event_time <= query.to_time)

    events = db.scalars(stmt.order_by(AuditEvent.event_time.asc(), AuditEvent.id.asc())).all()

    if not events:
        return AuditIntegrityResponse(
            workspace_id=query.workspace_id,
            status="OK",
            checked_count=0,
            broken_at_event_id=None,
            message="No events in selected range",
        )

    is_partial_window = query.from_time is not None and events[0].prev_hash is not None
    expected_prev_hash = events[0].prev_hash if is_partial_window else None

    for index, event in enumerate(events, start=1):
        if event.prev_hash != expected_prev_hash:
            return AuditIntegrityResponse(
                workspace_id=query.workspace_id,
                status="BROKEN",
                checked_count=index,
                broken_at_event_id=event.id,
                message="Chain mismatch",
            )

        if event.event_hash is None:
            return AuditIntegrityResponse(
                workspace_id=query.workspace_id,
                status="PARTIAL",
                checked_count=index,
                broken_at_event_id=None,
                message="Missing event_hash in selected range; full continuity not proven",
            )

        recomputed_hash = recompute_event_hash(event)
        if event.event_hash != recomputed_hash:
            return AuditIntegrityResponse(
                workspace_id=query.workspace_id,
                status="BROKEN",
                checked_count=index,
                broken_at_event_id=event.id,
                message="Chain mismatch",
            )

        expected_prev_hash = event.event_hash

    if is_partial_window:
        return AuditIntegrityResponse(
            workspace_id=query.workspace_id,
            status="PARTIAL",
            checked_count=len(events),
            broken_at_event_id=None,
            message="Window starts mid-chain; full continuity not proven",
        )

    return AuditIntegrityResponse(
        workspace_id=query.workspace_id,
        status="OK",
        checked_count=len(events),
        broken_at_event_id=None,
        message="Hash chain valid",
    )
