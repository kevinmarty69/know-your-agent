from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import AuthContext, ensure_workspace_match, get_auth_context
from app.core.openapi import COMMON_ERROR_RESPONSES
from app.db.session import get_db
from app.modules.capability_issuer.service import issue_capability
from app.schemas.capability import CapabilityIssueResponse, CapabilityRequest

router = APIRouter(tags=["capabilities"])
DbSession = Annotated[Session, Depends(get_db)]
Auth = Annotated[AuthContext, Depends(get_auth_context)]


@router.post(
    "/capabilities/request",
    response_model=CapabilityIssueResponse,
    status_code=201,
    summary="Issue Capability",
    description="Issues a signed capability token if agent/policy constraints allow it.",
    responses={
        **COMMON_ERROR_RESPONSES,
        404: {
            "description": "Agent or policy binding not found.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "code": "POLICY_NOT_BOUND",
                            "message": "No active policy binding found for this agent",
                        }
                    }
                }
            },
        },
        409: {
            "description": "Agent revoked.",
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
def request_capability_endpoint(
    payload: CapabilityRequest,
    auth: Auth,
    db: DbSession,
) -> CapabilityIssueResponse:
    ensure_workspace_match(auth.workspace_id, payload.workspace_id)
    return issue_capability(db, payload)
