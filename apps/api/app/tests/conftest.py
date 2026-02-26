import os
from collections.abc import Generator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.orm import Session

# Mandatory runtime JWT config for app startup in tests.
os.environ.setdefault("KYA_JWT_KID", "test-ed25519-key-1")
os.environ.setdefault(
    "KYA_JWT_PRIVATE_KEY_PEM",
    "-----BEGIN PRIVATE KEY-----\n"
    "MC4CAQAwBQYDK2VwBCIEIL1+Klzp5E0gHEu8KSBoLuWCxKDLdmgjxNmo3FNARcVl\n"
    "-----END PRIVATE KEY-----",
)
os.environ.setdefault(
    "KYA_JWT_PUBLIC_KEY_PEM",
    "-----BEGIN PUBLIC KEY-----\n"
    "MCowBQYDK2VwAyEA/UbU9hxaQZ9Rw3x9FPaAhRaXpvV/xsksX10W4S17Was=\n"
    "-----END PUBLIC KEY-----",
)
os.environ.setdefault("KYA_WORKSPACE_BOOTSTRAP_TOKEN", "test-bootstrap-token")

from app.db.session import SessionLocal  # noqa: E402
from app.main import app  # noqa: E402
from app.models.workspace import Workspace  # noqa: E402

TABLES_TO_TRUNCATE = [
    "revocations",
    "audit_events",
    "capabilities",
    "agent_policy_bindings",
    "policies",
    "agents",
    "workspaces",
]


@pytest.fixture(autouse=True)
def clean_database() -> Generator[None, None, None]:
    with SessionLocal() as db:
        db.execute(text(f"TRUNCATE TABLE {', '.join(TABLES_TO_TRUNCATE)} RESTART IDENTITY CASCADE"))
        db.commit()
    yield


@pytest.fixture
def client(workspace_id: str) -> TestClient:
    return TestClient(app, headers={"X-Workspace-Id": workspace_id})


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session


@pytest.fixture
def workspace_id(db_session: Session) -> str:
    workspace = Workspace(
        id=uuid4(),
        name="Test Workspace",
        slug=f"workspace-{uuid4().hex[:8]}",
        status="active",
    )
    db_session.add(workspace)
    db_session.commit()
    return str(workspace.id)


@pytest.fixture
def auth_headers(workspace_id: str) -> dict[str, str]:
    return {"X-Workspace-Id": workspace_id}
