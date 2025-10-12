#!/usr/bin/env python3
"""
Setup authentication database with user tables and initial admin user
"""
import sys
from pathlib import Path

# Add the root project directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlmodel import create_engine, SQLModel
from app.config import settings
from app.models.database import (
    User, Customer, Application, LicenseKey, Activation, 
    ActivationForm, OfflineActivationCode, APIToken, Session,
    UserRole, SystemRole
)
from app.services.auth_service import AuthService
from app.models.schemas import UserCreate
from app.database.connection import get_session
from app.utils.test_users import get_test_users_for_registration, get_test_user_credentials, print_test_users_info


def setup_database():
    """Create all database tables"""
    print("🔧 Setting up authentication database...")
    
    # Create engine
    engine = create_engine(settings.database_url)
    
    # Create all tables
    SQLModel.metadata.create_all(engine)
    print("✅ Database tables created successfully")


def create_initial_admin():
    """Create initial admin user"""
    print("\n👤 Creating initial admin user...")
    
    with next(get_session()) as db:
        auth_service = AuthService(db)
        
        # Check if admin already exists
        existing_admin = auth_service.get_user_by_username("admin")
        if existing_admin:
            print("⚠️  Admin user already exists")
            return
        
        # Get admin user data from config
        admin_credentials = get_test_user_credentials("admin")
        if not admin_credentials:
            print("❌ Admin user not found in test configuration")
            return
        
        username, password = admin_credentials
        
        # Create admin user
        admin_data = UserCreate(
            username=username,
            email="admin@example.com",
            full_name="System Administrator",
            password=password
        )
        
        try:
            admin_user_response = auth_service.create_user(admin_data)
            
            # Get the actual user from database to update system role
            admin_user = auth_service.get_user_by_username("admin")
            if admin_user:
                # Update to system admin role
                admin_user.system_role = SystemRole.SYSTEM_ADMIN
                db.add(admin_user)
                db.commit()
                db.refresh(admin_user)
                
                print(f"✅ Admin user created successfully:")
                print(f"   Username: {admin_user.username}")
                print(f"   Email: {admin_user.email}")
                print(f"   Business Role: {admin_user.business_role}")
                print(f"   System Role: {admin_user.system_role}")
                print(f"   ID: {admin_user.id}")
            else:
                print("❌ Failed to retrieve admin user for role update")
        except Exception as e:
            print(f"❌ Error creating admin user: {e}")


def create_sample_users():
    """Create sample users for testing"""
    print("\n👥 Creating sample users...")
    
    with next(get_session()) as db:
        auth_service = AuthService(db)
        
        # Get test users from configuration
        test_users = get_test_users_for_registration()
        
        # Filter out admin (already created) and testuser (created during testing)
        sample_users = [user for user in test_users if user["username"] not in ["admin", "testuser"]]
        
        for user_data in sample_users:
            try:
                # Create user
                user_create = UserCreate(**user_data)
                user_response = auth_service.create_user(user_create)
                print(f"✅ Created {user_response.business_role} user: {user_response.username}")
            except Exception as e:
                print(f"❌ Error creating user {user_data['username']}: {e}")


def test_authentication():
    """Test authentication with created users"""
    print("\n🔐 Testing authentication...")
    
    with next(get_session()) as db:
        auth_service = AuthService(db)
        
        # Test admin login
        admin_credentials = get_test_user_credentials("admin")
        if admin_credentials:
            username, password = admin_credentials
            try:
                admin_user = auth_service.authenticate_user(username, password)
                if admin_user:
                    token_response = auth_service.create_access_token(admin_user)
                    print(f"✅ Admin authentication successful")
                    print(f"   Token: {token_response.access_token[:20]}...")
                else:
                    print("❌ Admin authentication failed")
            except Exception as e:
                print(f"❌ Admin authentication error: {e}")
        else:
            print("❌ Admin credentials not found in test configuration")
        
        # Test regular user login
        user_credentials = get_test_user_credentials("john")
        if user_credentials:
            username, password = user_credentials
            try:
                user = auth_service.authenticate_user(username, password)
                if user:
                    token_response = auth_service.create_access_token(user)
                    print(f"✅ User authentication successful")
                    print(f"   Token: {token_response.access_token[:20]}...")
                else:
                    print("❌ User authentication failed")
            except Exception as e:
                print(f"❌ User authentication error: {e}")
        else:
            print("❌ User credentials not found in test configuration")


def main():
    """Main setup function"""
    print("🔐 Authentication Database Setup")
    print("=" * 50)
    
    # Show available test users
    print_test_users_info()
    
    # Setup database
    setup_database()
    
    # Create initial admin
    create_initial_admin()
    
    # Create sample users
    create_sample_users()
    
    # Test authentication
    test_authentication()
    
    print("\n🎉 Setup complete!")
    print("\nDefault users created from config/test_users.json")


if __name__ == "__main__":
    main() 