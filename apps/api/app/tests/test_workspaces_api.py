from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.main import app
from app.models.audit_event import AuditEvent


def _bootstrap_headers(token: str = "test-bootstrap-token") -> dict[str, str]:
    return {"X-Bootstrap-Token": token}


def test_create_workspace_success() -> None:
    client = TestClient(app)

    response = client.post(
        "/workspaces",
        json={"name": "Acme Sandbox", "slug": "acme-sandbox"},
        headers=_bootstrap_headers(),
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["name"] == "Acme Sandbox"
    assert payload["slug"] == "acme-sandbox"
    assert payload["status"] == "active"


def test_create_workspace_slug_auto_derived() -> None:
    client = TestClient(app)

    response = client.post(
        "/workspaces",
        json={"name": "Acme Workspace V1"},
        headers=_bootstrap_headers(),
    )

    assert response.status_code == 201
    assert response.json()["slug"] == "acme-workspace-v1"


def test_create_workspace_duplicate_slug_conflict() -> None:
    client = TestClient(app)

    first = client.post(
        "/workspaces",
        json={"name": "First", "slug": "same-slug"},
        headers=_bootstrap_headers(),
    )
    second = client.post(
        "/workspaces",
        json={"name": "Second", "slug": "same-slug"},
        headers=_bootstrap_headers(),
    )

    assert first.status_code == 201
    assert second.status_code == 409
    assert second.json()["detail"]["code"] == "WORKSPACE_SLUG_ALREADY_EXISTS"


def test_create_workspace_missing_bootstrap_token_unauthorized() -> None:
    client = TestClient(app)

    response = client.post("/workspaces", json={"name": "No token", "slug": "no-token"})

    assert response.status_code == 401
    assert response.json()["detail"]["code"] == "AUTH_BOOTSTRAP_MISSING"


def test_create_workspace_invalid_bootstrap_token_unauthorized() -> None:
    client = TestClient(app)

    response = client.post(
        "/workspaces",
        json={"name": "Bad token", "slug": "bad-token"},
        headers=_bootstrap_headers("wrong-token"),
    )

    assert response.status_code == 401
    assert response.json()["detail"]["code"] == "AUTH_BOOTSTRAP_INVALID"


def test_create_workspace_bootstrap_not_configured_service_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = TestClient(app)
    monkeypatch.setattr(settings, "kya_workspace_bootstrap_token", None)

    response = client.post(
        "/workspaces",
        json={"name": "No config", "slug": "no-config"},
        headers=_bootstrap_headers(),
    )

    assert response.status_code == 503
    assert response.json()["detail"]["code"] == "WORKSPACE_BOOTSTRAP_DISABLED"


def test_get_workspace_success(client: TestClient, workspace_id: str) -> None:
    response = client.get(f"/workspaces/{workspace_id}")

    assert response.status_code == 200
    assert response.json()["id"] == workspace_id


def test_get_workspace_workspace_mismatch_denied(client: TestClient, workspace_id: str) -> None:
    response = client.get(
        f"/workspaces/{workspace_id}",
        headers={"X-Workspace-Id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"},
    )

    assert response.status_code == 403
    assert response.json()["detail"]["code"] == "WORKSPACE_MISMATCH"


def test_get_workspace_unknown_id_not_found() -> None:
    unknown = str(uuid4())
    client = TestClient(app, headers={"X-Workspace-Id": unknown})

    response = client.get(f"/workspaces/{unknown}")

    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "WORKSPACE_NOT_FOUND"


def test_workspace_created_event_written_to_audit(db_session: Session) -> None:
    client = TestClient(app)
    response = client.post(
        "/workspaces",
        json={"name": "Audit Workspace", "slug": "audit-workspace"},
        headers=_bootstrap_headers(),
    )
    assert response.status_code == 201

    event_types = db_session.scalars(select(AuditEvent.event_type)).all()
    assert "workspace.created" in event_types
