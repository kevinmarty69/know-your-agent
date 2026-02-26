from datetime import UTC, datetime, timedelta
from typing import cast
from uuid import UUID

import jwt

from app.core.config import settings
from app.core.jwt_keys import load_jwt_private_key, load_jwt_public_key

ALGO = "EdDSA"


def build_capability_claims(
    *,
    agent_id: UUID,
    workspace_id: UUID,
    scopes: list[str],
    limits: dict[str, object],
    policy_id: UUID,
    policy_version: int,
    jti: str,
    ttl_minutes: int,
) -> dict[str, object]:
    now = datetime.now(tz=UTC)
    exp = now + timedelta(minutes=ttl_minutes)

    return {
        "sub": str(agent_id),
        "workspace_id": str(workspace_id),
        "scopes": scopes,
        "limits": limits,
        "policy_id": str(policy_id),
        "policy_version": policy_version,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
        "jti": jti,
    }


def encode_capability_token(claims: dict[str, object]) -> str:
    private_key = load_jwt_private_key()
    return jwt.encode(
        claims,
        private_key,
        algorithm=ALGO,
        headers={"kid": settings.kya_jwt_kid},
    )


def decode_capability_token(token: str) -> dict[str, object]:
    public_key = load_jwt_public_key()
    claims = jwt.decode(
        token,
        public_key,
        algorithms=[ALGO],
        leeway=settings.jwt_leeway_seconds,
        options={"require": ["sub", "workspace_id", "exp", "iat", "jti"]},
    )
    return cast(dict[str, object], claims)
