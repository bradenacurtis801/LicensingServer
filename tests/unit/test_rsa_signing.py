"""
Unit tests for RSA signing utilities.
No database or server required.
"""
import pytest
import app.core.signing as signing
from app.utils.rsa_verification import RSAVerifier


@pytest.fixture
def key_pair():
    return RSAVerifier.generate_key_pair()


@pytest.mark.unit
class TestRSAVerifier:

    def test_key_pair_has_correct_pem_headers(self, key_pair):
        private_pem, public_pem = key_pair
        assert private_pem.startswith("-----BEGIN PRIVATE KEY-----")
        assert public_pem.startswith("-----BEGIN PUBLIC KEY-----")

    def test_sign_and_verify_roundtrip(self, key_pair):
        private_pem, public_pem = key_pair
        data = {
            "valid": True,
            "license_id": 42,
            "expires_at": "2027-01-01T00:00:00+00:00",
            "features": {"pro": True, "enterprise": False},
        }

        signature = RSAVerifier.create_signature(data, private_pem)
        assert signature

        assert RSAVerifier.verify_signature(data, signature, public_pem) is True

    def test_tampered_data_fails_verification(self, key_pair):
        private_pem, public_pem = key_pair
        data = {"valid": False, "license_id": 42, "expires_at": None, "features": None}
        signature = RSAVerifier.create_signature(data, private_pem)

        tampered = {**data, "valid": True}

        assert RSAVerifier.verify_signature(tampered, signature, public_pem) is False

    def test_wrong_public_key_fails_verification(self):
        private_pem_a, _ = RSAVerifier.generate_key_pair()
        _, public_pem_b = RSAVerifier.generate_key_pair()
        data = {"valid": True, "license_id": 1, "expires_at": None, "features": None}

        signature = RSAVerifier.create_signature(data, private_pem_a)

        assert RSAVerifier.verify_signature(data, signature, public_pem_b) is False

    def test_each_generated_key_pair_is_unique(self):
        _, pub1 = RSAVerifier.generate_key_pair()
        _, pub2 = RSAVerifier.generate_key_pair()
        assert pub1 != pub2


@pytest.mark.unit
class TestSignResponseHelper:

    def test_returns_signature_when_key_loaded(self, key_pair):
        private_pem, public_pem = key_pair
        signing._private_key_pem = private_pem

        data = {"valid": True, "license_id": 7, "expires_at": None, "features": None}
        signature = signing.sign_response(data)

        assert signature is not None
        assert RSAVerifier.verify_signature(data, signature, public_pem) is True

    def test_returns_none_when_no_key_loaded(self):
        signing._private_key_pem = None

        data = {"valid": True, "license_id": 1, "expires_at": None, "features": None}

        assert signing.sign_response(data) is None
