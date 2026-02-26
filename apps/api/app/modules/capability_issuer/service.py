from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.errors import raise_http_error
from app.core.jwt_tokens import build_capability_claims, encode_capability_token
from app.models.agent import Agent
from app.models.agent_policy_binding import AgentPolicyBinding
from app.models.capability import Capability
from app.models.policy import Policy
from app.modules.audit_log.service import append_audit_event
from app.modules.verify_engine.policy_eval import policy_allows_scope, policy_allows_spend_request
from app.schemas.capability import CapabilityIssueResponse, CapabilityRequest


def _get_active_policy_for_agent(db: Session, *, workspace_id: UUID, agent_id: UUID) -> Policy:
    binding = db.scalar(
        select(AgentPolicyBinding).where(
            AgentPolicyBinding.workspace_id == workspace_id,
            AgentPolicyBinding.agent_id == agent_id,
            AgentPolicyBinding.status == "active",
        )
    )
    if binding is None:
        raise_http_error(404, "POLICY_NOT_BOUND", "No active policy binding for agent")

    policy = db.scalar(
        select(Policy).where(
            Policy.id == binding.policy_id,
            Policy.workspace_id == workspace_id,
            Policy.is_active.is_(True),
        )
    )
    if policy is None:
        raise_http_error(404, "POLICY_NOT_BOUND", "No active policy found for binding")

    return policy


def issue_capability(db: Session, payload: CapabilityRequest) -> CapabilityIssueResponse:
    agent = db.scalar(
        select(Agent).where(
            Agent.id == payload.agent_id,
            Agent.workspace_id == payload.workspace_id,
        )
    )
    if agent is None:
        raise_http_error(404, "AGENT_NOT_FOUND", "Agent not found")
    if agent.status != "active":
        raise_http_error(409, "AGENT_REVOKED", "Agent is revoked")

    policy = _get_active_policy_for_agent(
        db,
        workspace_id=payload.workspace_id,
        agent_id=payload.agent_id,
    )

    if not policy_allows_scope(
        policy_json=policy.policy_json,
        requested_scopes=payload.requested_scopes,
    ):
        raise_http_error(422, "CAPABILITY_SCOPE_MISMATCH", "Requested scopes are not allowed")

    if not policy_allows_spend_request(
        policy_json=policy.policy_json,
        requested_limits=payload.requested_limits,
    ):
        raise_http_error(422, "SPEND_LIMIT_EXCEEDED", "Requested limits exceed policy")

    ttl_minutes = payload.ttl_minutes or settings.capability_default_ttl_minutes
    ttl_minutes = max(settings.capability_min_ttl_minutes, ttl_minutes)
    ttl_minutes = min(settings.capability_max_ttl_minutes, ttl_minutes)

    issued_at = datetime.now(tz=UTC)
    expires_at = issued_at + timedelta(minutes=ttl_minutes)
    jti = str(uuid4())

    capability = Capability(
        workspace_id=payload.workspace_id,
        agent_id=payload.agent_id,
        jti=jti,
        scopes={"items": payload.requested_scopes},
        limits=payload.requested_limits,
        status="active",
        issued_at=issued_at,
        expires_at=expires_at,
    )
    db.add(capability)
    db.flush()

    claims = build_capability_claims(
        agent_id=payload.agent_id,
        workspace_id=payload.workspace_id,
        scopes=payload.requested_scopes,
        limits=payload.requested_limits,
        policy_id=policy.id,
        policy_version=policy.version,
        jti=jti,
        ttl_minutes=ttl_minutes,
    )
    token = encode_capability_token(claims)

    append_audit_event(
        db,
        workspace_id=payload.workspace_id,
        event_type="capability.issued",
        subject_type="capability",
        subject_id=capability.id,
        event_data={
            "workspace_id": str(payload.workspace_id),
            "agent_id": str(payload.agent_id),
            "action": payload.action,
            "target_service": payload.target_service,
            "jti": jti,
            "exp": int(expires_at.timestamp()),
        },
    )

    db.commit()
    db.refresh(capability)

    return CapabilityIssueResponse(
        capability_id=capability.id,
        token=token,
        jti=jti,
        issued_at=capability.issued_at,
        expires_at=capability.expires_at,
    )
