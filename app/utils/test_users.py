"""
Test Users Configuration

This module provides utilities for loading and managing test users
from a centralized JSON configuration file.
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from app.core.constants import PROJECT_ROOT

# Get the project root directory
TEST_USERS_FILE = PROJECT_ROOT / "config" / "test_users.json"


def load_test_users() -> Dict[str, Dict[str, Any]]:
    """Load test users from JSON configuration file"""
    try:
        with open(TEST_USERS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  Test users file not found: {TEST_USERS_FILE}")
        return {}
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing test users file: {e}")
        return {}


def get_test_user(username: str) -> Optional[Dict[str, Any]]:
    """Get a specific test user by username"""
    users = load_test_users()
    return users.get(username)


def get_test_user_credentials(username: str) -> Optional[tuple[str, str]]:
    """Get username and password for a test user"""
    user = get_test_user(username)
    if user:
        return user["username"], user["password"]
    return None


def get_test_user_api_token(username: str) -> Optional[str]:
    """Get API token for a test user"""
    user = get_test_user(username)
    if user:
        return user.get("api_token")
    return None


def get_braden_api_token() -> Optional[str]:
    """Get Braden's permanent API token for testing"""
    return get_test_user_api_token("braden")


def get_all_test_users() -> Dict[str, Dict[str, Any]]:
    """Get all test users"""
    return load_test_users()


def get_test_users_for_registration() -> list[Dict[str, Any]]:
    """Get test users formatted for registration (without roles)"""
    users = load_test_users()
    registration_users = []
    
    for user_data in users.values():
        # Only include username, email, full_name, and password for registration
        registration_user = {
            "username": user_data["username"],
            "email": user_data["email"],
            "full_name": user_data["full_name"],
            "password": user_data["password"]
        }
        registration_users.append(registration_user)
    
    return registration_users


def print_test_users_info():
    """Print information about available test users"""
    users = load_test_users()
    
    print("👥 Available Test Users:")
    print("=" * 50)
    
    for username, user_data in users.items():
        print(f"👤 {username}")
        print(f"   Name: {user_data['full_name']}")
        print(f"   Email: {user_data['email']}")
        print(f"   Password: {user_data['password']}")
        print(f"   Business Role: {user_data['business_role']}")
        print(f"   System Role: {user_data['system_role']}")
        print(f"   Description: {user_data['description']}")
        if 'api_token' in user_data:
            print(f"   API Token: {user_data['api_token']}")
        print()


if __name__ == "__main__":
    # Test the module
    print_test_users_info() 