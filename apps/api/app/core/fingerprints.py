import base64
import hashlib

from app.core.errors import raise_http_error


def compute_public_key_fingerprint(public_key_b64: str) -> str:
    try:
        key_bytes = base64.b64decode(public_key_b64, validate=True)
    except Exception:
        raise_http_error(422, "VALIDATION_ERROR", "public_key must be valid base64")

    if len(key_bytes) != 32:
        raise_http_error(422, "VALIDATION_ERROR", "public_key must decode to 32 bytes for Ed25519")

    digest = hashlib.sha256(key_bytes).hexdigest()
    return f"sha256:{digest}"
