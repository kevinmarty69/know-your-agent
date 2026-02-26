from hashlib import sha256
from typing import Any
from uuid import UUID

from app.models.audit_event import AuditEvent
from app.modules.verify_engine.canonical_json import canonical_json_bytes


def compute_audit_event_hash(
    *,
    event_id: UUID,
    workspace_id: UUID,
    event_time: str,
    event_type: str,
    actor_type: str,
    actor_id: UUID | None,
    subject_type: str,
    subject_id: UUID | None,
    event_data: dict[str, object],
    payload_hash: str | None,
    prev_hash: str | None,
) -> str:
    payload: dict[str, Any] = {
        "id": str(event_id),
        "workspace_id": str(workspace_id),
        "event_time": event_time,
        "event_type": event_type,
        "actor_type": actor_type,
        "actor_id": str(actor_id) if actor_id else None,
        "subject_type": subject_type,
        "subject_id": str(subject_id) if subject_id else None,
        "event_data": event_data,
        "payload_hash": payload_hash,
        "prev_hash": prev_hash,
    }
    digest = sha256(canonical_json_bytes(payload)).hexdigest()
    return f"sha256:{digest}"


def recompute_event_hash(event: AuditEvent) -> str:
    return compute_audit_event_hash(
        event_id=event.id,
        workspace_id=event.workspace_id,
        event_time=event.event_time.isoformat(),
        event_type=event.event_type,
        actor_type=event.actor_type,
        actor_id=event.actor_id,
        subject_type=event.subject_type,
        subject_id=event.subject_id,
        event_data=event.event_data,
        payload_hash=event.payload_hash,
        prev_hash=event.prev_hash,
    )
