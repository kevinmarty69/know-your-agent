import base64

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.agent_policy_binding import AgentPolicyBinding
from app.models.audit_event import AuditEvent


def _valid_public_key(raw: bytes) -> str:
    return base64.b64encode(raw).decode()


def _create_agent(client: TestClient, workspace_id: str, raw_key: bytes) -> str:
    response = client.post(
        "/agents",
        json={
            "workspace_id": workspace_id,
            "name": "agent-bind",
            "public_key": _valid_public_key(raw_key),
            "metadata": {},
        },
    )
    assert response.status_code == 201
    return str(response.json()["id"])


def _create_policy(client: TestClient, workspace_id: str, name: str, version: int) -> str:
    response = client.post(
        "/policies",
        json={
            "workspace_id": workspace_id,
            "name": name,
            "version": version,
            "schema_version": 1,
            "policy_json": {"allowed_tools": ["purchase"]},
        },
    )
    assert response.status_code == 201
    return str(response.json()["id"])


def test_bind_policy_success(client: TestClient, workspace_id: str) -> None:
    agent_id = _create_agent(client, workspace_id, b"\x02" * 32)
    policy_id = _create_policy(client, workspace_id, "purchase_basic", 1)

    response = client.post(
        f"/agents/{agent_id}/bind_policy",
        json={"workspace_id": workspace_id, "policy_id": policy_id},
        headers={"X-Workspace-Id": workspace_id},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["status"] == "active"
    assert payload["agent_id"] == agent_id
    assert payload["policy_id"] == policy_id


def test_rebind_marks_old_binding_inactive(
    client: TestClient, workspace_id: str, db_session: Session
) -> None:
    agent_id = _create_agent(client, workspace_id, b"\x03" * 32)
    first_policy_id = _create_policy(client, workspace_id, "purchase_basic", 1)
    second_policy_id = _create_policy(client, workspace_id, "purchase_basic", 2)

    first_bind = client.post(
        f"/agents/{agent_id}/bind_policy",
        json={"workspace_id": workspace_id, "policy_id": first_policy_id},
        headers={"X-Workspace-Id": workspace_id},
    )
    second_bind = client.post(
        f"/agents/{agent_id}/bind_policy",
        json={"workspace_id": workspace_id, "policy_id": second_policy_id},
        headers={"X-Workspace-Id": workspace_id},
    )

    assert first_bind.status_code == 201
    assert second_bind.status_code == 201

    bindings = db_session.scalars(
        select(AgentPolicyBinding).where(AgentPolicyBinding.agent_id == agent_id)
    ).all()

    assert len(bindings) == 2
    active_bindings = [binding for binding in bindings if binding.status == "active"]
    inactive_bindings = [binding for binding in bindings if binding.status == "inactive"]

    assert len(active_bindings) == 1
    assert str(active_bindings[0].policy_id) == second_policy_id
    assert len(inactive_bindings) == 1
    assert str(inactive_bindings[0].policy_id) == first_policy_id
    assert inactive_bindings[0].unbound_at is not None


def test_bind_policy_on_revoked_agent_returns_conflict(
    client: TestClient, workspace_id: str
) -> None:
    agent_id = _create_agent(client, workspace_id, b"\x04" * 32)
    policy_id = _create_policy(client, workspace_id, "purchase_basic", 1)

    revoke = client.post(
        f"/agents/{agent_id}/revoke",
        json={"workspace_id": workspace_id, "reason": "disabled"},
        headers={"X-Workspace-Id": workspace_id},
    )
    assert revoke.status_code == 200

    bind = client.post(
        f"/agents/{agent_id}/bind_policy",
        json={"workspace_id": workspace_id, "policy_id": policy_id},
        headers={"X-Workspace-Id": workspace_id},
    )

    assert bind.status_code == 409
    assert bind.json()["detail"]["code"] == "AGENT_REVOKED"


def test_policy_bound_event_written(
    client: TestClient, workspace_id: str, db_session: Session
) -> None:
    agent_id = _create_agent(client, workspace_id, b"\x05" * 32)
    policy_id = _create_policy(client, workspace_id, "purchase_basic", 1)

    response = client.post(
        f"/agents/{agent_id}/bind_policy",
        json={"workspace_id": workspace_id, "policy_id": policy_id},
        headers={"X-Workspace-Id": workspace_id},
    )

    assert response.status_code == 201
    event_types = db_session.scalars(select(AuditEvent.event_type)).all()
    assert "policy.bound" in event_types


def test_bind_policy_workspace_mismatch_denied(client: TestClient, workspace_id: str) -> None:
    agent_id = _create_agent(client, workspace_id, b"\x06" * 32)
    policy_id = _create_policy(client, workspace_id, "purchase_basic", 1)

    response = client.post(
        f"/agents/{agent_id}/bind_policy",
        json={"workspace_id": workspace_id, "policy_id": policy_id},
        headers={"X-Workspace-Id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"},
    )

    assert response.status_code == 403
    assert response.json()["detail"]["code"] == "WORKSPACE_MISMATCH"
