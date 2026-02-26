import hmac
from dataclasses import dataclass
from uuid import UUID

from fastapi import Security
from fastapi.security.api_key import APIKeyHeader

from app.core.config import settings
from app.core.errors import raise_http_error


@dataclass(frozen=True)
class AuthContext:
    workspace_id: UUID
    actor_id: str | None


workspace_id_header = APIKeyHeader(name="X-Workspace-Id", auto_error=False)
actor_id_header = APIKeyHeader(name="X-Actor-Id", auto_error=False)
bootstrap_token_header = APIKeyHeader(name="X-Bootstrap-Token", auto_error=False)


def get_auth_context(
    x_workspace_id: str | None = Security(workspace_id_header),
    x_actor_id: str | None = Security(actor_id_header),
) -> AuthContext:
    if x_workspace_id is None:
        raise_http_error(401, "AUTH_WORKSPACE_MISSING", "Missing X-Workspace-Id header")

    try:
        workspace_id = UUID(x_workspace_id)
    except ValueError:
        raise_http_error(401, "AUTH_WORKSPACE_INVALID", "Invalid X-Workspace-Id header")

    return AuthContext(workspace_id=workspace_id, actor_id=x_actor_id)


def ensure_workspace_match(auth_workspace_id: UUID, request_workspace_id: UUID) -> None:
    if auth_workspace_id != request_workspace_id:
        raise_http_error(
            403,
            "WORKSPACE_MISMATCH",
            "Workspace does not match authenticated context",
        )


def require_bootstrap_token(
    x_bootstrap_token: str | None = Security(bootstrap_token_header),
) -> None:
    configured_token = settings.kya_workspace_bootstrap_token
    if configured_token is None or not configured_token.strip():
        raise_http_error(
            503,
            "WORKSPACE_BOOTSTRAP_DISABLED",
            "Workspace bootstrap is disabled; configure KYA_WORKSPACE_BOOTSTRAP_TOKEN",
        )

    if x_bootstrap_token is None:
        raise_http_error(401, "AUTH_BOOTSTRAP_MISSING", "Missing X-Bootstrap-Token header")

    if not hmac.compare_digest(x_bootstrap_token, configured_token):
        raise_http_error(401, "AUTH_BOOTSTRAP_INVALID", "Invalid X-Bootstrap-Token header")
