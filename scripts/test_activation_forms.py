#!/usr/bin/env python3
"""
Test Activation Forms - Complete Workflow
"""
import sys
import os
import requests
import json
import time

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client_sdk.utils.machine_fingerprint import MachineFingerprint

# Configuration
BASE_URL = "http://localhost:8999/api/v1"
TEST_LICENSE_KEY = "ALKZV-EUHQC-AGSCZ-5LNKA-2NUFY"  # From sample data

def test_activation_forms_workflow():
    """Test the complete activation forms workflow"""
    print("🔐 Activation Forms Test - Complete Workflow")
    print("=" * 60)
    
    # Step 1: Generate machine fingerprint
    machine_id = MachineFingerprint.generate_fingerprint()
    print(f"📱 Machine ID: {machine_id}")
    print()
    
    # Step 2: Create activation form request (offline computer)
    print("Step 1: Creating Activation Form Request (Offline Computer)")
    print("-" * 50)
    
    form_data = {
        "license_key": TEST_LICENSE_KEY,
        "machine_id": machine_id,
        "machine_name": "Test Machine - Offline"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/activation-forms/",
            json=form_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            form = response.json()
            request_code = form["request_code"]
            print(f"✅ Activation form created successfully!")
            print(f"📋 Request Code: {request_code}")
            print(f"🆔 Form ID: {form['id']}")
            print(f"⏰ Expires: {form['expires_at']}")
            print()
            
            # Step 3: Generate offline activation codes (admin/server)
            print("Step 2: Generating Offline Activation Codes (Admin/Server)")
            print("-" * 50)
            
            offline_codes_data = {
                "license_key_id": 1,  # Assuming license ID 1
                "machine_id": machine_id,
                "quantity": 3
            }
            
            offline_response = requests.post(
                f"{BASE_URL}/activation-forms/offline-codes",
                json=offline_codes_data,
                headers={"Content-Type": "application/json"}
            )
            
            if offline_response.status_code == 200:
                offline_codes = offline_response.json()
                print(f"✅ Generated {len(offline_codes)} offline activation codes:")
                for i, code in enumerate(offline_codes, 1):
                    print(f"   {i}. {code['activation_code']}")
                print()
                
                # Step 4: Complete activation form (offline computer)
                print("Step 3: Completing Activation Form (Offline Computer)")
                print("-" * 50)
                
                # Use the first activation code
                activation_code = offline_codes[0]["activation_code"]
                
                complete_data = {
                    "request_code": request_code,
                    "activation_code": activation_code
                }
                
                complete_response = requests.post(
                    f"{BASE_URL}/activation-forms/complete",
                    json=complete_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if complete_response.status_code == 200:
                    completed_form = complete_response.json()
                    print(f"✅ Activation completed successfully!")
                    print(f"📋 Form ID: {completed_form['id']}")
                    print(f"✅ Status: {completed_form['status']}")
                    print(f"⏰ Completed: {completed_form['completed_at']}")
                    print()
                    
                    # Step 5: Verify activation
                    print("Step 4: Verifying Activation")
                    print("-" * 50)
                    
                    verify_data = {
                        "license_key": TEST_LICENSE_KEY,
                        "machine_id": machine_id
                    }
                    
                    verify_response = requests.post(
                        f"{BASE_URL}/validate/license",
                        json=verify_data,
                        headers={"Content-Type": "application/json"}
                    )
                    
                    if verify_response.status_code == 200:
                        verification = verify_response.json()
                        print(f"✅ License validation successful!")
                        print(f"🔑 License ID: {verification['license_id']}")
                        print(f"✅ Valid: {verification['valid']}")
                        print(f"👤 Customer ID: {verification['customer_id']}")
                        print(f"📱 Application ID: {verification['application_id']}")
                        print(f"📊 Remaining Activations: {verification['remaining_activations']}")
                    else:
                        print(f"❌ License validation failed: {verify_response.text}")
                        
                else:
                    print(f"❌ Activation completion failed: {complete_response.text}")
                    
            else:
                print(f"❌ Offline code generation failed: {offline_response.text}")
                
        else:
            print(f"❌ Activation form creation failed: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the server is running on http://localhost:8999")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_error_scenarios():
    """Test various error scenarios"""
    print("\n🧪 Testing Error Scenarios")
    print("=" * 60)
    
    machine_id = MachineFingerprint.generate_fingerprint()
    
    # Test 1: Invalid license key
    print("Test 1: Invalid License Key")
    print("-" * 30)
    
    try:
        response = requests.post(
            f"{BASE_URL}/activation-forms/",
            json={
                "license_key": "INVALID-KEY-HERE",
                "machine_id": machine_id,
                "machine_name": "Test Machine"
            },
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        print()
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Invalid request code
    print("Test 2: Invalid Request Code")
    print("-" * 30)
    
    try:
        response = requests.post(
            f"{BASE_URL}/activation-forms/complete",
            json={
                "request_code": "INVALID-REQUEST-CODE",
                "activation_code": "INVALID-ACTIVATION-CODE"
            },
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        print()
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Expired activation form
    print("Test 3: Expired Activation Form")
    print("-" * 30)
    print("(This would require manual database manipulation to test)")
    print()

def show_usage_examples():
    """Show how clients would use activation forms"""
    print("\n📖 Client Usage Examples")
    print("=" * 60)
    
    print("""
🔧 Developer Workflow:

1. OFFLINE COMPUTER (Client):
   - User has no internet access
   - Application generates machine fingerprint
   - Application creates activation form request
   - Application displays request code to user
   - User manually transfers request code to online computer

2. ONLINE COMPUTER (Admin/Server):
   - Admin receives request code from user
   - Admin generates offline activation codes
   - Admin provides activation code to user

3. OFFLINE COMPUTER (Client):
   - User enters activation code in application
   - Application completes activation form
   - Application validates license locally

📱 Example Client Implementation:

```python
# Step 1: Create activation form request
def create_activation_request(license_key, machine_id):
    response = requests.post(
        "https://your-license-server.com/api/v1/activation-forms/",
        json={
            "license_key": license_key,
            "machine_id": machine_id,
            "machine_name": "My Computer"
        }
    )
    return response.json()["request_code"]

# Step 2: Complete activation with code
def complete_activation(request_code, activation_code):
    response = requests.post(
        "https://your-license-server.com/api/v1/activation-forms/complete",
        json={
            "request_code": request_code,
            "activation_code": activation_code
        }
    )
    return response.json()

# Step 3: Validate license
def validate_license(license_key, machine_id):
    response = requests.post(
        "https://your-license-server.com/api/v1/validate/license",
        json={
            "license_key": license_key,
            "machine_id": machine_id
        }
    )
    return response.json()
```

🔄 Offline Activation Process:

1. User opens application on offline computer
2. Application generates machine fingerprint
3. Application creates activation form request
4. Application displays request code (e.g., "ABC123DEF456")
5. User writes down request code
6. User goes to online computer
7. User provides request code to admin
8. Admin generates activation code
9. User returns to offline computer
10. User enters activation code in application
11. Application completes activation
12. Application validates license successfully

💡 Benefits:
- Works without internet connection
- Secure machine fingerprinting
- Prevents license sharing
- Supports air-gapped environments
- Maintains activation limits
""")

def main():
    """Main test function"""
    print("🚀 Activation Forms Testing Suite")
    print("=" * 60)
    
    # Test the complete workflow
    test_activation_forms_workflow()
    
    # Test error scenarios
    test_error_scenarios()
    
    # Show usage examples
    show_usage_examples()
    
    print("\n✅ Testing complete!")
    print("\n📝 Next Steps:")
    print("1. Start the server: python run_server.py")
    print("2. Run this test: python scripts/test_activation_forms.py")
    print("3. Test on different machines to verify fingerprinting")
    print("4. Test error scenarios and edge cases")

if __name__ == "__main__":
    main() 