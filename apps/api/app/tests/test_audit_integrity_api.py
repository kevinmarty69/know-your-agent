from uuid import UUID, uuid4

from fastapi.testclient import TestClient
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.models.audit_event import AuditEvent
from app.models.workspace import Workspace
from app.modules.audit_log.service import append_audit_event


def _write_event(
    db_session: Session,
    *,
    workspace_id: str,
    event_type: str,
    event_data: dict[str, object],
) -> str:
    event = append_audit_event(
        db_session,
        workspace_id=UUID(workspace_id),
        event_type=event_type,
        subject_type="agent",
        subject_id=uuid4(),
        event_data=event_data,
    )
    db_session.commit()
    return str(event.id)


def test_audit_chain_fields_are_set(db_session: Session, workspace_id: str) -> None:
    _write_event(
        db_session,
        workspace_id=workspace_id,
        event_type="action.verification.requested",
        event_data={"decision": "ALLOW"},
    )
    _write_event(
        db_session,
        workspace_id=workspace_id,
        event_type="action.verification.allowed",
        event_data={"decision": "ALLOW"},
    )

    events = db_session.scalars(
        select(AuditEvent)
        .where(AuditEvent.workspace_id == UUID(workspace_id))
        .order_by(AuditEvent.event_time.asc(), AuditEvent.id.asc())
    ).all()
    assert len(events) == 2
    assert events[0].prev_hash is None
    assert events[0].event_hash is not None
    assert events[1].prev_hash == events[0].event_hash
    assert events[1].event_hash is not None


def test_audit_chain_isolated_between_workspaces(db_session: Session, workspace_id: str) -> None:
    _write_event(
        db_session,
        workspace_id=workspace_id,
        event_type="agent.created",
        event_data={},
    )

    second_workspace = Workspace(
        name="Second Workspace",
        slug=f"workspace-{uuid4().hex[:8]}",
        status="active",
    )
    db_session.add(second_workspace)
    db_session.commit()

    _write_event(
        db_session,
        workspace_id=str(second_workspace.id),
        event_type="agent.created",
        event_data={},
    )

    rows = db_session.execute(
        text(
            """
        SELECT workspace_id::text, prev_hash
        FROM audit_events
        ORDER BY event_time ASC, id ASC
        """
        )
    ).all()

    first_workspace_prev_hashes = [prev for ws, prev in rows if ws == workspace_id]
    second_workspace_prev_hashes = [prev for ws, prev in rows if ws == str(second_workspace.id)]

    assert first_workspace_prev_hashes[0] is None
    assert second_workspace_prev_hashes[0] is None


def test_audit_integrity_check_ok(
    client: TestClient, db_session: Session, workspace_id: str
) -> None:
    _write_event(
        db_session,
        workspace_id=workspace_id,
        event_type="policy.created",
        event_data={},
    )
    _write_event(
        db_session,
        workspace_id=workspace_id,
        event_type="policy.bound",
        event_data={},
    )

    response = client.get(f"/audit/integrity/check?workspace_id={workspace_id}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "OK"
    assert payload["broken_at_event_id"] is None
    assert payload["checked_count"] == 2


def test_audit_integrity_check_broken_after_tamper(
    client: TestClient,
    db_session: Session,
    workspace_id: str,
) -> None:
    event_id = _write_event(
        db_session,
        workspace_id=workspace_id,
        event_type="action.verification.denied",
        event_data={"decision": "DENY", "reason_code": "SIGNATURE_INVALID"},
    )
    _write_event(
        db_session,
        workspace_id=workspace_id,
        event_type="action.verification.requested",
        event_data={"decision": "ALLOW"},
    )

    db_session.execute(
        text(
            """
        UPDATE audit_events
        SET event_data = '{"decision": "DENY", "reason_code": "TAMPERED"}'::jsonb
        WHERE id = CAST(:event_id AS uuid)
        """
        ),
        {"event_id": event_id},
    )
    db_session.commit()

    response = client.get(f"/audit/integrity/check?workspace_id={workspace_id}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "BROKEN"
    assert payload["broken_at_event_id"] == event_id


def test_audit_integrity_check_partial_on_mid_window(
    client: TestClient,
    db_session: Session,
    workspace_id: str,
) -> None:
    _write_event(
        db_session,
        workspace_id=workspace_id,
        event_type="policy.created",
        event_data={},
    )
    second_event_id = _write_event(
        db_session,
        workspace_id=workspace_id,
        event_type="policy.bound",
        event_data={},
    )

    second_event = db_session.scalar(
        select(AuditEvent).where(AuditEvent.id == UUID(second_event_id))
    )
    assert second_event is not None
    window_from = second_event.event_time.isoformat()
    response = client.get(
        "/audit/integrity/check",
        params={"workspace_id": workspace_id, "from": window_from},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "PARTIAL"
    assert payload["broken_at_event_id"] is None


def test_audit_integrity_workspace_mismatch_denied(client: TestClient, workspace_id: str) -> None:
    response = client.get(
        f"/audit/integrity/check?workspace_id={workspace_id}",
        headers={"X-Workspace-Id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"},
    )

    assert response.status_code == 403
    assert response.json()["detail"]["code"] == "WORKSPACE_MISMATCH"


def test_audit_integrity_partial_when_event_hash_missing(
    client: TestClient,
    db_session: Session,
    workspace_id: str,
) -> None:
    event_id = _write_event(
        db_session,
        workspace_id=workspace_id,
        event_type="agent.created",
        event_data={},
    )
    db_session.execute(
        text(
            """
        UPDATE audit_events
        SET event_hash = NULL
        WHERE id = CAST(:event_id AS uuid)
        """
        ),
        {"event_id": event_id},
    )
    db_session.commit()

    response = client.get(f"/audit/integrity/check?workspace_id={workspace_id}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "PARTIAL"
    assert payload["broken_at_event_id"] is None


def test_audit_integrity_invalid_date_window_returns_422(
    client: TestClient, workspace_id: str
) -> None:
    response = client.get(
        f"/audit/integrity/check?workspace_id={workspace_id}&from=2026-01-02T00:00:00Z&to=2026-01-01T00:00:00Z"
    )

    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "VALIDATION_ERROR"
