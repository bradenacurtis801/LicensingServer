import logging
from typing import Optional
from app.utils.rsa_verification import RSAVerifier

logger = logging.getLogger(__name__)

_private_key_pem: Optional[str] = None


def init_signing_key(key_path: Optional[str]) -> None:
    global _private_key_pem
    if not key_path:
        logger.warning("RSA_PRIVATE_KEY_PATH not set — validation responses will not be signed")
        return
    try:
        with open(key_path, "r") as f:
            _private_key_pem = f.read()
        logger.info(f"RSA signing key loaded from {key_path}")
    except FileNotFoundError:
        logger.warning(f"RSA private key file not found: {key_path} — validation responses will not be signed")
    except Exception as e:
        logger.error(f"Failed to load RSA private key from {key_path}: {e}")


def sign_response(data: dict) -> Optional[str]:
    if not _private_key_pem:
        return None
    try:
        return RSAVerifier.create_signature(data, _private_key_pem)
    except Exception as e:
        logger.error(f"Failed to sign validation response: {e}")
        return None
