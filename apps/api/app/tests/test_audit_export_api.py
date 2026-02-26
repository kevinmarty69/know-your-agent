import csv
from datetime import UTC, datetime, timedelta
from io import StringIO
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.audit_event import AuditEvent


def _insert_audit_event(
    db_session: Session,
    *,
    workspace_id: str,
    event_time: datetime,
    event_type: str,
    subject_id: UUID,
    event_data: dict[str, object],
    payload_hash: str | None = None,
) -> None:
    db_session.add(
        AuditEvent(
            workspace_id=UUID(workspace_id),
            event_time=event_time,
            event_type=event_type,
            actor_type="system",
            actor_id=None,
            subject_type="agent",
            subject_id=subject_id,
            event_data=event_data,
            payload_hash=payload_hash,
            prev_hash=None,
            event_hash=None,
        )
    )
    db_session.commit()


def test_export_audit_json_respects_filters_and_hides_payload_hash(
    client: TestClient, workspace_id: str, db_session: Session
) -> None:
    now = datetime.now(tz=UTC)
    subject_id = uuid4()

    _insert_audit_event(
        db_session,
        workspace_id=workspace_id,
        event_time=now - timedelta(minutes=2),
        event_type="action.verification.allowed",
        subject_id=subject_id,
        event_data={"decision": "ALLOW"},
        payload_hash="sha256:internal",
    )
    _insert_audit_event(
        db_session,
        workspace_id=workspace_id,
        event_time=now - timedelta(minutes=1),
        event_type="action.verification.denied",
        subject_id=subject_id,
        event_data={"decision": "DENY", "reason_code": "SIGNATURE_INVALID"},
    )

    response = client.get(f"/audit/export.json?workspace_id={workspace_id}&decision=DENY")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["event_type"] == "action.verification.denied"
    assert "payload_hash" not in payload[0]


def test_export_audit_csv_header_and_reason_code(
    client: TestClient, workspace_id: str, db_session: Session
) -> None:
    now = datetime.now(tz=UTC)
    subject_id = uuid4()

    _insert_audit_event(
        db_session,
        workspace_id=workspace_id,
        event_time=now - timedelta(minutes=1),
        event_type="action.verification.denied",
        subject_id=subject_id,
        event_data={"decision": "DENY", "reason_code": "RATE_LIMIT_EXCEEDED"},
    )

    response = client.get(f"/audit/export.csv?workspace_id={workspace_id}&decision=DENY")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")

    reader = csv.DictReader(StringIO(response.text))
    assert reader.fieldnames == [
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

    rows = list(reader)
    assert len(rows) == 1
    assert rows[0]["reason_code"] == "RATE_LIMIT_EXCEEDED"


def test_export_audit_workspace_mismatch_denied(client: TestClient, workspace_id: str) -> None:
    response = client.get(
        f"/audit/export.json?workspace_id={workspace_id}",
        headers={"X-Workspace-Id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"},
    )

    assert response.status_code == 403
    assert response.json()["detail"]["code"] == "WORKSPACE_MISMATCH"


def test_export_audit_json_applies_max_rows_cap(
    client: TestClient,
    workspace_id: str,
    db_session: Session,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    now = datetime.now(tz=UTC)
    subject_id = uuid4()

    _insert_audit_event(
        db_session,
        workspace_id=workspace_id,
        event_time=now - timedelta(minutes=2),
        event_type="action.verification.allowed",
        subject_id=subject_id,
        event_data={"decision": "ALLOW"},
    )
    _insert_audit_event(
        db_session,
        workspace_id=workspace_id,
        event_time=now - timedelta(minutes=1),
        event_type="action.verification.denied",
        subject_id=subject_id,
        event_data={"decision": "DENY", "reason_code": "SIGNATURE_INVALID"},
    )

    monkeypatch.setattr(settings, "audit_export_max_rows", 1)
    response = client.get(f"/audit/export.json?workspace_id={workspace_id}")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
