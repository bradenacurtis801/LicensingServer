from unittest.mock import MagicMock, patch

import pytest

from client_sdk.license_client import LicenseClient, LicenseValidationError
from client_sdk.utils.rsa_verification import RSAVerifier


@pytest.mark.unit
def test_client_sdk_signature_verification():
    private_pem, public_pem = RSAVerifier.generate_key_pair()
    
    # Instantiate client with our test public key
    client = LicenseClient("http://localhost:8999", "TestApp", "1.0.0", public_key=public_pem)
    
    # Mock validation response dictionary
    data = {
        "valid": True,
        "license_id": 123,
        "status": "active",
        "expires_at": "2027-01-01T00:00:00+00:00",
        "features": {"premium": True},
    }
    
    # Generate signature using the private key (only on the signed fields)
    sign_data = {
        "valid": data["valid"],
        "license_id": data["license_id"],
        "expires_at": data["expires_at"],
        "features": data["features"],
    }
    signature = RSAVerifier.create_signature(sign_data, private_pem)
    
    mock_response_data = {
        **data,
        "signature": signature
    }
    
    with patch("requests.post") as mock_post:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_response_data
        mock_post.return_value = mock_resp
        
        # This should succeed since signature matches
        license_info = client.validate_license("AAAAA-BBBBB-CCCCC-DDDDD-EEEEE")
        assert license_info.license_id == 123
        assert license_info.features["premium"] is True
        
        # Now mock a tampered response where features are modified
        tampered_response_data = {
            **mock_response_data,
            "features": {"premium": False}
        }
        mock_resp.json.return_value = tampered_response_data
        
        # This should raise LicenseValidationError
        with pytest.raises(LicenseValidationError, match="License response signature verification failed"):
            client.validate_license("AAAAA-BBBBB-CCCCC-DDDDD-EEEEE", force_refresh=True)
