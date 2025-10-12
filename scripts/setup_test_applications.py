#!/usr/bin/env python3
"""
Setup Test Applications

This script creates the test applications from config/test_applications.json
under a specified user account (default: braden).
"""
import requests
import json
import logging
import sys
from pathlib import Path

# Add the parent directory to the Python path so we can import from app
sys.path.append(str(Path(__file__).parent.parent))

from app.utils.test_users import get_test_user_credentials, get_braden_api_token

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class ApplicationSetup:
    def __init__(self, base_url: str = "http://localhost:8999"):
        self.base_url = base_url.rstrip('/')
        self.api_url = f"{self.base_url}/api/v1"
        
    def load_test_applications(self) -> list:
        """Load applications from test_applications.json"""
        config_file = Path(__file__).parent.parent / "config" / "test_applications.json"
        
        if not config_file.exists():
            logger.error(f"Test applications file not found: {config_file}")
            return []
            
        try:
            with open(config_file, 'r') as f:
                data = json.load(f)
                return data.get('applications', [])
        except Exception as e:
            logger.error(f"Error loading test applications: {e}")
            return []
    
    def authenticate_user(self, username: str, password: str) -> str:
        """Authenticate user and return session token"""
        try:
            response = requests.post(
                f"{self.api_url}/auth/login",
                data={"username": username, "password": password},
                headers={"Content-Type": "application/x-www-form-urlencoded"}
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
    
    def get_auth_token(self, username: str = "braden") -> str:
        """Get authentication token (try API token first, then session token)"""
        # Try to use permanent API token first (if it's braden)
        if username.lower() == "braden":
            api_token = get_braden_api_token()
            if api_token:
                logger.info("Using permanent API token for authentication")
                return api_token
        
        # Fall back to session token
        credentials = get_test_user_credentials(username)
        if not credentials:
            logger.error(f"No credentials found for user: {username}")
            return None
            
        username, password = credentials
        session_token = self.authenticate_user(username, password)
        if session_token:
            logger.info("Using session token for authentication")
            return session_token
        
        return None
    
    def create_application(self, app_data: dict, token: str) -> bool:
        """Create a single application"""
        try:
            # Prepare the application data for API
            api_data = {
                "name": app_data["name"],
                "version": app_data["version"],
                "description": app_data["description"],
                "features": app_data.get("features", {})
            }
            
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(
                f"{self.api_url}/applications/",
                json=api_data,
                headers=headers
            )
            
            if response.status_code == 201:
                app_response = response.json()
                logger.info(f"✅ Created application: {app_data['name']} (ID: {app_response['id']})")
                return True
            elif response.status_code == 400 and "already exists" in response.text:
                logger.info(f"ℹ️  Application already exists: {app_data['name']}")
                return True
            else:
                logger.error(f"❌ Failed to create {app_data['name']}: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error creating application {app_data['name']}: {e}")
            return False
    
    def setup_applications(self, username: str = "braden") -> bool:
        """Set up all test applications for a user"""
        logger.info(f"Setting up test applications for user: {username}")
        
        # Load test applications
        applications = self.load_test_applications()
        if not applications:
            logger.error("No applications to create")
            return False
        
        logger.info(f"Found {len(applications)} applications to create")
        
        # Get authentication token
        token = self.get_auth_token(username)
        if not token:
            logger.error(f"Failed to get authentication token for user: {username}")
            return False
        
        # Create each application
        success_count = 0
        for app_data in applications:
            if self.create_application(app_data, token):
                success_count += 1
        
        logger.info(f"Successfully created/verified {success_count}/{len(applications)} applications")
        return success_count == len(applications)

def main():
    """Main setup function"""
    setup = ApplicationSetup()
    
    # You can change the username here if needed
    username = "braden"
    
    logger.info("=" * 60)
    logger.info("Test Applications Setup")
    logger.info("=" * 60)
    
    success = setup.setup_applications(username)
    
    if success:
        logger.info("🎉 All applications set up successfully!")
    else:
        logger.error("❌ Some applications failed to set up")
        sys.exit(1)

if __name__ == "__main__":
    main()
