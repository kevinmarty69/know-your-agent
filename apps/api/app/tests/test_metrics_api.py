import base64
from hashlib import sha256
from typing import cast

from fastapi.testclient import TestClient
from nacl.signing import SigningKey

from app.modules.verify_engine.canonical_json import canonical_json_bytes


def _create_agent(client: TestClient, workspace_id: str, public_key_b64: str) -> str:
    response = client.post(
        "/agents",
        json={
            "workspace_id": workspace_id,
            "name": "agent-metrics",
            "public_key": public_key_b64,
            "metadata": {},
        },
    )
    assert response.status_code == 201
    return str(response.json()["id"])


def _create_bound_policy(client: TestClient, workspace_id: str, agent_id: str) -> None:
    policy = client.post(
        "/policies",
        json={
            "workspace_id": workspace_id,
            "name": "policy-metrics",
            "version": 1,
            "schema_version": 1,
            "policy_json": {
                "allowed_tools": ["purchase"],
                "spend": {"currency": "EUR", "max_per_tx": 50},
                "rate_limits": {"max_actions_per_min": 10},
            },
        },
    )
    assert policy.status_code == 201
    bind = client.post(
        f"/agents/{agent_id}/bind_policy",
        json={"workspace_id": workspace_id, "policy_id": policy.json()["id"]},
        headers={"X-Workspace-Id": workspace_id},
    )
    assert bind.status_code == 201


def _issue_capability(client: TestClient, workspace_id: str, agent_id: str) -> dict[str, object]:
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
    return cast(dict[str, object], response.json())


def test_metrics_exposed_and_updated(client: TestClient, workspace_id: str) -> None:
    signing_key = SigningKey.generate()
    public_key_b64 = base64.b64encode(bytes(signing_key.verify_key)).decode()
    agent_id = _create_agent(client, workspace_id, public_key_b64)
    _create_bound_policy(client, workspace_id, agent_id)
    capability = _issue_capability(client, workspace_id, agent_id)

    payload = {"amount": 18, "currency": "EUR", "tool": "purchase"}
    envelope = {
        "agent_id": agent_id,
        "workspace_id": workspace_id,
        "action_type": "purchase",
        "target_service": "stripe_proxy",
        "payload": payload,
        "capability_jti": str(capability["jti"]),
    }
    signature = base64.b64encode(
        signing_key.sign(sha256(canonical_json_bytes(envelope)).digest()).signature
    ).decode()

    verify = client.post(
        "/verify",
        json={
            "workspace_id": workspace_id,
            "agent_id": agent_id,
            "action_type": "purchase",
            "target_service": "stripe_proxy",
            "payload": payload,
            "signature": signature,
            "capability_token": capability["token"],
            "request_context": {},
        },
        headers={"X-Workspace-Id": workspace_id},
    )
    assert verify.status_code == 200

    integrity = client.get(
        f"/audit/integrity/check?workspace_id={workspace_id}",
        headers={"X-Workspace-Id": workspace_id},
    )
    assert integrity.status_code == 200

    metrics = client.get("/metrics")
    assert metrics.status_code == 200
    assert "kya_verify_total" in metrics.text
    assert "kya_verify_latency_seconds" in metrics.text
    assert "kya_audit_integrity_total" in metrics.text
    assert 'decision="ALLOW"' in metrics.text
    assert 'status="OK"' in metrics.text
