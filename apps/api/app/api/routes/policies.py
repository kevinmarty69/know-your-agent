from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import AuthContext, ensure_workspace_match, get_auth_context
from app.core.openapi import COMMON_ERROR_RESPONSES
from app.db.session import get_db
from app.modules.policy_service.binding_service import bind_policy_to_agent
from app.modules.policy_service.service import create_policy
from app.schemas.binding import PolicyBindingResponse, PolicyBindRequest
from app.schemas.policy import PolicyCreateRequest, PolicyResponse

router = APIRouter(tags=["policies"])
DbSession = Annotated[Session, Depends(get_db)]
Auth = Annotated[AuthContext, Depends(get_auth_context)]


@router.post(
    "/policies",
    response_model=PolicyResponse,
    status_code=201,
    summary="Create Policy",
    description="Creates a versioned policy in a workspace.",
    responses={
        **COMMON_ERROR_RESPONSES,
        409: {
            "description": "Policy version already exists.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "code": "POLICY_VERSION_ALREADY_EXISTS",
                            "message": "Policy version already exists",
                        }
                    }
                }
            },
        },
    },
)
def create_policy_endpoint(
    payload: PolicyCreateRequest,
    auth: Auth,
    db: DbSession,
) -> PolicyResponse:
    ensure_workspace_match(auth.workspace_id, payload.workspace_id)
    policy = create_policy(db, payload)
    return PolicyResponse.model_validate(policy)


@router.post(
    "/agents/{agent_id}/bind_policy",
    response_model=PolicyBindingResponse,
    status_code=201,
    summary="Bind Policy To Agent",
    description="Binds a policy to an agent, deactivating previous active binding if any.",
    responses={
        **COMMON_ERROR_RESPONSES,
        404: {
            "description": "Agent or policy not found.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "code": "POLICY_OR_AGENT_NOT_FOUND",
                            "message": "Agent or policy not found",
                        }
                    }
                }
            },
        },
        409: {
            "description": "Agent is revoked and cannot be bound.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {"code": "AGENT_REVOKED", "message": "Agent is revoked"}
                    }
                }
            },
        },
    },
)
def bind_policy_endpoint(
    agent_id: UUID,
    payload: PolicyBindRequest,
    auth: Auth,
    db: DbSession,
) -> PolicyBindingResponse:
    ensure_workspace_match(auth.workspace_id, payload.workspace_id)
    binding = bind_policy_to_agent(
        db,
        agent_id=agent_id,
        policy_id=payload.policy_id,
        workspace_id=auth.workspace_id,
    )
    return PolicyBindingResponse.model_validate(binding)
