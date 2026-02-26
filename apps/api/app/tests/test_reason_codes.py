from app.core.reason_codes import ReasonCode, is_valid_reason_code


def test_reason_codes_are_stable() -> None:
    expected = {
        "AGENT_NOT_FOUND",
        "AGENT_REVOKED",
        "POLICY_NOT_BOUND",
        "CAPABILITY_INVALID",
        "CAPABILITY_EXPIRED",
        "CAPABILITY_REVOKED",
        "CAPABILITY_SCOPE_MISMATCH",
        "SIGNATURE_INVALID",
        "SPEND_LIMIT_EXCEEDED",
        "RATE_LIMIT_EXCEEDED",
        "WORKSPACE_MISMATCH",
    }

    assert {code.value for code in ReasonCode} == expected


def test_reason_code_validator() -> None:
    assert is_valid_reason_code("AGENT_REVOKED")
    assert not is_valid_reason_code("UNKNOWN_CODE")
