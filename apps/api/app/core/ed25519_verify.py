import base64

from nacl.signing import VerifyKey


def verify_ed25519_signature(
    *,
    public_key_b64: str,
    message: bytes,
    signature_b64: str,
) -> bool:
    try:
        public_key = base64.b64decode(public_key_b64, validate=True)
        signature = base64.b64decode(signature_b64, validate=True)
        VerifyKey(public_key).verify(message, signature)
        return True
    except Exception:
        return False
