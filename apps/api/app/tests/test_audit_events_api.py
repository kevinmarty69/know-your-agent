from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

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


def test_list_audit_events_paginated(
    client: TestClient, workspace_id: str, db_session: Session
) -> None:
    now = datetime.now(tz=UTC)
    subject_id = uuid4()

    _insert_audit_event(
        db_session,
        workspace_id=workspace_id,
        event_time=now - timedelta(minutes=3),
        event_type="action.verification.requested",
        subject_id=subject_id,
        event_data={"decision": "ALLOW"},
    )
    _insert_audit_event(
        db_session,
        workspace_id=workspace_id,
        event_time=now - timedelta(minutes=2),
        event_type="action.verification.denied",
        subject_id=subject_id,
        event_data={"decision": "DENY", "reason_code": "SIGNATURE_INVALID"},
    )
    _insert_audit_event(
        db_session,
        workspace_id=workspace_id,
        event_time=now - timedelta(minutes=1),
        event_type="action.verification.allowed",
        subject_id=subject_id,
        event_data={"decision": "ALLOW"},
    )

    response = client.get(f"/audit/events?workspace_id={workspace_id}&limit=2&offset=0")

    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 3
    assert payload["limit"] == 2
    assert payload["offset"] == 0
    assert len(payload["items"]) == 2


def test_list_audit_events_filters(
    client: TestClient, workspace_id: str, db_session: Session
) -> None:
    now = datetime.now(tz=UTC)
    subject_allow = uuid4()
    subject_deny = uuid4()

    _insert_audit_event(
        db_session,
        workspace_id=workspace_id,
        event_time=now - timedelta(minutes=2),
        event_type="action.verification.allowed",
        subject_id=subject_allow,
        event_data={"decision": "ALLOW"},
    )
    _insert_audit_event(
        db_session,
        workspace_id=workspace_id,
        event_time=now - timedelta(minutes=1),
        event_type="action.verification.denied",
        subject_id=subject_deny,
        event_data={"decision": "DENY", "reason_code": "RATE_LIMIT_EXCEEDED"},
    )

    deny_resp = client.get(
        f"/audit/events?workspace_id={workspace_id}&decision=DENY&event_type=action.verification.denied"
    )
    assert deny_resp.status_code == 200
    items = deny_resp.json()["items"]
    assert len(items) == 1
    assert items[0]["subject_id"] == str(subject_deny)
    assert "payload_hash" not in items[0]

    subject_resp = client.get(
        f"/audit/events?workspace_id={workspace_id}&subject_id={subject_allow}"
    )
    assert subject_resp.status_code == 200
    subject_items = subject_resp.json()["items"]
    assert len(subject_items) == 1
    assert subject_items[0]["subject_id"] == str(subject_allow)


def test_list_audit_events_invalid_date_window_returns_422(
    client: TestClient, workspace_id: str
) -> None:
    response = client.get(
        f"/audit/events?workspace_id={workspace_id}&from=2026-01-02T00:00:00Z&to=2026-01-01T00:00:00Z"
    )

    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "VALIDATION_ERROR"


def test_list_audit_events_workspace_mismatch_denied(client: TestClient, workspace_id: str) -> None:
    response = client.get(
        f"/audit/events?workspace_id={workspace_id}",
        headers={"X-Workspace-Id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"},
    )

    assert response.status_code == 403
    assert response.json()["detail"]["code"] == "WORKSPACE_MISMATCH"
