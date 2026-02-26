import base64
from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.agent import Agent
from app.models.audit_event import AuditEvent


def _valid_public_key() -> str:
    return base64.b64encode(b"\x01" * 32).decode()


def test_create_agent_success(client: TestClient, workspace_id: str) -> None:
    response = client.post(
        "/agents",
        json={
            "workspace_id": workspace_id,
            "name": "agent-sales",
            "public_key": _valid_public_key(),
            "runtime_type": "codex",
            "metadata": {"version": "0.1.0"},
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["status"] == "active"
    assert payload["key_alg"] == "ed25519"
    assert payload["metadata"]["version"] == "0.1.0"


def test_create_agent_rejects_invalid_public_key(client: TestClient, workspace_id: str) -> None:
    response = client.post(
        "/agents",
        json={
            "workspace_id": workspace_id,
            "name": "agent-bad",
            "public_key": "not-base64",
            "metadata": {},
        },
    )

    assert response.status_code == 422


def test_get_agent_success(client: TestClient, workspace_id: str) -> None:
    create = client.post(
        "/agents",
        json={
            "workspace_id": workspace_id,
            "name": "agent-get",
            "public_key": _valid_public_key(),
            "metadata": {},
        },
    )
    agent_id = str(create.json()["id"])

    response = client.get(f"/agents/{agent_id}")

    assert response.status_code == 200
    assert response.json()["id"] == agent_id


def test_get_agent_workspace_mismatch_denied(client: TestClient, workspace_id: str) -> None:
    create = client.post(
        "/agents",
        json={
            "workspace_id": workspace_id,
            "name": "agent-get-mismatch",
            "public_key": _valid_public_key(),
            "metadata": {},
        },
    )
    agent_id = str(create.json()["id"])

    response = client.get(
        f"/agents/{agent_id}",
        headers={"X-Workspace-Id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"},
    )

    assert response.status_code == 403
    assert response.json()["detail"]["code"] == "WORKSPACE_MISMATCH"


def test_revoke_agent_success_and_double_revoke_conflict(
    client: TestClient, workspace_id: str, auth_headers: dict[str, str]
) -> None:
    create = client.post(
        "/agents",
        json={
            "workspace_id": workspace_id,
            "name": "agent-revoke",
            "public_key": _valid_public_key(),
            "metadata": {},
        },
    )
    agent_id = str(create.json()["id"])

    first_revoke = client.post(
        f"/agents/{agent_id}/revoke",
        json={"workspace_id": workspace_id, "reason": "compromised_key"},
        headers=auth_headers,
    )
    second_revoke = client.post(
        f"/agents/{agent_id}/revoke",
        json={"workspace_id": workspace_id, "reason": "already"},
        headers=auth_headers,
    )

    assert first_revoke.status_code == 200
    assert first_revoke.json()["status"] == "revoked"
    assert second_revoke.status_code == 409
    assert second_revoke.json()["detail"]["code"] == "AGENT_ALREADY_REVOKED"


def test_create_agent_duplicate_fingerprint_conflict(client: TestClient, workspace_id: str) -> None:
    payload = {
        "workspace_id": workspace_id,
        "name": "agent-1",
        "public_key": _valid_public_key(),
        "metadata": {},
    }
    first = client.post("/agents", json=payload)
    second = client.post("/agents", json={**payload, "name": "agent-2"})

    assert first.status_code == 201
    assert second.status_code == 409
    assert second.json()["detail"]["code"] == "AGENT_FINGERPRINT_ALREADY_EXISTS"


def test_agent_events_written_to_audit_log(
    client: TestClient,
    workspace_id: str,
    db_session: Session,
    auth_headers: dict[str, str],
) -> None:
    create = client.post(
        "/agents",
        json={
            "workspace_id": workspace_id,
            "name": "agent-audit",
            "public_key": _valid_public_key(),
            "metadata": {},
        },
    )
    agent_id = str(create.json()["id"])

    client.post(
        f"/agents/{agent_id}/revoke",
        json={"workspace_id": workspace_id, "reason": "rotated"},
        headers=auth_headers,
    )

    audit_types = db_session.scalars(
        select(AuditEvent.event_type).order_by(AuditEvent.event_time)
    ).all()
    assert "agent.created" in audit_types
    assert "agent.revoked" in audit_types

    agent = db_session.scalar(select(Agent).where(Agent.id == UUID(agent_id)))
    assert agent is not None
    assert agent.status == "revoked"


def test_revoke_agent_workspace_mismatch_denied(
    client: TestClient, workspace_id: str
) -> None:
    create = client.post(
        "/agents",
        json={
            "workspace_id": workspace_id,
            "name": "agent-revoke-mismatch",
            "public_key": _valid_public_key(),
            "metadata": {},
        },
    )
    agent_id = str(create.json()["id"])

    response = client.post(
        f"/agents/{agent_id}/revoke",
        json={"workspace_id": workspace_id, "reason": "compromised_key"},
        headers={"X-Workspace-Id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"},
    )

    assert response.status_code == 403
    assert response.json()["detail"]["code"] == "WORKSPACE_MISMATCH"
