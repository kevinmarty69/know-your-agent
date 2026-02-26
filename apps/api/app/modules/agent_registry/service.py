from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import raise_http_error
from app.core.fingerprints import compute_public_key_fingerprint
from app.models.agent import Agent
from app.models.workspace import Workspace
from app.modules.audit_log.service import append_audit_event
from app.schemas.agent import AgentCreateRequest


def create_agent(db: Session, payload: AgentCreateRequest) -> Agent:
    workspace = db.scalar(select(Workspace).where(Workspace.id == payload.workspace_id))
    if workspace is None:
        raise_http_error(404, "WORKSPACE_NOT_FOUND", "Workspace not found")

    fingerprint = compute_public_key_fingerprint(payload.public_key)
    existing = db.scalar(
        select(Agent).where(
            Agent.workspace_id == payload.workspace_id,
            Agent.fingerprint == fingerprint,
        )
    )
    if existing is not None:
        raise_http_error(
            409,
            "AGENT_FINGERPRINT_ALREADY_EXISTS",
            "Agent fingerprint already exists",
        )

    agent = Agent(
        workspace_id=payload.workspace_id,
        name=payload.name,
        status="active",
        public_key=payload.public_key,
        key_alg="ed25519",
        fingerprint=fingerprint,
        runtime_type=payload.runtime_type,
        metadata_json=payload.metadata,
    )
    db.add(agent)
    db.flush()

    append_audit_event(
        db,
        workspace_id=payload.workspace_id,
        event_type="agent.created",
        subject_type="agent",
        subject_id=agent.id,
        event_data={"workspace_id": str(payload.workspace_id), "name": payload.name},
    )

    db.commit()
    db.refresh(agent)
    return agent


def get_agent(db: Session, agent_id: UUID) -> Agent:
    agent = db.scalar(select(Agent).where(Agent.id == agent_id))
    if agent is None:
        raise_http_error(404, "AGENT_NOT_FOUND", "Agent not found")
    return agent


def revoke_agent(db: Session, *, agent_id: UUID, workspace_id: UUID, reason: str) -> Agent:
    agent = db.scalar(select(Agent).where(Agent.id == agent_id, Agent.workspace_id == workspace_id))
    if agent is None:
        raise_http_error(404, "AGENT_NOT_FOUND", "Agent not found")

    if agent.status == "revoked":
        raise_http_error(409, "AGENT_ALREADY_REVOKED", "Agent already revoked")

    now = datetime.now(tz=UTC)
    agent.status = "revoked"
    agent.revoked_at = now
    agent.revoke_reason = reason

    append_audit_event(
        db,
        workspace_id=workspace_id,
        event_type="agent.revoked",
        subject_type="agent",
        subject_id=agent.id,
        event_data={"workspace_id": str(workspace_id), "reason": reason},
    )

    db.commit()
    db.refresh(agent)
    return agent
