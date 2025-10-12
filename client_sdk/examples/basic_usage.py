"""Basic usage examples for the License Client SDK"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from client_sdk.license_client import LicenseClient

def basic_validation_example():
    """Example of basic license validation"""
    print("Basic License Validation Example")
    print("=" * 40)

    # Initialize client
    client = LicenseClient("http://localhost:8999")
    
    # Example license key (replace with actual key from sample data)
    license_key = "ABCDE-FGHIJ-KLMNO-PQRST-UVWXY"
    
    print(f"Validating license: {license_key}")
    print(f"Machine ID: {client.get_machine_id()}")
    
    # Validate license
    result = client.validate_license(license_key)
    
    print(f"\nValidation Result:")
    print(f"Valid: {result.get('valid', False)}")
    print(f"Message: {result.get('message', 'No message')}")
    
    if result.get('valid'):
        print(f"License ID: {result.get('license_id')}")
        print(f"Customer ID: {result.get('customer_id')}")
        print(f"Application ID: {result.get('application_id')}")
        print(f"Expires: {result.get('expires_at', 'Never')}")
        print(f"Remaining Activations: {result.get('remaining_activations')}")

        features = result.get('features', {})
        if features:
            print("Features:")
            for feature, enabled in features.items():
                status = "✅ Enabled" if enabled else "❌ Disabled"
                print(f"  {status} {feature}")

def feature_checking_example():
    """Example of checking specific features"""
    print("Feature Checking Example")
    print("=" * 40)

    client = LicenseClient("http://localhost:8999")
    license_key = "ABCDE-FGHIJ-KLMNO-PQRST-UVWXY"
    
    # Check if license has specific features
    features_to_check = [
        "basic_features",
        "advanced_features",
        "premium_support",
        "code_editor",
        "debugger"
    ]
    
    print(f"Checking features for license: {license_key}")
    for feature in features_to_check:
        has_feature = client.has_feature(license_key, feature)
        status = "✅ Enabled" if has_feature else "❌ Disabled"
        print(f"  {status}: {feature}")

def error_handling_example():
    """Example of handling various error scenarios"""
    print("Error Handling Example")
    print("=" * 40)

    client = LicenseClient("http://localhost:8999")
    
    # Test with invalid license key
    invalid_keys = [
        "INVALID-KEY-FORMAT",
        "12345-67890-ABCDE-FGHIJ-KLMNO",  # Invalid format
        "AAAAA-BBBBB-CCCCC-DDDDD-EEEEE",  # Valid format but doesn't exist
    ]
    
    for key in invalid_keys:
        print(f"\nTesting invalid key: {key}")
        result = client.validate_license(key)
        print(f"Valid: {result.get('valid', False)}")
        print(f"Message: {result.get('message', 'No message')}")
    
if __name__ == "__main__":
    print("License Client SDK Examples")
    print("=" * 50)
    print("Make sure the license server is running on http://localhost:8999")
    print("Run 'python scripts/create_sample_data.py' first to create test data")
    print()

    try:
        basic_validation_example()
        feature_checking_example()
        error_handling_example()
    except Exception as e:
        print(f"\nError: {e}")