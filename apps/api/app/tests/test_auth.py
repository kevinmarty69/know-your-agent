from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.core.auth import (
    create_workspace_key,
    ensure_workspace_match,
    get_auth_context,
    validate_workspace_auth_config,
)
from app.core.config import settings

pytestmark = pytest.mark.unit


def test_authenticated_workspace_must_match_request_workspace() -> None:
    with pytest.raises(HTTPException) as exc_info:
        ensure_workspace_match(uuid4(), uuid4())

    assert exc_info.value.status_code == 403
    assert isinstance(exc_info.value.detail, dict)
    assert exc_info.value.detail["code"] == "WORKSPACE_MISMATCH"


def test_workspace_key_is_bound_to_workspace() -> None:
    first = uuid4()
    second = uuid4()

    assert get_auth_context(str(first), create_workspace_key(first)).workspace_id == first
    with pytest.raises(HTTPException) as exc_info:
        get_auth_context(str(second), create_workspace_key(first))

    assert exc_info.value.status_code == 401
    assert isinstance(exc_info.value.detail, dict)
    assert exc_info.value.detail["code"] == "AUTH_WORKSPACE_KEY_INVALID"


def test_workspace_bootstrap_rejects_weak_auth_config(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, "limiq_workspace_auth_secret", "too-short")

    with pytest.raises(HTTPException) as exc_info:
        validate_workspace_auth_config()

    assert exc_info.value.status_code == 503
