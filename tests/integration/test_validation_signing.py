"""
Integration tests for RSA-signed validation responses.

Uses FastAPI TestClient with an in-memory SQLite database.
No running server required.

Covers:
- Signature present on valid and invalid responses
- Signature verifies against the matching public key
- Tampered data fails verification
- Wrong public key fails verification
- Null signature when no key is configured
"""
import pytest
from app.utils.rsa_verification import RSAVerifier
import app.core.signing as signing


def _validate(client, license_key: str, machine_id: str = "test-machine-001") -> dict:
    resp = client.post("/api/v1/validation/", json={
        "license_key": license_key,
        "machine_id": machine_id,
    })
    assert resp.status_code == 200
    return resp.json()


def _verify(response: dict, public_key_pem: str) -> bool:
    signature = response.get("signature")
    if not signature:
        return False
    sign_data = {
        "valid": response["valid"],
        "license_id": response.get("license_id"),
        "expires_at": response.get("expires_at"),
        "features": response.get("features"),
    }
    return RSAVerifier.verify_signature(sign_data, signature, public_key_pem)


@pytest.mark.integration
class TestValidationSigning:

    def test_valid_response_includes_signature(self, client, license_key):
        response = _validate(client, license_key)

        assert response["valid"] is True
        assert response["signature"] is not None

    def test_signature_verifies_with_correct_public_key(self, client, license_key, rsa_key_pair):
        _, public_pem = rsa_key_pair

        response = _validate(client, license_key)

        assert _verify(response, public_pem) is True

    def test_tampered_valid_field_fails_verification(self, client, license_key, rsa_key_pair):
        _, public_pem = rsa_key_pair
        response = _validate(client, license_key)

        tampered = {**response, "valid": False}

        assert _verify(tampered, public_pem) is False

    def test_tampered_features_fails_verification(self, client, license_key, rsa_key_pair):
        _, public_pem = rsa_key_pair
        response = _validate(client, license_key)

        tampered = {**response, "features": {"admin": True, "bypass": True}}

        assert _verify(tampered, public_pem) is False

    def test_wrong_public_key_fails_verification(self, client, license_key):
        _, unrelated_public_pem = RSAVerifier.generate_key_pair()
        response = _validate(client, license_key)

        assert _verify(response, unrelated_public_pem) is False

    def test_invalid_license_is_also_signed(self, client, rsa_key_pair):
        _, public_pem = rsa_key_pair

        response = _validate(client, "AAAAA-BBBBB-CCCCC-DDDDD-EEEEE")

        assert response["valid"] is False
        assert response["signature"] is not None
        assert _verify(response, public_pem) is True

    def test_no_signing_key_returns_null_signature(self, client, license_key):
        original = signing._private_key_pem
        signing._private_key_pem = None
        try:
            response = _validate(client, license_key)
            assert response["signature"] is None
        finally:
            signing._private_key_pem = original
