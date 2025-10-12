#!/usr/bin/env python3
"""
Role-Based Authentication Example

This example demonstrates:
1. User registration with default roles
2. Role management by administrators
3. API token creation with different scopes
4. Scope-based access control
"""
import requests
import json
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.utils.test_users import get_test_users_for_registration, get_test_user_credentials

# Configuration
base_url = "http://localhost:8999"
api_url = f"{base_url}/api/v1"

def authenticate_user(username: str, password: str) -> str:
    """Authenticate user and return session token"""
    response = requests.post(
        f"{api_url}/auth/login",
        json={"username": username, "password": password}
    )
    
    if response.status_code == 200:
        data = response.json()
        return data["session_token"]
    else:
        raise Exception(f"Authentication failed: {response.status_code} - {response.text}")

def register_users():
    """Register users with basic info (no role specified)"""
    print("👥 Registering Users")
    print("=" * 50)
    
    # Get test users from configuration
    users = get_test_users_for_registration()
    
    # Filter out admin (already exists) and testuser (created during testing)
    registration_users = [user for user in users if user["username"] not in ["admin", "testuser"]]
    
    created_users = {}
    
    for user_data in registration_users:
        try:
            response = requests.post(
                f"{api_url}/auth/register",
                json=user_data
            )
            
            if response.status_code == 201:
                user = response.json()
                created_users[user_data["username"]] = user
                print(f"✅ User '{user['username']}' registered successfully")
                print(f"   User ID: {user['id']}")
                print(f"   Email: {user['email']}")
                print(f"   Business Role: {user['business_role']}")
                print(f"   System Role: {user['system_role']}")
                print()
            else:
                print(f"❌ Failed to register user '{user_data['username']}': {response.status_code}")
                print(f"   Error: {response.text}")
                print()
                
        except Exception as e:
            print(f"❌ Error registering user '{user_data['username']}': {e}")
            print()
    
    return created_users

def create_api_tokens_for_users(users: dict):
    """Create API tokens for different users"""
    print("🔑 Creating API Tokens")
    print("=" * 50)
    
    # Get admin credentials for token creation
    admin_credentials = get_test_user_credentials("admin")
    if not admin_credentials:
        print("❌ Admin credentials not found")
        return
    
    username, password = admin_credentials
    admin_token = authenticate_user(username, password)
    
    for username, user in users.items():
        try:
            # Create token with different scopes based on user
            if username == "john":
                scopes = ["license:read", "license:write"]
                token_name = "John's License Token"
            elif username == "sarah":
                scopes = ["application:read", "application:write"]
                token_name = "Sarah's Application Token"
            elif username == "mike":
                scopes = ["activation:read", "activation:delete"]
                token_name = "Mike's Activation Token"
            else:
                scopes = ["license:read"]
                token_name = f"{username}'s Basic Token"
            
            response = requests.post(
                f"{api_url}/auth/tokens",
                json={
                    "name": token_name,
                    "scopes": scopes,
                    "expires_at": None
                },
                headers={"Authorization": f"Bearer {admin_token}"}
            )
            
            if response.status_code == 201:
                result = response.json()
                print(f"✅ Created API token for {username}: {result['name']}")
                print(f"   Scopes: {', '.join(scopes)}")
                print(f"   Token ID: {result['id']}")
                print()
            else:
                print(f"❌ Failed to create API token for {username}: {response.text}")
                print()
                
        except Exception as e:
            print(f"❌ Error creating token for {username}: {e}")
            print()

