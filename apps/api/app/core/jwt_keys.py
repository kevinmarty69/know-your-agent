from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

from app.core.config import settings


def _normalize_pem(value: str) -> str:
    return value.replace("\\n", "\n").strip() + "\n"


def load_jwt_private_key() -> Ed25519PrivateKey:
    if not settings.kya_jwt_private_key_pem:
        raise RuntimeError("Missing required setting: KYA_JWT_PRIVATE_KEY_PEM")

    try:
        key = serialization.load_pem_private_key(
            _normalize_pem(settings.kya_jwt_private_key_pem).encode("utf-8"),
            password=None,
        )
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("Invalid KYA_JWT_PRIVATE_KEY_PEM") from exc

    if not isinstance(key, Ed25519PrivateKey):
        raise RuntimeError("KYA_JWT_PRIVATE_KEY_PEM must be an Ed25519 private key")

    return key


def load_jwt_public_key() -> Ed25519PublicKey:
    if not settings.kya_jwt_public_key_pem:
        raise RuntimeError("Missing required setting: KYA_JWT_PUBLIC_KEY_PEM")

    try:
        key = serialization.load_pem_public_key(
            _normalize_pem(settings.kya_jwt_public_key_pem).encode("utf-8")
        )
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("Invalid KYA_JWT_PUBLIC_KEY_PEM") from exc

    if not isinstance(key, Ed25519PublicKey):
        raise RuntimeError("KYA_JWT_PUBLIC_KEY_PEM must be an Ed25519 public key")

    return key


def validate_jwt_key_config() -> None:
    if not settings.kya_jwt_kid:
        raise RuntimeError("Missing required setting: KYA_JWT_KID")

    load_jwt_private_key()
    load_jwt_public_key()
