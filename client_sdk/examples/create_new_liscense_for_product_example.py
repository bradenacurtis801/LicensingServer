#!/usr/bin/env python3
"""
Create New License Key for Product Example

This example demonstrates how to:
1. Create a new license key for a specific product
2. Set up customer and application data
3. Configure license features and restrictions
4. Test activation using the LicenseClient SDK

IMPORTANT: Before running this example:
1. Make sure the license server is running on http://localhost:8999
2. The product "MyAwesomeApp" should be registered (from product_registration_example.py)
"""
import sys
import requests
import json
from pathlib import Path

# Add the root project directory to Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from client_sdk.license_client import LicenseClient, FeatureManager
from client_sdk.utils.machine_fingerprint import MachineFingerprint

def create_license_for_product():
    """Create a new license key for the MyAwesomeApp product"""
    
    base_url = "http://localhost:8999/api/v1"
    
    print("🎯 Create New License Key for MyAwesomeApp")
    print("=" * 50)
    
    # Step 1: Create or get a customer
    print("\n1️⃣ Creating customer...")
    customer_data = {
        "name": "Test Customer",
        "email": "test@example.com",
        "company": "Test Company"
    }
    
    try:
        response = requests.post(f"{base_url}/customers", json=customer_data)
        if response.status_code == 201:
            customer = response.json()
            print(f"✅ Customer created: {customer['name']} (ID: {customer['id']})")
        elif response.status_code == 200:
            customer = response.json()
            print(f"✅ Customer already exists: {customer['name']} (ID: {customer['id']})")
        else:
            print(f"❌ Failed to create customer: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error creating customer: {e}")
        return
    
    # Step 2: Get the application (MyAwesomeApp)
    print("\n2️⃣ Getting application...")
    try:
        response = requests.get(f"{base_url}/applications")
        if response.status_code == 200:
            applications = response.json()
            my_app = None
            for app in applications:
                if app['name'] == "MyAwesomeApp":
                    my_app = app
                    break
            
            if my_app:
                print(f"✅ Found application: {my_app['name']} (ID: {my_app['id']})")
            else:
                print("❌ MyAwesomeApp not found. Please run product_registration_example.py first.")
                return
        else:
            print(f"❌ Failed to get applications: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error getting applications: {e}")
        return
    
    # Step 3: Create a license key
    print("\n3️⃣ Creating license key...")
    license_data = {
        "customer_id": customer['id'],
        "application_id": my_app['id'],
        "max_activations": 1,  # Single machine license
        "expires_at": None,  # Never expires (permanent)
        "features": {
            "basic_editing": True,
            "advanced_editing": True,
            "file_export": True,
            "cloud_sync": True,
            "team_collaboration": True,
            "premium_support": True,
            "custom_themes": True,
            "api_access": True
        },
        "notes": "Test license for MyAwesomeApp - Full features"
    }
    
    try:
        response = requests.post(f"{base_url}/licenses", json=license_data)
        if response.status_code == 201:
            license_info = response.json()
            print(f"✅ License created successfully!")
            print(f"   License Key: {license_info['license_key']}")
            print(f"   Status: {license_info['status']}")
            print(f"   Max Activations: {license_info['max_activations']}")
            print(f"   Features: {license_info['features']}")
            print(f"   Notes: {license_info['notes']}")
            
            # Save the license key to a file for easy access
            with open("test_license_key.txt", "w") as f:
                f.write(license_info['license_key'])
            print(f"\n💾 License key saved to: test_license_key.txt")
            
            return license_info['license_key']
        else:
            print(f"❌ Failed to create license: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error creating license: {e}")
        return None

def test_license_activation_with_sdk(license_key: str):
    """Test the license activation using the LicenseClient SDK"""
    print(f"\n4️⃣ Testing license activation with SDK...")
    
    # Initialize the license client
    license_client = LicenseClient(
        server_url="http://localhost:8999",
        app_name="MyAwesomeApp",
        app_version="1.0.0"
    )
    
    # Generate machine fingerprint
    machine_id = MachineFingerprint.generate_fingerprint()
    print(f"   Machine ID: {machine_id}")
    
    try:
        # Validate the license (this will also activate it)
        license_info = license_client.validate_license(license_key)
        
        print(f"✅ License validated and activated successfully!")
        print(f"   Valid: {license_info.status.value}")
        print(f"   Message: {license_info.message}")
        print(f"   License ID: {license_info.license_id}")
        print(f"   Application ID: {license_info.application_id}")
        print(f"   Customer ID: {license_info.customer_id}")
        print(f"   Features: {license_info.features}")
        print(f"   Expires At: {license_info.expires_at}")
        print(f"   Remaining Activations: {license_info.remaining_activations}")
        
        # Test feature manager
        print(f"\n5️⃣ Testing Feature Manager...")
        feature_manager = FeatureManager(license_client)
        feature_manager.set_license_key(license_key)
        
        print(f"   Enabled features: {feature_manager.get_enabled_features()}")
        print(f"   Disabled features: {feature_manager.get_disabled_features()}")
        
        # Test individual features
        test_features = [
            "basic_editing", "advanced_editing", "file_export", 
            "cloud_sync", "team_collaboration", "premium_support",
            "custom_themes", "api_access"
        ]
        
        print(f"   Feature status:")
        for feature in test_features:
            enabled = feature_manager.is_feature_enabled(feature)
            status = "✅" if enabled else "❌"
            print(f"     {status} {feature}")
        
    except Exception as e:
        print(f"❌ Error validating/activating license: {e}")

def main():
    """Main function"""
    print("🚀 Create New License Key for Product Example")
    print("=" * 60)
    
    # Create the license
    # license_key = create_license_for_product()
    license_key = "DSJLH-VBMMM-BMFT9-GUWQR-MTEB1"
    
    if license_key:
        # Test the license using the SDK
        test_license_activation_with_sdk(license_key)
        
        print(f"\n✅ License creation and testing completed!")
        print(f"📋 Next steps:")
        print(f"   1. Use this license key in your application")
        print(f"   2. Test with product_registration_example.py")
        print(f"   3. Check the license key in test_license_key.txt")
    else:
        print(f"\n❌ Failed to create license key")

if __name__ == "__main__":
    main()
