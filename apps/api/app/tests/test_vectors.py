import json
from hashlib import sha256
from pathlib import Path

from app.modules.verify_engine.canonical_json import canonical_json_bytes


def test_shared_verify_vectors_match_backend_canonicalization() -> None:
    vectors_dir = Path(__file__).resolve().parents[4] / "shared-test-vectors" / "verify"
    vector_files = sorted(vectors_dir.glob("*.json"))
    assert vector_files

    for vector_file in vector_files:
        data = json.loads(vector_file.read_text(encoding="utf-8"))
        envelope = data["input"]
        expected = data["expected"]

        canonical = canonical_json_bytes(envelope).decode("utf-8")
        digest = sha256(canonical.encode("utf-8")).hexdigest()

        assert canonical == expected["canonical_json"]
        assert digest == expected["sha256_hex"]
