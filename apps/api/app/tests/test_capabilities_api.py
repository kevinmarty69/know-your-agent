import base64
from uuid import UUID

from fastapi.testclient import TestClient


def _public_key_from_byte(value: int) -> str:
    return base64.b64encode(bytes([value]) * 32).decode()


def _create_agent(client: TestClient, workspace_id: str, value: int) -> str:
    response = client.post(
        "/agents",
        json={
            "workspace_id": workspace_id,
            "name": f"agent-{value}",
            "public_key": _public_key_from_byte(value),
            "metadata": {},
        },
    )
    assert response.status_code == 201
    return str(response.json()["id"])


def _create_policy(client: TestClient, workspace_id: str, max_per_tx: int = 50) -> str:
    response = client.post(
        "/policies",
        json={
            "workspace_id": workspace_id,
            "name": "purchase_basic",
            "version": 1,
            "schema_version": 1,
            "policy_json": {
                "allowed_tools": ["purchase"],
                "spend": {"currency": "EUR", "max_per_tx": max_per_tx},
            },
        },
    )
    assert response.status_code == 201
    return str(response.json()["id"])


def _bind_policy(client: TestClient, workspace_id: str, agent_id: str, policy_id: str) -> None:
    response = client.post(
        f"/agents/{agent_id}/bind_policy",
        json={"workspace_id": workspace_id, "policy_id": policy_id},
        headers={"X-Workspace-Id": workspace_id},
    )
    assert response.status_code == 201


def test_issue_capability_success(client: TestClient, workspace_id: str) -> None:
    agent_id = _create_agent(client, workspace_id, 11)
    policy_id = _create_policy(client, workspace_id)
    _bind_policy(client, workspace_id, agent_id, policy_id)

    response = client.post(
        "/capabilities/request",
        json={
            "workspace_id": workspace_id,
            "agent_id": agent_id,
            "action": "purchase",
            "target_service": "stripe_proxy",
            "requested_scopes": ["purchase"],
            "requested_limits": {"amount": 18, "currency": "EUR"},
            "ttl_minutes": 15,
        },
        headers={"X-Workspace-Id": workspace_id},
    )

    assert response.status_code == 201
    payload = response.json()
    assert UUID(payload["capability_id"])
    assert payload["token"]
    assert UUID(payload["jti"])


def test_issue_capability_denied_on_revoked_agent(client: TestClient, workspace_id: str) -> None:
    agent_id = _create_agent(client, workspace_id, 12)
    policy_id = _create_policy(client, workspace_id)
    _bind_policy(client, workspace_id, agent_id, policy_id)

    revoke = client.post(
        f"/agents/{agent_id}/revoke",
        json={"workspace_id": workspace_id, "reason": "compromised"},
        headers={"X-Workspace-Id": workspace_id},
    )
    assert revoke.status_code == 200

    response = client.post(
        "/capabilities/request",
        json={
            "workspace_id": workspace_id,
            "agent_id": agent_id,
            "action": "purchase",
            "target_service": "stripe_proxy",
            "requested_scopes": ["purchase"],
            "requested_limits": {"amount": 18},
            "ttl_minutes": 15,
        },
        headers={"X-Workspace-Id": workspace_id},
    )

    assert response.status_code == 409
    assert response.json()["detail"]["code"] == "AGENT_REVOKED"


def test_issue_capability_scope_mismatch_returns_422(client: TestClient, workspace_id: str) -> None:
    agent_id = _create_agent(client, workspace_id, 13)
    policy_id = _create_policy(client, workspace_id)
    _bind_policy(client, workspace_id, agent_id, policy_id)

    response = client.post(
        "/capabilities/request",
        json={
            "workspace_id": workspace_id,
            "agent_id": agent_id,
            "action": "purchase",
            "target_service": "stripe_proxy",
            "requested_scopes": ["deploy_prod"],
            "requested_limits": {"amount": 18},
            "ttl_minutes": 15,
        },
        headers={"X-Workspace-Id": workspace_id},
    )

    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "CAPABILITY_SCOPE_MISMATCH"


def test_issue_capability_workspace_mismatch_denied(client: TestClient, workspace_id: str) -> None:
    agent_id = _create_agent(client, workspace_id, 14)
    policy_id = _create_policy(client, workspace_id)
    _bind_policy(client, workspace_id, agent_id, policy_id)

    response = client.post(
        "/capabilities/request",
        json={
            "workspace_id": workspace_id,
            "agent_id": agent_id,
            "action": "purchase",
            "target_service": "stripe_proxy",
            "requested_scopes": ["purchase"],
            "requested_limits": {"amount": 18, "currency": "EUR"},
            "ttl_minutes": 15,
        },
        headers={"X-Workspace-Id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"},
    )

    assert response.status_code == 403
    assert response.json()["detail"]["code"] == "WORKSPACE_MISMATCH"
