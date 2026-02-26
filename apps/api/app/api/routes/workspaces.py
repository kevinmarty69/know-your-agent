from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import (
    AuthContext,
    ensure_workspace_match,
    get_auth_context,
    require_bootstrap_token,
)
from app.core.openapi import COMMON_ERROR_RESPONSES
from app.db.session import get_db
from app.modules.workspace_service.service import create_workspace, get_workspace
from app.schemas.workspace import WorkspaceCreateRequest, WorkspaceResponse

router = APIRouter(tags=["workspaces"])
DbSession = Annotated[Session, Depends(get_db)]
Auth = Annotated[AuthContext, Depends(get_auth_context)]
BootstrapGuard = Annotated[None, Depends(require_bootstrap_token)]


@router.post(
    "/workspaces",
    response_model=WorkspaceResponse,
    status_code=201,
    summary="Create Workspace",
    description="Creates a workspace for local bootstrap/dev flows.",
    responses={
        **COMMON_ERROR_RESPONSES,
        409: {
            "description": "Workspace slug already exists.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "code": "WORKSPACE_SLUG_ALREADY_EXISTS",
                            "message": "Workspace slug already exists",
                        }
                    }
                }
            },
        },
        503: {
            "description": "Workspace bootstrap endpoint disabled by configuration.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "code": "WORKSPACE_BOOTSTRAP_DISABLED",
                            "message": (
                                "Workspace bootstrap is disabled; configure "
                                "KYA_WORKSPACE_BOOTSTRAP_TOKEN"
                            ),
                        }
                    }
                }
            },
        },
    },
)
def create_workspace_endpoint(
    payload: WorkspaceCreateRequest,
    _: BootstrapGuard,
    db: DbSession,
) -> WorkspaceResponse:
    workspace = create_workspace(db, payload)
    return WorkspaceResponse.model_validate(workspace)


@router.get(
    "/workspaces/{workspace_id}",
    response_model=WorkspaceResponse,
    summary="Get Workspace",
    description="Fetches a workspace by id within authenticated tenant context.",
    responses={
        **COMMON_ERROR_RESPONSES,
        404: {
            "description": "Workspace not found.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "code": "WORKSPACE_NOT_FOUND",
                            "message": "Workspace not found",
                        }
                    }
                }
            },
        },
    },
)
def get_workspace_endpoint(workspace_id: UUID, auth: Auth, db: DbSession) -> WorkspaceResponse:
    ensure_workspace_match(auth.workspace_id, workspace_id)
    workspace = get_workspace(db, workspace_id)
    return WorkspaceResponse.model_validate(workspace)
