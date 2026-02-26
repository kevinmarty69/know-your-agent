import json
from collections.abc import Mapping


def canonical_json_bytes(payload: Mapping[str, object]) -> bytes:
    # Stable and language-agnostic canonical form for signing and verification.
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return canonical.encode("utf-8")
