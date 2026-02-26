from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import raise_http_error
from app.models.agent import Agent
from app.models.agent_policy_binding import AgentPolicyBinding
from app.modules.audit_log.service import append_audit_event
from app.modules.policy_service.service import get_policy_in_workspace


def bind_policy_to_agent(
    db: Session,
    *,
    agent_id: UUID,
    policy_id: UUID,
    workspace_id: UUID,
) -> AgentPolicyBinding:
    agent = db.scalar(select(Agent).where(Agent.id == agent_id, Agent.workspace_id == workspace_id))
    if agent is None:
        raise_http_error(404, "AGENT_NOT_FOUND", "Agent not found")

    if agent.status == "revoked":
        raise_http_error(409, "AGENT_REVOKED", "Agent is revoked")

    policy = get_policy_in_workspace(db, policy_id=policy_id, workspace_id=workspace_id)
    if policy is None:
        raise_http_error(404, "POLICY_NOT_FOUND", "Policy not found")

    now = datetime.now(tz=UTC)
    active_bindings = db.scalars(
        select(AgentPolicyBinding).where(
            AgentPolicyBinding.agent_id == agent_id,
            AgentPolicyBinding.status == "active",
        )
    ).all()
    for binding in active_bindings:
        binding.status = "inactive"
        binding.unbound_at = now

    new_binding = AgentPolicyBinding(
        workspace_id=workspace_id,
        agent_id=agent_id,
        policy_id=policy_id,
        status="active",
        bound_at=now,
    )
    db.add(new_binding)
    db.flush()

    append_audit_event(
        db,
        workspace_id=workspace_id,
        event_type="policy.bound",
        subject_type="agent",
        subject_id=agent_id,
        event_data={"workspace_id": str(workspace_id), "policy_id": str(policy_id)},
    )

    db.commit()
    db.refresh(new_binding)
    return new_binding
