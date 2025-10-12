#!/usr/bin/env python3
"""
Authentication Example with User Ownership

This example demonstrates:
1. User registration and login
2. Role-based access control
3. API token creation with specific scopes
4. User ownership of resources (customers, applications, licenses)
5. Cross-user resource isolation

IMPORTANT: Before running this example:
1. Run: python scripts/setup_auth_database.py
2. Start the server: python run_server.py
3. Install required packages: pip install python-jose[cryptography] passlib[bcrypt]
"""
import sys
import requests
import json
import time
from pathlib import Path

# Add the root project directory to Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

def login_user(username: str, password: str):
    """Login a user and get session token"""
    base_url = "http://localhost:8999/api/v1/auth"
    
    login_data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(f"{base_url}/login", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            print(f"✅ {username} logged in successfully")
            return token_data["session_token"]
        else:
            print(f"❌ Login failed for {username}: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error logging in {username}: {e}")
        return None

def create_api_token(token_name: str, scopes: list, session_token: str):
    """Create an API token with specific scopes"""
    base_url = "http://localhost:8999/api/v1/auth"
    
    token_data = {
        "name": token_name,
        "scopes": scopes,
        "expires_at": None  # No expiration
    }
    
    headers = {"Authorization": f"Bearer {session_token}"}
    
    try:
        response = requests.post(f"{base_url}/tokens", json=token_data, headers=headers)
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Created API token: {result['name']}")
            return result["token"]
        else:
            print(f"❌ Failed to create API token: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error creating API token: {e}")
        return None

def test_user_ownership():
    """Test that users can only access their own resources"""
    print("\n🏠 Testing User Ownership")
    print("=" * 50)
    
    # Login as different users
    admin_token = login_user("admin", "admin123")
    john_token = login_user("john", "john12345")
    
    if not admin_token or not john_token:
        print("❌ Failed to login users")
        return
    
    # Test with session tokens (should work now!)
    print("\n🔑 Testing with Session Tokens...")
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    john_headers = {"Authorization": f"Bearer {john_token}"}
    
    # Create resources as admin using session token
    print("\n👑 Admin creating resources with session token...")
    
    # Create customer as admin
    import time
    timestamp = int(time.time())
    customer_data = {
        "name": "Admin Customer",
        "email": f"admin{timestamp}@customer.com",
        "company": "Admin Corp"
    }
    response = requests.post("http://localhost:8999/api/v1/customers", 
                           json=customer_data, headers=admin_headers)
    if response.status_code == 201:
        admin_customer = response.json()
        print(f"✅ Admin created customer: {admin_customer['name']}")
    else:
        print(f"❌ Admin failed to create customer: {response.text}")
        return
    
    # Create application as admin
    app_data = {
        "name": f"Admin App {timestamp}",
        "version": "1.0.0",
        "description": "Admin's application"
    }
    response = requests.post("http://localhost:8999/api/v1/applications", 
                           json=app_data, headers=admin_headers)
    if response.status_code == 201:
        admin_app = response.json()
        print(f"✅ Admin created application: {admin_app['name']}")
    else:
        print(f"❌ Admin failed to create application: {response.text}")
        return
    
    # Create license as admin
    license_data = {
        "customer_id": admin_customer["id"],
        "application_id": admin_app["id"],
        "max_activations": 5
    }
    response = requests.post("http://localhost:8999/api/v1/licenses", 
                           json=license_data, headers=admin_headers)
    if response.status_code == 201:
        admin_license = response.json()
        print(f"✅ Admin created license: {admin_license['id']}")
    else:
        print(f"❌ Admin failed to create license: {response.text}")
        return
    
    # Try to access admin's resources as john using session token
    print("\n👨‍💻 John trying to access admin's resources with session token...")
    
    # Try to get admin's customer
    response = requests.get(f"http://localhost:8999/api/v1/customers/{admin_customer['id']}", 
                          headers=john_headers)
    if response.status_code == 404:
        print("✅ John correctly cannot access admin's customer")
    else:
        print(f"❌ John incorrectly accessed admin's customer: {response.status_code}")
    
    # Try to get admin's application
    response = requests.get(f"http://localhost:8999/api/v1/applications/{admin_app['id']}", 
                          headers=john_headers)
    if response.status_code == 404:
        print("✅ John correctly cannot access admin's application")
    else:
        print(f"❌ John incorrectly accessed admin's application: {response.status_code}")
    
    # Try to get admin's license
    response = requests.get(f"http://localhost:8999/api/v1/licenses/{admin_license['id']}", 
                          headers=john_headers)
    if response.status_code == 404:
        print("✅ John correctly cannot access admin's license")
    else:
        print(f"❌ John incorrectly accessed admin's license: {response.status_code}")
    
    # Test with API tokens (should also work)
    print("\n🔑 Testing with API Tokens...")
    
    # Create API tokens for users
    admin_api_token = create_api_token(
        "Admin Full Access",
        ["customer:read", "customer:write", "customer:delete", 
         "application:read", "application:write", "application:delete",
         "license:read", "license:write", "license:delete"],
        admin_token
    )
    
    john_api_token = create_api_token(
        "John's Access",
        ["customer:read", "customer:write", 
         "application:read", "application:write",
         "license:read", "license:write"],
        john_token
    )
    
    if admin_api_token and john_api_token:
        print("✅ API tokens created successfully")
        
        # Test API token access
        admin_api_headers = {"Authorization": f"Bearer {admin_api_token}"}
        john_api_headers = {"Authorization": f"Bearer {john_api_token}"}
        
        # Test that API tokens work the same way
        response = requests.get("http://localhost:8999/api/v1/customers", headers=admin_api_headers)
        if response.status_code == 200:
            print("✅ Admin API token can access customers")
        else:
            print(f"❌ Admin API token cannot access customers: {response.status_code}")
    else:
        print("❌ Failed to create API tokens for testing")

def test_role_based_permissions():
    """Test role-based permissions"""
    print("\n🔐 Testing Role-Based Permissions")
    print("=" * 50)
    
    # Generate timestamp for unique test data
    timestamp = int(time.time())
    
    # Login as different users
    admin_token = login_user("admin", "admin123")
    john_token = login_user("john", "john12345")
    sarah_token = login_user("sarah", "sarah12345")
    
    if not all([admin_token, john_token, sarah_token]):
        print("❌ Failed to login users")
        return
    
    # Test with session tokens (should work now!)
    print("\n🔑 Testing with Session Tokens...")
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    john_headers = {"Authorization": f"Bearer {john_token}"}
    sarah_headers = {"Authorization": f"Bearer {sarah_token}"}
    
    # Test admin permissions with session token
    print("\n👑 Testing Admin Permissions with Session Token...")
    
    # Admin should be able to create users
    response = requests.post("http://localhost:8999/api/v1/auth/users", 
                           json={"username": f"test{timestamp}", "email": f"test{timestamp}@test.com", 
                                "full_name": "Test User", "password": "test123456"}, 
                           headers=admin_headers)
    if response.status_code == 201:
        print("✅ Admin can create users with session token")
    else:
        print(f"❌ Admin cannot create users with session token: {response.status_code}")
        print(f"   Error details: {response.text}")
    
    # Test regular user permissions with session token
    print("\n👤 Testing Regular User Permissions with Session Token...")
    
    # Regular user should be able to create customers
    import time
    timestamp = int(time.time())
    customer_data = {"name": "John's Customer", "email": f"john{timestamp}@customer.com"}
    response = requests.post("http://localhost:8999/api/v1/customers", 
                           json=customer_data, headers=john_headers)
    if response.status_code == 201:
        print("✅ John can create customers with session token")
    else:
        print(f"❌ John cannot create customers with session token: {response.status_code}")
    
    # Regular user should NOT be able to create users
    response = requests.post("http://localhost:8999/api/v1/auth/users", 
                           json={"username": f"test2{timestamp}", "email": f"test2{timestamp}@test.com", 
                                "full_name": "Test User 2", "password": "test123456"}, 
                           headers=john_headers)
    if response.status_code == 403:
        print("✅ John correctly cannot create users with session token")
    else:
        print(f"❌ John incorrectly can create users with session token: {response.status_code}")
    
    # Test another regular user with session token
    print("\n👤 Testing Another Regular User with Session Token...")
    
    # Sarah should be able to read customers
    response = requests.get("http://localhost:8999/api/v1/customers", headers=sarah_headers)
    if response.status_code == 200:
        print("✅ Sarah can read customers with session token")
    else:
        print(f"❌ Sarah cannot read customers with session token: {response.status_code}")
    
    # Sarah should be able to create customers  
    timestamp = int(time.time()) + 1  # Ensure unique timestamp
    customer_data = {"name": "Sarah's Customer", "email": f"sarah{timestamp}@customer.com"}
    response = requests.post("http://localhost:8999/api/v1/customers", 
                           json=customer_data, headers=sarah_headers)
    if response.status_code == 201:
        print("✅ Sarah can create customers with session token")
    else:
        print(f"❌ Sarah cannot create customers with session token: {response.status_code}")

def test_api_tokens():
    """Test API token functionality"""
    print("\n🔑 Testing API Tokens")
    print("=" * 50)
    
    # Login as admin
    admin_token = login_user("admin", "admin123")
    if not admin_token:
        print("❌ Failed to login admin")
        return
    
    # Create API token with specific scopes
    print("\n🔧 Creating API token with limited scopes...")
    api_token = create_api_token(
        "Test API Token",
        ["customer:read", "application:read", "license:read"],
        admin_token
    )
    
    if not api_token:
        print("❌ Failed to create API token")
        return
    
    # Test API token permissions
    print("\n🧪 Testing API token permissions...")
    api_headers = {"Authorization": f"Bearer {api_token}"}
    
    # Should be able to read customers
    response = requests.get("http://localhost:8999/api/v1/customers", headers=api_headers)
    if response.status_code == 200:
        print("✅ API token can read customers")
    else:
        print(f"❌ API token cannot read customers: {response.status_code}")
    
    # Should NOT be able to create customers
    timestamp = int(time.time()) + 2  # Ensure unique timestamp
    customer_data = {"name": "API Customer", "email": f"api{timestamp}@customer.com"}
    response = requests.post("http://localhost:8999/api/v1/customers", 
                           json=customer_data, headers=api_headers)
    if response.status_code == 403:
        print("✅ API token correctly cannot create customers")
    else:
        print(f"❌ API token incorrectly can create customers: {response.status_code}")

def demonstrate_usage():
    """Demonstrate practical usage scenarios"""
    print("\n🎯 Practical Usage Scenarios")
    print("=" * 50)
    
    print("\n1️⃣ Multi-tenant Architecture:")
    print("   - Each user owns their customers, applications, and licenses")
    print("   - Users cannot access other users' resources")
    print("   - Perfect for SaaS applications")
    
    print("\n2️⃣ Role-Based Access Control:")
    print("   - System Admin: Full access to everything")
    print("   - Regular User: Can manage their own resources")
    print("   - Business roles determine resource access")
    
    print("\n3️⃣ API Token Benefits:")
    print("   - Long-lived tokens for automated systems")
    print("   - Granular permissions per token")
    print("   - Can be revoked individually")
    print("   - Better security than shared credentials")
    
    print("\n4️⃣ Security Features:")
    print("   - Password hashing with bcrypt")
    print("   - Session tokens with expiration")
    print("   - Resource ownership validation")
    print("   - Scope-based permissions")

def main():
    """Main function"""
    print("🚀 Authentication System Example")
    print("=" * 60)
    
    # Test user ownership
    test_user_ownership()
    
    # Test role-based permissions
    test_role_based_permissions()
    
    # Test API tokens
    test_api_tokens()
    
    # Show usage scenarios
    demonstrate_usage()
    
    print(f"\n✅ Authentication example completed!")
    print(f"📋 Key Features Demonstrated:")
    print(f"   ✅ User ownership of resources")
    print(f"   ✅ Role-based access control")
    print(f"   ✅ API tokens with scopes")
    print(f"   ✅ Cross-user resource isolation")
    print(f"   ✅ Secure authentication flow")

if __name__ == "__main__":
    main() 