from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.models.audit_event import AuditEvent
from app.modules.audit_log.hash_chain import compute_audit_event_hash


def append_audit_event(
    db: Session,
    *,
    workspace_id: UUID,
    event_type: str,
    subject_type: str,
    subject_id: UUID,
    event_data: dict[str, object],
    actor_type: str = "system",
) -> AuditEvent:
    db.execute(
        text(
            "SELECT pg_advisory_xact_lock("
            "hashtextextended(CAST(:workspace_id AS text), 0)"
            ")"
        ),
        {"workspace_id": str(workspace_id)},
    )
    previous_hash = db.scalar(
        select(AuditEvent.event_hash)
        .where(AuditEvent.workspace_id == workspace_id)
        .order_by(AuditEvent.event_time.desc(), AuditEvent.id.desc())
        .limit(1)
    )

    event_id = uuid4()
    event_time = datetime.now(tz=UTC)
    event_hash = compute_audit_event_hash(
        event_id=event_id,
        workspace_id=workspace_id,
        event_time=event_time.isoformat(),
        event_type=event_type,
        actor_type=actor_type,
        actor_id=None,
        subject_type=subject_type,
        subject_id=subject_id,
        event_data=event_data,
        payload_hash=None,
        prev_hash=previous_hash,
    )

    event = AuditEvent(
        id=event_id,
        workspace_id=workspace_id,
        event_type=event_type,
        actor_type=actor_type,
        subject_type=subject_type,
        subject_id=subject_id,
        event_time=event_time,
        event_data=event_data,
        prev_hash=previous_hash,
        event_hash=event_hash,
    )
    db.add(event)
    db.flush()
    return event
