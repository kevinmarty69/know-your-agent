from uuid import UUID

from app.modules.revocation.service import check_rate_limit


def scopes_allow_action(*, scopes: list[str], action_type: str, tool: str | None) -> bool:
    if action_type in scopes:
        return True
    if tool and tool in scopes:
        return True
    return False


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
    if not isinstance(spend, dict):
        return True

    max_per_tx = spend.get("max_per_tx")
    req_amount = requested_limits.get("amount")
    if max_per_tx is None or req_amount is None:
        return True

    try:
        req_value = float(str(req_amount))
        max_value = float(str(max_per_tx))
        return req_value <= max_value
    except (TypeError, ValueError):
        return False


def policy_allows_payload_spend(
    *,
    policy_json: dict[str, object],
    payload: dict[str, object],
) -> bool:
    spend = policy_json.get("spend")
    if not isinstance(spend, dict):
        return True

    max_per_tx = spend.get("max_per_tx")
    amount = payload.get("amount")
    if max_per_tx is None or amount is None:
        return True

    try:
        amount_value = float(str(amount))
        max_value = float(str(max_per_tx))
        return amount_value <= max_value
    except (TypeError, ValueError):
        return False


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
