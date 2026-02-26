import csv
from collections.abc import Sequence
from io import StringIO

from app.models.audit_event import AuditEvent

CSV_COLUMNS = [
    "id",
    "event_time",
    "event_type",
    "workspace_id",
    "actor_type",
    "actor_id",
    "subject_type",
    "subject_id",
    "reason_code",
    "prev_hash",
    "event_hash",
]


def _reason_code(event: AuditEvent) -> str:
    reason = event.event_data.get("reason_code")
    if isinstance(reason, str):
        return reason

    legacy_reason = event.event_data.get("reason")
    if isinstance(legacy_reason, str):
        return legacy_reason

    return ""


def build_audit_csv(events: Sequence[AuditEvent]) -> str:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=CSV_COLUMNS)
    writer.writeheader()

    for event in events:
        writer.writerow(
            {
                "id": str(event.id),
                "event_time": event.event_time.isoformat(),
                "event_type": event.event_type,
                "workspace_id": str(event.workspace_id),
                "actor_type": event.actor_type,
                "actor_id": str(event.actor_id) if event.actor_id else "",
                "subject_type": event.subject_type,
                "subject_id": str(event.subject_id) if event.subject_id else "",
                "reason_code": _reason_code(event),
                "prev_hash": event.prev_hash or "",
                "event_hash": event.event_hash or "",
            }
        )

    return output.getvalue()
