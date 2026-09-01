import pytest

from app.modules.verify_engine.policy_eval import (
    capability_allows_payload_spend,
    policy_allows_payload_spend,
    scopes_allow_action,
)

pytestmark = pytest.mark.unit


@pytest.mark.parametrize("amount", ["-0.01", "NaN", "Infinity"])
def test_spend_checks_reject_invalid_amounts(amount: str) -> None:
    assert not policy_allows_payload_spend(
        policy_json={"spend": {"max_per_tx": "20.00", "currency": "EUR"}},
        payload={"amount": amount, "currency": "EUR"},
    )


def test_capability_limit_is_precise_and_currency_bound() -> None:
    limits: dict[str, object] = {"amount": "20.00", "currency": "EUR"}

    assert capability_allows_payload_spend(
        limits=limits,
        payload={"amount": "20.00", "currency": "EUR"},
    )
    assert not capability_allows_payload_spend(
        limits=limits,
        payload={"amount": "20.01", "currency": "EUR"},
    )
    assert not capability_allows_payload_spend(
        limits=limits,
        payload={"amount": "10.00", "currency": "USD"},
    )
    assert not capability_allows_payload_spend(limits=limits, payload={"currency": "EUR"})
    assert not policy_allows_payload_spend(
        policy_json={"spend": {"max_per_tx": "20.00", "currency": "EUR"}},
        payload={"currency": "EUR"},
    )


def test_scope_never_falls_back_to_untrusted_payload_tool() -> None:
    assert not scopes_allow_action(scopes=["purchase"], action_type="delete_all")
