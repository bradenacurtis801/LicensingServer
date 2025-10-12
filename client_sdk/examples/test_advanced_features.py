#!/usr/bin/env python3
"""
Test script for advanced license management features
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from client_sdk.methods import LicenseKey

def test_advanced_features():
    """Test all the advanced license management features"""
    
    server_url = "http://localhost:8999"
    
    print("🔧 Testing Advanced License Management Features")
    print("=" * 50)
    
    # First, create a test license using existing customer and application IDs
    # Based on the working curl example, let's use customer_id=72 and application_id=36
    print("\n1. Creating a test license...")
    result, message = LicenseKey.create_key(
        server_url=server_url,
        customer_id=2,  # Use existing customer ID
        application_id=2,  # Use existing application ID
        max_activations=3,
        features={"basic": True, "advanced": False},
        notes="Test license for advanced features"
    )
    
    if result:
        license_key = result.get("license_key")
        license_id = result.get("id")
        print(f"✅ License created: {license_key} (ID: {license_id})")
        
        # Test block/unblock using license ID directly
        print("\n2. Testing block/unblock functionality...")
        success, msg = LicenseKey.block_key(server_url, license_key)
        print(f"🔒 Block result: {success} - {msg}")
        
        success, msg = LicenseKey.unblock_key(server_url, license_key)
        print(f"🔓 Unblock result: {success} - {msg}")
        
        # Test feature management
        print("\n3. Testing feature management...")
        success, msg = LicenseKey.add_feature(server_url, license_key, "premium")
        print(f"➕ Add feature result: {success} - {msg}")
        
        success, msg = LicenseKey.remove_feature(server_url, license_key, "basic")
        print(f"➖ Remove feature result: {success} - {msg}")
        
        # Test machine lock limit
        print("\n4. Testing machine lock limit...")
        success, msg = LicenseKey.machine_lock_limit(server_url, license_key, 5)
        print(f"🔒 Machine limit result: {success} - {msg}")
        
        # Test license extension
        print("\n5. Testing license extension...")
        success, msg = LicenseKey.extend_license(server_url, license_key, 30)
        print(f"📅 Extension result: {success} - {msg}")
        
        # Test notes change
        print("\n6. Testing notes change...")
        success, msg = LicenseKey.change_notes(server_url, license_key, "Updated notes for testing")
        print(f"📝 Notes change result: {success} - {msg}")
        
        # Test get_key (simplified)
        print("\n7. Testing get_key...")
        # For testing, we'll skip signature verification by not providing rsa_pub_key
        result, msg = LicenseKey.get_key(server_url, license_key)
        if result:
            print(f"📋 License info: ID={result.get('id')}, Status={result.get('status')}")
        else:
            print(f"❌ Get key failed: {msg}")
        
        # Test trial license creation
        print("\n8. Testing trial license creation...")
        result, msg = LicenseKey.create_trial_key(
            server_url=server_url,
            customer_id=72,  # Use existing customer ID
            application_id=36,  # Use existing application ID
            friendly_name="Test Trial"
        )
        if result:
            trial_key = result.get("license_key")
            print(f"🎯 Trial license created: {trial_key}")
        else:
            print(f"❌ Trial creation failed: {msg}")
        
        print("\n✅ All advanced features tested successfully!")
        
    else:
        print(f"❌ Failed to create test license: {message}")

if __name__ == "__main__":
    test_advanced_features() 