import base64
from hashlib import sha256
from typing import cast

from fastapi.testclient import TestClient
from nacl.signing import SigningKey

from app.modules.verify_engine.canonical_json import canonical_json_bytes


def _generate_agent_keypair() -> tuple[str, SigningKey]:
    signing_key = SigningKey.generate()
    verify_key = signing_key.verify_key
    public_key_b64 = base64.b64encode(bytes(verify_key)).decode()
    return public_key_b64, signing_key


def _create_agent(client: TestClient, workspace_id: str, public_key_b64: str) -> str:
    response = client.post(
        "/agents",
        headers={"X-Workspace-Id": workspace_id},
        json={
            "workspace_id": workspace_id,
            "name": "agent-e2e",
            "public_key": public_key_b64,
            "metadata": {},
        },
    )
    assert response.status_code == 201
    return str(response.json()["id"])


def _create_policy(client: TestClient, workspace_id: str) -> str:
    response = client.post(
        "/policies",
        headers={"X-Workspace-Id": workspace_id},
        json={
            "workspace_id": workspace_id,
            "name": "purchase_e2e",
            "version": 1,
            "schema_version": 1,
            "policy_json": {
                "allowed_tools": ["purchase"],
                "spend": {"currency": "EUR", "max_per_tx": 100},
                "rate_limits": {"max_actions_per_min": 10},
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


def _sign_verify_request(
    *,
    signing_key: SigningKey,
    workspace_id: str,
    agent_id: str,
    action_type: str,
    target_service: str,
    payload: dict[str, object],
    capability_jti: str,
) -> str:
    envelope = {
        "agent_id": agent_id,
        "workspace_id": workspace_id,
        "action_type": action_type,
        "target_service": target_service,
        "payload": payload,
        "capability_jti": capability_jti,
    }
    digest = sha256(canonical_json_bytes(envelope)).digest()
    signature = signing_key.sign(digest).signature
    return base64.b64encode(signature).decode()


def test_e2e_reference_flow(client: TestClient, workspace_id: str) -> None:
    public_key_b64, signing_key = _generate_agent_keypair()
    agent_id = _create_agent(client, workspace_id, public_key_b64)
    policy_id = _create_policy(client, workspace_id)
    _bind_policy(client, workspace_id, agent_id, policy_id)
    capability = _issue_capability(client, workspace_id, agent_id)

    payload = {"amount": 18, "currency": "EUR", "tool": "purchase"}
    signature = _sign_verify_request(
        signing_key=signing_key,
        workspace_id=workspace_id,
        agent_id=agent_id,
        action_type="purchase",
        target_service="stripe_proxy",
        payload=payload,
        capability_jti=str(capability["jti"]),
    )

    verify_allow = client.post(
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
    assert verify_allow.status_code == 200
    assert verify_allow.json()["decision"] == "ALLOW"

    revoke = client.post(
        f"/agents/{agent_id}/revoke",
        json={"workspace_id": workspace_id, "reason": "compromised_key"},
        headers={"X-Workspace-Id": workspace_id},
    )
    assert revoke.status_code == 200

    verify_deny = client.post(
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
    assert verify_deny.status_code == 200
    assert verify_deny.json()["decision"] == "DENY"
    assert verify_deny.json()["reason_code"] == "AGENT_REVOKED"

    audit_export = client.get(
        f"/audit/export.json?workspace_id={workspace_id}",
        headers={"X-Workspace-Id": workspace_id},
    )
    assert audit_export.status_code == 200
    audit_items = cast(list[dict[str, object]], audit_export.json())
    assert len(audit_items) >= 9
    audit_types = {str(item["event_type"]) for item in audit_items}
    assert {
        "agent.created",
        "policy.created",
        "policy.bound",
        "capability.issued",
        "agent.revoked",
        "action.verification.requested",
        "action.verification.allowed",
        "action.verification.denied",
    }.issubset(audit_types)

    integrity = client.get(
        f"/audit/integrity/check?workspace_id={workspace_id}",
        headers={"X-Workspace-Id": workspace_id},
    )
    assert integrity.status_code == 200
    assert integrity.json()["status"] == "OK"

    metrics = client.get("/metrics")
    assert metrics.status_code == 200
    assert "kya_verify_total" in metrics.text
    assert "kya_audit_integrity_total" in metrics.text
