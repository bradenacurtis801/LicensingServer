#!/usr/bin/env python3
"""
Test Token Scopes Feature

This script tests the token scopes functionality including:
- API token creation with different scopes
- Scope-based access control
- Endpoint permissions
- Error handling for insufficient permissions
"""
import requests
import json
import logging
import time
from typing import Dict, List, Optional

# Add the project root to Python path
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from app.utils.test_users import get_test_user_credentials, get_test_user

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class TokenScopesTester:
    def __init__(self, base_url: str = "http://localhost:8999"):
        self.base_url = base_url.rstrip('/')
        self.api_url = f"{self.base_url}/api/v1"
        self.test_tokens = {}  # Store created tokens for cleanup
        self.test_applications = []  # Store created applications for cleanup
        
    def log_section(self, title: str):
        """Log a section header"""
        logger.info("")
        logger.info("=" * 60)
        logger.info(f" {title}")
        logger.info("=" * 60)
    
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"{status} {test_name}")
        if details:
            logger.info(f"   Details: {details}")
    
    def authenticate_user(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and return session token"""
        try:
            response = requests.post(
                f"{self.api_url}/auth/login",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("session_token")
            else:
                logger.error(f"Login failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return None
    
    def create_api_token(self, session_token: str, name: str, scopes: List[str]) -> Optional[str]:
        """Create API token with specified scopes"""
        try:
            headers = {"Authorization": f"Bearer {session_token}"}
            
            response = requests.post(
                f"{self.api_url}/auth/tokens",
                json={
                    "name": name,
                    "scopes": scopes,
                    "expires_at": None
                },
                headers=headers
            )
            
            if response.status_code == 201:
                data = response.json()
                token = data.get("token")
                token_id = data.get("id")
                
                # Store for cleanup
                self.test_tokens[token_id] = {
                    "name": name,
                    "scopes": scopes,
                    "session_token": session_token
                }
                
                logger.info(f"Created API token '{name}' with scopes: {scopes}")
                return token
            else:
                logger.error(f"Token creation failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Token creation error: {e}")
            return None
    
    def test_endpoint_with_token(self, endpoint: str, method: str = "GET", 
                                token: Optional[str] = None, 
                                expected_status: int = 200,
                                data: Optional[Dict] = None) -> bool:
        """Test an endpoint with a token and verify response"""
        try:
            headers = {}
            if token:
                headers["Authorization"] = f"Bearer {token}"
            
            if method == "GET":
                response = requests.get(f"{self.api_url}{endpoint}", headers=headers)
            elif method == "POST":
                response = requests.post(f"{self.api_url}{endpoint}", json=data, headers=headers)
            elif method == "PUT":
                response = requests.put(f"{self.api_url}{endpoint}", json=data, headers=headers)
            elif method == "DELETE":
                response = requests.delete(f"{self.api_url}{endpoint}", headers=headers)
            else:
                logger.error(f"Unsupported method: {method}")
                return False
            
            # Handle multiple expected status codes
            if isinstance(expected_status, list):
                success = response.status_code in expected_status
            else:
                success = response.status_code == expected_status
            
            if not success:
                logger.warning(f"Expected {expected_status}, got {response.status_code}")
                logger.warning(f"Response: {response.text}")
            
            return success
            
        except Exception as e:
            logger.error(f"Request error: {e}")
            return False

    def test_application_creation(self, token: str, app_data: Dict) -> tuple[bool, Optional[Dict]]:
        """Test application creation and return success status and response data"""
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(f"{self.api_url}/applications/", json=app_data, headers=headers)
            
            success = response.status_code == 201
            if not success:
                logger.warning(f"Expected 201, got {response.status_code}")
                logger.warning(f"Response: {response.text}")
                return False, None
            
            return True, response.json()
            
        except Exception as e:
            logger.error(f"Request error: {e}")
            return False, None
    
    def cleanup_applications(self):
        """Clean up created test applications"""
        if not self.test_applications:
            return
            
        logger.info("Cleaning up test applications...")
        
        # Get admin token for cleanup
        admin_credentials = get_test_user_credentials("admin")
        if admin_credentials:
            username, password = admin_credentials
            admin_token = self.authenticate_user(username, password)
            
            if admin_token:
                for app_id in self.test_applications:
                    try:
                        headers = {"Authorization": f"Bearer {admin_token}"}
                        response = requests.delete(f"{self.api_url}/applications/{app_id}", headers=headers)
                        
                        if response.status_code in [200, 204]:
                            logger.info(f"Deleted application: {app_id}")
                        else:
                            logger.warning(f"Failed to delete application {app_id}: {response.status_code}")
                            
                    except Exception as e:
                        logger.error(f"Error deleting application {app_id}: {e}")

    def cleanup_tokens(self):
        """Clean up created test tokens"""
        logger.info("Cleaning up test tokens...")
        
        for token_id, token_info in self.test_tokens.items():
            try:
                # Handle both storage formats: dict or string
                if isinstance(token_info, dict):
                    session_token = token_info["session_token"]
                    token_name = token_info.get("name", f"Token {token_id}")
                else:
                    # token_info is just the session token string
                    session_token = token_info
                    token_name = f"Token {token_id}"
                
                headers = {"Authorization": f"Bearer {session_token}"}
                
                response = requests.delete(
                    f"{self.api_url}/auth/tokens/{token_id}",
                    headers=headers
                )
                
                if response.status_code == 200:  # Updated expected status code
                    logger.info(f"Deleted token: {token_name}")
                else:
                    logger.warning(f"Failed to delete token {token_name}: {response.status_code}")
                    
            except Exception as e:
                logger.error(f"Error cleaning up token {token_id}: {e}")
        
        self.test_tokens.clear()
    
    def test_scope_access_control(self):
        """Test scope-based access control"""
        self.log_section("Testing Scope-Based Access Control")
        
        # Test 1: Login as admin
        logger.info("Test 1: Login as admin")
        admin_credentials = get_test_user_credentials("admin")
        if not admin_credentials:
            logger.error("Admin credentials not found in test configuration")
            return
        
        username, password = admin_credentials
        admin_token = self.authenticate_user(username, password)
        if not admin_token:
            logger.error("Failed to authenticate as admin")
            return
        
        # Test 2: Create API tokens with different scopes
        logger.info("Test 2: Create API tokens with different scopes")
        
        # Create token with license read scope
        license_read_token = self.create_api_token(
            admin_token, 
            "license-read-token", 
            ["license:read"]
        )
        
        # Create token with application write scope
        app_write_token = self.create_api_token(
            admin_token, 
            "app-write-token", 
            ["application:write"]
        )
        
        # Create token with activation read scope  
        activation_read_token = self.create_api_token(
            admin_token, 
            "activation-read-token", 
            ["activation:read"]
        )
        
        if not all([license_read_token, app_write_token, activation_read_token]):
            logger.error("Failed to create test tokens")
            return
        
        # Test 3: Verify scope-based access
        logger.info("Test 3: Verify scope-based access")
        
        # Test license read access
        success1 = self.test_endpoint_with_token(
            "/licenses/", "GET", license_read_token, 200
        )
        self.log_test("License read access", success1)
        
        # Test application write access
        timestamp = int(time.time())
        app_data = {"name": f"Test App {timestamp}", "version": "1.0.0", "description": "Test application"}
        success2, app_response = self.test_application_creation(app_write_token, app_data)
        if success2 and app_response:
            # Store application ID for cleanup
            self.test_applications.append(app_response.get('id'))
        self.log_test("Application write access", success2)
        
        # Test activation read access
        success3 = self.test_endpoint_with_token(
            "/activations/", "GET", activation_read_token, 200
        )
        self.log_test("Activation read access", success3)
        
        # Test 4: Verify scope restrictions
        logger.info("Test 4: Verify scope restrictions")
        
        # Try to access applications with license read token (should fail)
        success4 = self.test_endpoint_with_token(
            "/applications/", "GET", license_read_token, 403
        )
        self.log_test("License token cannot access applications", success4)
        
        # Try to access licenses with application token (should fail)
        success5 = self.test_endpoint_with_token(
            "/licenses/", "GET", app_write_token, 403
        )
        self.log_test("Application token cannot access licenses", success5)
    
    def test_user_registration_and_role_management(self):
        """Test user registration and role management"""
        self.log_section("Testing User Registration and Role Management")
        
        # Test 1: Register new user with default role
        logger.info("Test 1: Register new user with default role")
        import time
        timestamp = int(time.time())
        
        response = requests.post(
            f"{self.api_url}/auth/register",
            json={
                "username": f"testuser{timestamp}",
                "email": f"testuser{timestamp}@test.com",
                "full_name": "Test User Registration",
                "password": "testpass123"
            }
        )
        
        if response.status_code == 201:
            user_data = response.json()
            user_id = user_data["id"]
            default_business_role = user_data["business_role"]
            
            success = default_business_role == "user"  # Default business role
            self.log_test("User registration with default role", success, f"Business role: {default_business_role}")
            
            # Test 2: Admin updates user role
            logger.info("Test 2: Admin updates user role")
            admin_credentials = get_test_user_credentials("admin")
            if admin_credentials:
                username, password = admin_credentials
                admin_token = self.authenticate_user(username, password)
                if admin_token:
                    role_update_response = requests.put(
                        f"{self.api_url}/auth/users/{user_id}/business-role",
                        json={"business_role": "user"},  # Only USER role available
                        headers={"Authorization": f"Bearer {admin_token}"}
                    )
                    
                    if role_update_response.status_code == 200:
                        updated_user = role_update_response.json()
                        success2 = updated_user["business_role"] == "user"
                        self.log_test("Admin role update", success2, f"New role: {updated_user['business_role']}")
                    else:
                        self.log_test("Admin role update", False, f"Status: {role_update_response.status_code}")
                else:
                    self.log_test("Admin role update", False, "Failed to authenticate admin")
            else:
                self.log_test("Admin role update", False, "Admin credentials not found")
        else:
            self.log_test("User registration with default role", False, f"Status: {response.status_code}")
    
    def test_invalid_token_access(self):
        """Test access with invalid/missing tokens"""
        self.log_section("Testing Invalid Token Access")
        
        # Test 1: No authentication token
        logger.info("Test 1: No authentication token")
        success1 = self.test_endpoint_with_token("/licenses/", "GET", None, 401)
        self.log_test("No token access denied", success1)
        
        # Test 2: Invalid token
        logger.info("Test 2: Invalid token")
        success2 = self.test_endpoint_with_token("/licenses/", "GET", "invalid_token_123", 401)
        self.log_test("Invalid token access denied", success2)
        
        # Test 3: Session token for scope-required endpoint (should work with proper scopes)
        logger.info("Test 3: Session token for scope-required endpoint")
        admin_credentials = get_test_user_credentials("admin")
        if admin_credentials:
            username, password = admin_credentials
            admin_token = self.authenticate_user(username, password)
            if admin_token:
                # Session tokens should work for scope-required endpoints if user has proper permissions
                success3 = self.test_endpoint_with_token("/licenses/", "GET", admin_token, 200)
                self.log_test("Session token works for scope endpoint", success3)
            else:
                self.log_test("Session token works for scope endpoint", False, "Failed to authenticate")
        else:
            self.log_test("Session token works for scope endpoint", False, "Admin credentials not found")
    
    def test_scope_error_messages(self):
        """Test error messages for insufficient permissions"""
        self.log_section("Testing Scope Error Messages")
        
        # Create a token with limited scopes
        admin_credentials = get_test_user_credentials("admin")
        if not admin_credentials:
            logger.error("Admin credentials not found in test configuration")
            return
        
        username, password = admin_credentials
        admin_token = self.authenticate_user(username, password)
        if not admin_token:
            logger.error("Failed to authenticate as admin")
            return
        
        limited_token = self.create_api_token(
            admin_token,
            "limited-token",
            ["license:read"]  # Only license read, no write
        )
        
        if not limited_token:
            logger.error("Failed to create limited token")
            return
        
        # Test 1: Try to create a license with read-only token
        logger.info("Test 1: Create license with read-only token")
        response = requests.post(
            f"{self.api_url}/licenses/",
            json={
                "customer_id": 1,
                "application_id": 1,
                "license_type": "perpetual",
                "max_activations": 5
            },
            headers={"Authorization": f"Bearer {limited_token}"}
        )
        
        if response.status_code == 403:
            error_detail = response.json().get("detail", "")
            success1 = "Insufficient permissions" in error_detail or "Required scope" in error_detail
            self.log_test("Proper error message for insufficient permissions", success1, f"Error: {error_detail}")
        else:
            self.log_test("Proper error message for insufficient permissions", False, f"Expected 403, got {response.status_code}")
        
        # Test 2: Try to access applications with license token
        logger.info("Test 2: Access applications with license token")
        response = requests.get(
            f"{self.api_url}/applications/",
            headers={"Authorization": f"Bearer {limited_token}"}
        )
        
        if response.status_code == 403:
            error_detail = response.json().get("detail", "")
            success2 = "Insufficient permissions" in error_detail or "Required scope" in error_detail
            self.log_test("Proper error message for wrong scope", success2, f"Error: {error_detail}")
        else:
            self.log_test("Proper error message for wrong scope", False, f"Expected 403, got {response.status_code}")
    
    def test_public_endpoints(self):
        """Test public endpoints that don't require authentication"""
        self.log_section("Testing Public Endpoints")
        
        # Test validation endpoint (should be public)
        logger.info("Test 1: Public validation endpoint")
        response = requests.post(
            f"{self.api_url}/validation/",
            json={
                "license_key": "test-key-123",
                "machine_id": "test-machine-123"
            }
        )
        
        success = response.status_code == 200
        self.log_test("Public validation endpoint", success, f"Status: {response.status_code}")
    
    def test_token_updates(self):
        """Test API token update functionality"""
        self.log_section("Testing Token Update Functionality")
        
        # Step 1: Get admin credentials and authenticate
        admin_creds = get_test_user_credentials("admin")
        if not admin_creds:
            self.log_test("Get admin credentials", False, "Admin user not found")
            return
        
        admin_token = self.authenticate_user(admin_creds[0], admin_creds[1])
        if not admin_token:
            self.log_test("Admin authentication", False, "Failed to authenticate admin")
            return
        
        # Step 2: Create a test token to update
        logger.info("Test 1: Create token for updating")
        token_data = {
            "name": "Test Update Token",
            "scopes": ["customer:read", "license:read"],
            "expires_at": None
        }
        
        response = requests.post(
            f"{self.api_url}/auth/tokens",
            json=token_data,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        if response.status_code != 201:
            self.log_test("Create test token", False, f"Status: {response.status_code}, Response: {response.text}")
            return
        
        token_info = response.json()
        token_id = token_info["id"]
        created_token = token_info["token"]
        self.test_tokens[token_id] = admin_token  # Store for cleanup
        
        self.log_test("Create test token", True, f"Token ID: {token_id}")
        
        # Step 3: Update token name
        logger.info("Test 2: Update token name")
        update_data = {
            "name": "Updated Token Name"
        }
        
        response = requests.put(
            f"{self.api_url}/auth/tokens/{token_id}",
            json=update_data,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        success = response.status_code == 200
        if success:
            updated_token = response.json()
            success = updated_token["name"] == "Updated Token Name"
        
        self.log_test("Update token name", success, f"Status: {response.status_code}")
        
        # Step 4: Update token scopes
        logger.info("Test 3: Update token scopes")
        update_data = {
            "scopes": ["customer:read", "customer:write", "application:read"]
        }
        
        response = requests.put(
            f"{self.api_url}/auth/tokens/{token_id}",
            json=update_data,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        success = response.status_code == 200
        if success:
            updated_token = response.json()
            returned_scopes = [scope for scope in updated_token["scopes"]]
            expected_scopes = ["customer:read", "customer:write", "application:read"]
            success = set(returned_scopes) == set(expected_scopes)
        
        self.log_test("Update token scopes", success, f"Status: {response.status_code}")
        
        # Step 5: Test updated token works with new scopes
        logger.info("Test 4: Verify updated token works with new scopes")
        response = requests.get(
            f"{self.api_url}/customers",
            headers={"Authorization": f"Bearer {created_token}"}
        )
        
        success = response.status_code == 200
        self.log_test("Updated token works with new scopes", success, f"Status: {response.status_code}")
        
        # Step 6: Disable token
        logger.info("Test 5: Disable token")
        update_data = {
            "is_active": False
        }
        
        response = requests.put(
            f"{self.api_url}/auth/tokens/{token_id}",
            json=update_data,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        success = response.status_code == 200
        if success:
            updated_token = response.json()
            success = updated_token["is_active"] == False
        
        self.log_test("Disable token", success, f"Status: {response.status_code}")
        
        # Step 7: Test disabled token returns 401
        logger.info("Test 6: Verify disabled token is rejected")
        response = requests.get(
            f"{self.api_url}/customers",
            headers={"Authorization": f"Bearer {created_token}"}
        )
        
        success = response.status_code == 401
        self.log_test("Disabled token rejected", success, f"Status: {response.status_code}")
        
        # Step 8: Test invalid scope assignment (should fail)
        logger.info("Test 7: Test invalid scope assignment")
        # Try to assign a scope that admin doesn't have permission for
        # (this should work for admin since they have all permissions, so we'll use a regular user)
        
        # Create a regular user token first
        john_creds = get_test_user_credentials("john")
        if john_creds:
            john_token = self.authenticate_user(john_creds[0], john_creds[1])
            if john_token:
                # Create a token for john
                token_data = {
                    "name": "John's Limited Token",
                    "scopes": ["customer:read"]
                }
                
                response = requests.post(
                    f"{self.api_url}/auth/tokens",
                    json=token_data,
                    headers={"Authorization": f"Bearer {john_token}"}
                )
                
                if response.status_code == 201:
                    john_token_info = response.json()
                    john_token_id = john_token_info["id"]
                    self.test_tokens[john_token_id] = john_token
                    
                    # Try to update with scopes john doesn't have
                    invalid_update = {
                        "scopes": ["user:management", "token:management"]  # Admin-only scopes
                    }
                    
                    response = requests.put(
                        f"{self.api_url}/auth/tokens/{john_token_id}",
                        json=invalid_update,
                        headers={"Authorization": f"Bearer {john_token}"}
                    )
                    
                    success = response.status_code == 403
                    self.log_test("Invalid scope assignment rejected", success, f"Status: {response.status_code}")
        
        # Step 9: Test update non-existent token
        logger.info("Test 8: Update non-existent token")
        response = requests.put(
            f"{self.api_url}/auth/tokens/99999",
            json={"name": "Should fail"},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        success = response.status_code == 404
        self.log_test("Update non-existent token", success, f"Status: {response.status_code}")
        
        # Step 10: Test update token without permission
        logger.info("Test 9: Update token without permission")
        # Try to update with no auth header
        response = requests.put(
            f"{self.api_url}/auth/tokens/{token_id}",
            json={"name": "Should fail"}
        )
        
        success = response.status_code == 401
        self.log_test("Update without auth", success, f"Status: {response.status_code}")
        
        # Step 11: Test PATCH endpoint for incremental updates
        logger.info("Test 10: Test PATCH endpoint for incremental updates")
        
        # Create a fresh token for PATCH testing
        patch_token_data = {
            "name": "PATCH Test Token",
            "scopes": ["customer:read"],
            "expires_at": None
        }
        
        response = requests.post(
            f"{self.api_url}/auth/tokens",
            json=patch_token_data,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        if response.status_code == 201:
            patch_token_info = response.json()
            patch_token_id = patch_token_info["id"]
            self.test_tokens[patch_token_id] = admin_token  # Store for cleanup
            
            # Test PATCH for name only (incremental update)
            patch_data = {"name": "PATCH Updated Name"}
            response = requests.patch(
                f"{self.api_url}/auth/tokens/{patch_token_id}",
                json=patch_data,
                headers={"Authorization": f"Bearer {admin_token}"}
            )
            
            success = response.status_code == 200
            self.log_test("PATCH token name (incremental)", success, f"Status: {response.status_code}")
            
            # Test PATCH for scopes only
            patch_data = {"scopes": ["customer:read", "customer:write"]}
            response = requests.patch(
                f"{self.api_url}/auth/tokens/{patch_token_id}",
                json=patch_data,
                headers={"Authorization": f"Bearer {admin_token}"}
            )
            
            success = response.status_code == 200
            self.log_test("PATCH token scopes (incremental)", success, f"Status: {response.status_code}")
            
            # Test PATCH for status only
            patch_data = {"is_active": False}
            response = requests.patch(
                f"{self.api_url}/auth/tokens/{patch_token_id}",
                json=patch_data,
                headers={"Authorization": f"Bearer {admin_token}"}
            )
            
            success = response.status_code == 200
            self.log_test("PATCH token status (incremental)", success, f"Status: {response.status_code}")
            
        else:
            self.log_test("Create PATCH test token", False, f"Status: {response.status_code}")
    
    def run_all_tests(self):
        """Run all tests"""
        logger.info("Starting Token Scopes Feature Tests")
        logger.info(f"Testing against: {self.api_url}")
        
        try:
            # Test public endpoints first
            self.test_public_endpoints()
            
            # Test scope-based access control
            self.test_scope_access_control()
            
            # Test user registration and role management
            self.test_user_registration_and_role_management()
            
            # Test invalid token access
            self.test_invalid_token_access()
            
            # Test scope error messages
            self.test_scope_error_messages()
            
            # Test token updates
            self.test_token_updates()
            
        except Exception as e:
            logger.error(f"Test execution error: {e}")
        
        finally:
            logger.info("🎉 All tests completed!")
            logger.info("Cleaning up test tokens...")
            self.cleanup_applications()
            self.cleanup_tokens()


def main():
    """Main test function"""
    tester = TokenScopesTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main() 