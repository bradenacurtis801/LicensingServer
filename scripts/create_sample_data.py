#!/usr/bin/env python3
"""Script to create sample data for development and testing"""

import sys
import os
import requests
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select, create_engine, SQLModel
from app.database.connection import engine, create_db_and_tables
from app.models.database import Customer, Application, LicenseKey, LicenseStatus, User, SystemRole
from app.utils.license_generator import LicenseKeyGenerator
from app.services.auth_service import AuthService
from app.models.schemas import UserCreate
from app.utils.test_users import get_test_users_for_registration, get_test_user_credentials
from pathlib import Path

# API configuration
BASE_URL = "http://localhost:8999"  # Your backend port from .env
API_PREFIX = "/api/v1"

def get_user_token(username: str) -> str:
    """Get authentication token for a user by logging in via API"""
    try:
        # Get user credentials from test_users.json
        user_creds = get_test_user_credentials(username)
        
        if not user_creds:
            print(f"⚠️  No credentials found for user: {username}")
            return None
        
        # user_creds is a tuple (username, password)
        username, password = user_creds
        
        # Login via API
        login_data = {
            "username": username,
            "password": password
        }
        
        response = requests.post(f"{BASE_URL}{API_PREFIX}/auth/login", json=login_data)
        
        if response.status_code == 200:
            login_response = response.json()
            # Get the session token from response
            token = login_response.get("session_token")
            if token:
                print(f"  ✅ Successfully logged in user: {username}")
                return token
            else:
                print(f"  ⚠️  Response missing session_token field: {login_response.keys()}")
                return None
        else:
            print(f"  ❌ Login failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"⚠️  Error getting token for user {username}: {e}")
        return None

def load_json_data(file_path: str) -> dict:
    """Load data from JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  File not found: {file_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON file {file_path}: {e}")
        return {}

def setup_database():
    """Create all database tables"""
    print("🔧 Setting up database tables...")
    
    # Create all tables
    create_db_and_tables()
    print("✅ Database tables created successfully")

def create_users():
    """Create users from test configuration"""
    print("\n👥 Setting up users...")
    
    with Session(engine) as session:
        auth_service = AuthService(session)
        
        # Get test users from configuration
        test_users = get_test_users_for_registration()
        
        created_users = []
        
        for user_data in test_users:
            # Check if user already exists
            existing_user = auth_service.get_user_by_username(user_data["username"])
            if existing_user:
                print(f"✅ User already exists: {existing_user.username}")
                created_users.append(existing_user)
                continue
            
            try:
                # Create user
                user_create = UserCreate(**user_data)
                user_response = auth_service.create_user(user_create)
                
                # Get the actual user from database to update system role if needed
                user = auth_service.get_user_by_username(user_data["username"])
                if user:
                    # Update system role if it's admin or braden
                    if user.username in ["admin", "braden"]:
                        user.system_role = SystemRole.SYSTEM_ADMIN
                        session.add(user)
                        session.commit()
                        session.refresh(user)
                    
                    created_users.append(user)
                    print(f"✅ Created user: {user.username} (ID: {user.id})")
                else:
                    print(f"❌ Failed to retrieve user {user_data['username']} after creation")
                    
            except Exception as e:
                print(f"❌ Error creating user {user_data['username']}: {e}")
        
        return created_users

def create_user_data(user_data: dict, user: User, session: Session):
    """Create applications, customers, and licenses for a specific user"""
    print(f"\n🔧 Creating data for user: {user.username}")
    
    # Create applications for this user
    applications = []
    if "applications" in user_data and user_data["applications"]:
        print(f"  📱 Creating {len(user_data['applications'])} applications...")
        
        for app_data in user_data["applications"]:
            # Check if application already exists
            existing_app = session.exec(
                select(Application).where(
                    Application.name == app_data["name"],
                    Application.version == app_data["version"],
                    Application.user_id == user.id
                )
            ).first()
            
            if existing_app:
                print(f"    ✅ Application already exists: {existing_app.name} v{existing_app.version}")
                applications.append(existing_app)
            else:
                # Add user_id to application data and convert features to JSON string
                app_data["user_id"] = user.id
                if "features" in app_data:
                    app_data["features"] = json.dumps(app_data["features"])
                app = Application(**app_data)
                session.add(app)
                session.commit()
                session.refresh(app)
                applications.append(app)
                print(f"    ✅ Created application: {app.name} v{app.version}")
    
    # Create customers and licenses for this user
    customers = []
    created_licenses = []
    
    if "customers" in user_data and user_data["customers"]:
        print(f"  👥 Creating {len(user_data['customers'])} customers...")
        
        for customer_data in user_data["customers"]:
            # Check if customer already exists for THIS USER only
            existing_customer = session.exec(
                select(Customer).where(
                    Customer.email == customer_data["email"],
                    Customer.user_id == user.id
                )
            ).first()
            
            if existing_customer:
                print(f"    ✅ Customer already exists: {existing_customer.name} ({existing_customer.email})")
                customers.append(existing_customer)
            else:
                # Add user_id to customer data
                customer_data["user_id"] = user.id
                customer = Customer(**customer_data)
                session.add(customer)
                session.commit()
                session.refresh(customer)
                customers.append(customer)
                print(f"    ✅ Created customer: {customer.name} ({customer.email})")
            
            # Create licenses for this customer
            if "licenses" in customer_data and customer_data["licenses"]:
                print(f"    🔑 Creating {len(customer_data['licenses'])} licenses...")
                
                for license_data in customer_data["licenses"]:
                    # Find application by name and version for the current user
                    application = session.exec(
                        select(Application).where(
                            Application.name == license_data["application_name"],
                            Application.version == license_data["application_version"],
                            Application.user_id == user.id
                        )
                    ).first()
                    
                    if not application:
                        print(f"      ⚠️  Application not found for license: {license_data['application_name']} v{license_data['application_version']}")
                        continue
                    
                    # Check if license already exists for this customer-application combination
                    # Determine which customer ID to use
                    customer_id_to_use = existing_customer.id if existing_customer else customer.id
                    
                    existing_license = session.exec(
                        select(LicenseKey).where(
                            LicenseKey.customer_id == customer_id_to_use,
                            LicenseKey.application_id == application.id
                        )
                    ).first()
                    
                    if existing_license:
                        print(f"      ✅ License already exists for {existing_customer.name if existing_customer else customer.name} - {application.name}")
                    else:
                        # Create license through API to get the plain text key
                        print(f"      🔑 Creating license via API for {existing_customer.name if existing_customer else customer.name} - {application.name}")
                        
                        # Parse expiration date
                        expires_at = None
                        if license_data.get("expires_at"):
                            try:
                                expires_at = datetime.fromisoformat(license_data["expires_at"].replace("Z", "+00:00"))
                            except ValueError:
                                print(f"      ⚠️  Invalid expiration date format: {license_data['expires_at']}")
                        
                        # Prepare license data for API
                        api_license_data = {
                            "customer_id": customer_id_to_use,
                            "application_id": application.id,
                            "expires_at": expires_at.isoformat() if expires_at else None,
                            "max_activations": license_data.get("max_activations", 1),
                            "features": license_data.get("features", {}),
                            "notes": license_data.get("notes", ""),
                            "status": "active"
                        }
                        
                        try:
                            # Call the license creation API
                            response = requests.post(
                                f"{BASE_URL}{API_PREFIX}/licenses/",
                                json=api_license_data,
                                headers={"Authorization": f"Bearer {get_user_token(user.username)}"}
                            )
                            
                            if response.status_code == 201:
                                license_response = response.json()
                                license_key = license_response.get("license_key")
                                if license_key:
                                    print(f"      ✅ Created license via API: {license_key[:20]}...")
                                    created_licenses.append((license_response, license_key))
                                else:
                                    print(f"      ⚠️  API response missing license key")
                            else:
                                print(f"      ❌ Failed to create license via API: {response.status_code}")
                                print(f"      Response: {response.text}")
                                
                        except Exception as e:
                            print(f"      ❌ Error calling license API: {e}")
                            # Fallback to direct database creation if API fails
                            print(f"      🔄 Falling back to direct database creation...")
                            generator = LicenseKeyGenerator()
                            license_key = generator.generate_key()
                            key_hash = generator.hash_key(license_key)
                            
                            db_license = LicenseKey(
                                key_hash=key_hash,
                                customer_id=customer_id_to_use,
                                application_id=application.id,
                                expires_at=expires_at,
                                max_activations=license_data.get("max_activations", 1),
                                features=json.dumps(license_data.get("features", {})),
                                notes=license_data.get("notes", ""),
                                status=LicenseStatus.ACTIVE
                            )
                            
                            session.add(db_license)
                            session.commit()
                            session.refresh(db_license)
                            created_licenses.append((db_license, license_key))
                            print(f"      ✅ Created license in database: {license_key[:20]}...")
    
    return applications, customers, created_licenses

def create_sample_data():
    """Create sample data for all users from test_users.json"""
    
    # Setup database and users first
    setup_database()
    users = create_users()
    
    if not users:
        print("❌ No users available. Cannot create sample data.")
        return
    
    # Load the complete test_users.json file
    test_users_data = load_json_data("config/test_users.json")
    if not test_users_data:
        print("❌ No test users data found in config/test_users.json")
        return
    
    # Track all created data
    all_applications = []
    all_customers = []
    all_created_licenses = []
    
    with Session(engine) as session:
        for username, user_data in test_users_data.items():
            # Find the user in the database
            user = session.exec(
                select(User).where(User.username == username)
            ).first()
            
            if not user:
                print(f"⚠️  User {username} not found in database, skipping...")
                continue
            
            # Create data for this user
            applications, customers, created_licenses = create_user_data(user_data, user, session)
            
            all_applications.extend(applications)
            all_customers.extend(customers)
            all_created_licenses.extend(created_licenses)
    
    # Print data summary
    print("\n📊 Data Summary:")
    print(f"👤 Total Users: {len(users)}")
    print(f"📱 Total Applications: {len(all_applications)}")
    print(f"👥 Total Customers: {len(all_customers)}")
    print(f"🔑 Total New Licenses: {len(all_created_licenses)}")
    
    # Update test_users.json with actual license keys
    if all_created_licenses:
        print("\n🔑 Updating test_users.json with actual license keys...")
        
        # Load current test_users.json
        test_users_file = "config/test_users.json"
        current_test_users = load_json_data(test_users_file)
        
        # Update with actual license keys
        for license_response, license_key in all_created_licenses:
            # Find the customer and application
            customer_id = license_response.get("customer_id")
            application_id = license_response.get("application_id")
            
            if customer_id and application_id:
                # Find the customer in our data
                customer = None
                for c in all_customers:
                    if c.id == customer_id:
                        customer = c
                        break
                
                # Find the application in our data
                application = None
                for a in all_applications:
                    if a.id == application_id:
                        application = a
                        break
                
                if customer and application:
                    # Find the user who owns this customer
                    user = None
                    for u in users:
                        if u.id == customer.user_id:
                            user = u
                            break
                    
                    if user and user.username in current_test_users:
                        # Find the customer in test_users.json
                        for test_customer in current_test_users[user.username]["customers"]:
                            if test_customer["email"] == customer.email:
                                # Find the license in test_users.json
                                for test_license in test_customer["licenses"]:
                                    if (test_license["application_name"] == application.name and 
                                        test_license["application_version"] == application.version):
                                        # Update with actual license key
                                        test_license["license_key"] = license_key
                                        test_license["database_id"] = license_response.get("id")
                                        print(f"  ✅ Updated license for {customer.name} - {application.name}")
                                        break
                                break
        
        # Save updated test_users.json
        with open(test_users_file, "w") as f:
            json.dump(current_test_users, f, indent=2)
        
        print(f"💾 Updated {test_users_file} with actual license keys")
        
        # Print summary of license keys
        print("\n🔑 Newly Generated License Keys:")
        for i, (license_response, license_key) in enumerate(all_created_licenses):
            print(f"{i+1}. {license_key}")
            print(f"   Customer ID: {license_response.get('customer_id')}")
            print(f"   Application ID: {license_response.get('application_id')}")
            print(f"   Database ID: {license_response.get('id')}")
            print()

if __name__ == "__main__":
    create_sample_data()