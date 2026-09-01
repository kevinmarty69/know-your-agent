from decimal import Decimal, InvalidOperation
from uuid import UUID

from app.modules.revocation.service import check_rate_limit


def scopes_allow_action(*, scopes: list[str], action_type: str) -> bool:
    return action_type in scopes


def policy_allows_scope(*, policy_json: dict[str, object], requested_scopes: list[str]) -> bool:
    allowed_tools = policy_json.get("allowed_tools", [])
    if not isinstance(allowed_tools, list):
        return False

    allowed = {str(x) for x in allowed_tools}
    return set(requested_scopes).issubset(allowed)


def policy_allows_spend_request(
    *,
    policy_json: dict[str, object],
    requested_limits: dict[str, object],
) -> bool:
    spend = policy_json.get("spend")
    req_amount = requested_limits.get("amount")
    if not isinstance(spend, dict):
        return req_amount is None or _valid_amount(req_amount)
    if req_amount is None:
        return spend.get("max_per_tx") is None
    return _spend_within_limit(limit=spend, requested=requested_limits)


def _amount(value: object) -> Decimal | None:
    try:
        parsed = Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None
    return parsed if parsed.is_finite() and parsed >= 0 else None


def _valid_amount(value: object) -> bool:
    return _amount(value) is not None


def _spend_within_limit(*, limit: dict[str, object], requested: dict[str, object]) -> bool:
    requested_amount = _amount(requested.get("amount"))
    max_amount = _amount(limit.get("max_per_tx", limit.get("amount")))
    if requested_amount is None or max_amount is None or requested_amount > max_amount:
        return False

    currency = limit.get("currency")
    return currency is None or requested.get("currency") == currency


def policy_allows_payload_spend(
    *,
    policy_json: dict[str, object],
    payload: dict[str, object],
) -> bool:
    spend = policy_json.get("spend")
    amount = payload.get("amount")
    if not isinstance(spend, dict):
        return amount is None or _valid_amount(amount)
    if amount is None:
        return spend.get("max_per_tx") is None
    return _spend_within_limit(limit=spend, requested=payload)


def capability_allows_payload_spend(
    *,
    limits: dict[str, object],
    payload: dict[str, object],
) -> bool:
    if payload.get("amount") is None:
        return limits.get("amount") is None
    return _spend_within_limit(limit=limits, requested=payload)


def policy_allows_rate(
    *,
    policy_json: dict[str, object],
    workspace_id: UUID,
    agent_id: UUID,
    action_type: str,
) -> bool:
    rate_limits = policy_json.get("rate_limits")
    if not isinstance(rate_limits, dict):
        return True

    max_actions_per_min = rate_limits.get("max_actions_per_min")
    if max_actions_per_min is None:
        return True

    try:
        limit = int(max_actions_per_min)
    except (TypeError, ValueError):
        return False

    return check_rate_limit(
        workspace_id=workspace_id,
        agent_id=agent_id,
        action_type=action_type,
        max_actions_per_min=limit,
    )
