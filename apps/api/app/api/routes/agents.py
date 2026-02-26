from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import AuthContext, ensure_workspace_match, get_auth_context
from app.core.openapi import COMMON_ERROR_RESPONSES
from app.db.session import get_db
from app.modules.agent_registry.service import create_agent, get_agent, revoke_agent
from app.schemas.agent import (
    AgentCreateRequest,
    AgentResponse,
    AgentRevokeRequest,
    AgentRevokeResponse,
)

router = APIRouter(tags=["agents"])
DbSession = Annotated[Session, Depends(get_db)]
Auth = Annotated[AuthContext, Depends(get_auth_context)]


@router.post(
    "/agents",
    response_model=AgentResponse,
    status_code=201,
    summary="Create Agent",
    description="Registers a new agent identity in a workspace.",
    responses={
        **COMMON_ERROR_RESPONSES,
        409: {
            "description": "Agent fingerprint already exists.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "code": "AGENT_FINGERPRINT_ALREADY_EXISTS",
                            "message": "An agent with this public key already exists",
                        }
                    }
                }
            },
        },
    },
)
def create_agent_endpoint(payload: AgentCreateRequest, auth: Auth, db: DbSession) -> AgentResponse:
    ensure_workspace_match(auth.workspace_id, payload.workspace_id)
    agent = create_agent(db, payload)
    return AgentResponse(
        id=agent.id,
        workspace_id=agent.workspace_id,
        name=agent.name,
        status=agent.status,
        public_key=agent.public_key,
        key_alg=agent.key_alg,
        fingerprint=agent.fingerprint,
        runtime_type=agent.runtime_type,
        metadata=agent.metadata_json,
        created_at=agent.created_at,
        revoked_at=agent.revoked_at,
        revoke_reason=agent.revoke_reason,
    )


@router.get(
    "/agents/{agent_id}",
    response_model=AgentResponse,
    summary="Get Agent",
    description="Fetches a single agent by id.",
    responses={
        **COMMON_ERROR_RESPONSES,
        404: {
            "description": "Agent not found.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {"code": "AGENT_NOT_FOUND", "message": "Agent not found"}
                    }
                }
            },
        },
    },
)
def get_agent_endpoint(agent_id: UUID, auth: Auth, db: DbSession) -> AgentResponse:
    agent = get_agent(db, agent_id)
    ensure_workspace_match(auth.workspace_id, agent.workspace_id)
    return AgentResponse(
        id=agent.id,
        workspace_id=agent.workspace_id,
        name=agent.name,
        status=agent.status,
        public_key=agent.public_key,
        key_alg=agent.key_alg,
        fingerprint=agent.fingerprint,
        runtime_type=agent.runtime_type,
        metadata=agent.metadata_json,
        created_at=agent.created_at,
        revoked_at=agent.revoked_at,
        revoke_reason=agent.revoke_reason,
    )


@router.post(
    "/agents/{agent_id}/revoke",
    response_model=AgentRevokeResponse,
    summary="Revoke Agent",
    description="Revokes an active agent. Future actions are denied.",
    responses={
        **COMMON_ERROR_RESPONSES,
        404: {
            "description": "Agent not found.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {"code": "AGENT_NOT_FOUND", "message": "Agent not found"}
                    }
                }
            },
        },
        409: {
            "description": "Agent already revoked.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "code": "AGENT_ALREADY_REVOKED",
                            "message": "Agent is already revoked",
                        }
                    }
                }
            },
        },
    },
)
def revoke_agent_endpoint(
    agent_id: UUID,
    payload: AgentRevokeRequest,
    auth: Auth,
    db: DbSession,
) -> AgentRevokeResponse:
    ensure_workspace_match(auth.workspace_id, payload.workspace_id)
    agent = revoke_agent(
        db,
        agent_id=agent_id,
        workspace_id=auth.workspace_id,
        reason=payload.reason,
    )
    if agent.revoked_at is None:
        raise RuntimeError("revoked_at must be set after revoke")

    return AgentRevokeResponse(id=agent.id, status=agent.status, revoked_at=agent.revoked_at)