def demonstrate_role_management():
    """Demonstrate role management by administrators"""
    print("👨‍💼 Role Management by Admin")
    print("=" * 50)
    
    # Get admin credentials
    admin_credentials = get_test_user_credentials("admin")
    if not admin_credentials:
        print("❌ Admin credentials not found")
        return
    
    username, password = admin_credentials
    admin_token = authenticate_user(username, password)
    
    print("ℹ️  Admin capabilities:")
    print("   - Can view all users")
    print("   - Can update user business roles")
    print("   - Can update user system roles")
    print("   - Can create API tokens for other users")
    print()
    
    # List all users
    try:
        response = requests.get(
            f"{api_url}/auth/users",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        if response.status_code == 200:
            users = response.json()
            print(f"📋 Total users in system: {len(users)}")
            for user in users:
                print(f"   👤 {user['username']} ({user['business_role']} / {user['system_role']})")
            print()
        else:
            print(f"❌ Failed to list users: {response.status_code}")
            print()
            
    except Exception as e:
        print(f"❌ Error listing users: {e}")
        print()

def demonstrate_scope_based_access():
    """Demonstrate scope-based access control"""
    print("🔐 Scope-Based Access Control")
    print("=" * 50)
    
    # Get admin credentials to create tokens
    admin_credentials = get_test_user_credentials("admin")
    if not admin_credentials:
        print("❌ Admin credentials not found")
        return
    
    username, password = admin_credentials
    admin_token = authenticate_user(username, password)
    
    # Create tokens with different scopes
    tokens = {
        "license_read": {
            "name": "License Read Token",
            "scopes": ["license:read"]
        },
        "license_full": {
            "name": "License Full Token", 
            "scopes": ["license:read", "license:write", "license:delete"]
        },
        "application_token": {
            "name": "Application Token",
            "scopes": ["application:read", "application:write"]
        }
    }
    
    created_tokens = {}
    
    for token_name, token_data in tokens.items():
        try:
            response = requests.post(
                f"{api_url}/auth/tokens",
                json=token_data,
                headers={"Authorization": f"Bearer {admin_token}"}
            )
            
            if response.status_code == 201:
                result = response.json()
                created_tokens[token_name] = result["token"]
                print(f"✅ Created {token_data['name']}")
                print(f"   Scopes: {', '.join(token_data['scopes'])}")
                print()
            else:
                print(f"❌ Failed to create {token_data['name']}: {response.text}")
                print()
                
        except Exception as e:
            print(f"❌ Error creating {token_data['name']}: {e}")
            print()
    
    # Test scope-based access
    if "license_read" in created_tokens:
        token = created_tokens["license_read"]
        
        # Test license read access (should work)
        response = requests.get(
            f"{api_url}/licenses/",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            print("✅ License read token can access licenses")
        else:
            print(f"❌ License read token cannot access licenses: {response.status_code}")
        
        # Test license write access (should fail)
        response = requests.post(
            f"{api_url}/licenses/",
            json={"customer_id": 1, "application_id": 1, "max_activations": 5},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 403:
            print("✅ License read token correctly denied write access")
        else:
            print(f"❌ License read token incorrectly allowed write access: {response.status_code}")
        
        print()
    
    # Test full license token
    if "license_full" in created_tokens:
        token = created_tokens["license_full"]
        
        # Test license write access (should work)
        response = requests.post(
            f"{api_url}/licenses/",
            json={"customer_id": 1, "application_id": 1, "max_activations": 5},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 201:
            print("✅ License full token can create licenses")
        else:
            print(f"❌ License full token cannot create licenses: {response.status_code}")
        
        print()

def main():
    """Main example function"""
    print("🎯 Role-Based Authentication Example")
    print("=" * 60)
    print()
    
    try:
        # Register users
        created_users = register_users()
        
        # Create API tokens
        create_api_tokens_for_users(created_users)
        
        # Demonstrate role management
        demonstrate_role_management()
        
        # Demonstrate scope-based access
        demonstrate_scope_based_access()
        
        print("🎉 Example completed successfully!")
        print()
        print("📋 Summary:")
        print("   ✅ Users registered with default roles")
        print("   ✅ API tokens created with different scopes")
        print("   ✅ Role management demonstrated")
        print("   ✅ Scope-based access control tested")
        
    except Exception as e:
        print(f"❌ Example failed: {e}")

if __name__ == "__main__":
    main() 