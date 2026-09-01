from datetime import datetime
from uuid import uuid4

import pytest

from app.modules.audit_log.hash_chain import compute_audit_event_hash

pytestmark = pytest.mark.unit


def test_audit_hash_is_timezone_invariant() -> None:
    instant_utc = datetime.fromisoformat("2026-09-01T09:00:00+00:00")
    instant_paris = datetime.fromisoformat("2026-09-01T11:00:00+02:00")
    event_id = uuid4()
    workspace_id = uuid4()
    subject_id = uuid4()

    def hash_at(event_time: datetime) -> str:
        return compute_audit_event_hash(
            event_id=event_id,
            workspace_id=workspace_id,
            event_time=event_time,
            event_type="policy.created",
            actor_type="system",
            actor_id=None,
            subject_type="policy",
            subject_id=subject_id,
            event_data={},
            payload_hash=None,
            prev_hash=None,
        )

    assert hash_at(instant_utc) == hash_at(instant_paris)
