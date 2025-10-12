"""
Utility functions for generating random test data for development and testing.
"""

import random
import string
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional
from faker import Faker
from app.models.schemas import UserCreate
from app.models.database import SystemRole, UserRole, LicenseStatus

# Initialize Faker for realistic data generation
fake = Faker()

class TestDataGenerator:
    """Generates random test data for all database tables"""
    
    # Predefined lists for realistic data
    APPLICATION_CATEGORIES = [
        "Productivity", "Development", "Analytics", "Communication", 
        "Business", "Design", "Security", "Entertainment", "Education", "Finance"
    ]
    
    PLATFORMS = [
        "Desktop", "Web", "Mobile", "Cross-platform", "Cloud", "Server", "Embedded"
    ]
    
    OPERATING_SYSTEMS = [
        "Windows 10", "Windows 11", "macOS 12", "macOS 13", "Ubuntu 20.04", 
        "Ubuntu 22.04", "CentOS 8", "Debian 11", "iOS 15", "iOS 16", 
        "Android 11", "Android 12", "Android 13"
    ]
    
    COMPANY_SUFFIXES = [
        "Inc", "LLC", "Corp", "Ltd", "Company", "Group", "Solutions", 
        "Technologies", "Systems", "Enterprises", "Partners", "Associates"
    ]
    
    BUSINESS_DOMAINS = [
        "Technology", "Healthcare", "Finance", "Education", "Retail", 
        "Manufacturing", "Consulting", "Marketing", "Legal", "Real Estate"
    ]
    
    @staticmethod
    def random_string(length: int = 10) -> str:
        """Generate a random string of specified length"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @staticmethod
    def random_license_key() -> str:
        """Generate a random license key in the format XXXXX-XXXXX-XXXXX-XXXXX-XXXXX"""
        parts = []
        for _ in range(5):
            part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            parts.append(part)
        return '-'.join(parts)
    
    @staticmethod
    def random_email(domain: str = None) -> str:
        """Generate a random email address"""
        if not domain:
            domain = fake.domain_name()
        username = fake.user_name()
        return f"{username}@{domain}"
    
    @staticmethod
    def random_phone() -> str:
        """Generate a random phone number"""
        return fake.phone_number()
    
    @staticmethod
    def random_date(start_date: datetime = None, end_date: datetime = None) -> datetime:
        """Generate a random date between start_date and end_date"""
        if not start_date:
            start_date = datetime.now(timezone.utc) - timedelta(days=365)
        if not end_date:
            end_date = datetime.now(timezone.utc) + timedelta(days=365)
        
        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randrange(days_between)
        return start_date + timedelta(days=random_days)
    
    @staticmethod
    def random_expiration_date() -> Optional[datetime]:
        """Generate a random expiration date (or None for perpetual licenses)"""
        if random.random() < 0.2:  # 20% chance of perpetual license
            return None
        return datetime.now(timezone.utc) + timedelta(days=random.randint(30, 1095))  # 1 month to 3 years
    
    @staticmethod
    def random_features() -> Dict[str, bool]:
        """Generate random feature flags"""
        feature_names = [
            "basic_features", "advanced_features", "premium_support", "cloud_sync",
            "offline_mode", "code_editor", "debugger", "deployment_tools",
            "team_collaboration", "version_control", "testing_framework",
            "data_import", "visualization", "statistical_analysis", "machine_learning",
            "report_generation", "real_time_processing", "text_messaging",
            "voice_calls", "video_calls", "file_sharing", "group_chat",
            "message_encryption", "task_management", "time_tracking",
            "resource_planning", "reporting", "integration_api"
        ]
        
        features = {}
        for feature in feature_names:
            features[feature] = random.choice([True, False])
        
        return features
    
    @staticmethod
    def random_system_requirements() -> Dict[str, str]:
        """Generate random system requirements"""
        os_choices = random.sample(TestDataGenerator.OPERATING_SYSTEMS, random.randint(1, 3))
        ram_options = ["2GB", "4GB", "8GB", "16GB", "32GB"]
        storage_options = ["100MB", "500MB", "1GB", "2GB", "5GB", "10GB"]
        
        return {
            "os": ", ".join(os_choices),
            "ram": random.choice(ram_options),
            "storage": random.choice(storage_options)
        }

class UserDataGenerator:
    """Generates random user data"""
    
    @staticmethod
    def generate_user_create(
        username: str = None,
        email: str = None,
        full_name: str = None,
        password: str = None,
        description: str = None
    ) -> UserCreate:
        """Generate a random UserCreate object"""
        if not username:
            username = fake.user_name()
        if not email:
            email = fake.email()
        if not full_name:
            full_name = fake.name()
        if not password:
            password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
        
        return UserCreate(
            username=username,
            email=email,
            full_name=full_name,
            password=password
        )
    
    @staticmethod
    def generate_multiple_users(count: int = 5) -> List[UserCreate]:
        """Generate multiple random users"""
        users = []
        for i in range(count):
            user = UserDataGenerator.generate_user_create()
            users.append(user)
        return users

class ApplicationDataGenerator:
    """Generates random application data"""
    
    @staticmethod
    def generate_application(
        user_id: int,
        name: str = None,
        version: str = None,
        description: str = None,
        features: Dict[str, bool] = None,
        category: str = None,
        platform: str = None,
        min_system_requirements: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """Generate a random application dictionary"""
        
        if not name:
            app_names = [
                "DataAnalyzer", "ProjectManager", "SecureChat", "WebToolSuite",
                "DesignStudio", "CodeEditor", "FileManager", "TaskTracker",
                "ReportGenerator", "Dashboard", "AnalyticsSuite", "CollaborationHub",
                "SecurityManager", "BackupTool", "MonitorPro", "Optimizer"
            ]
            name = random.choice(app_names)
        
        if not version:
            major = random.randint(1, 5)
            minor = random.randint(0, 9)
            patch = random.randint(0, 9)
            version = f"{major}.{minor}.{patch}"
        
        if not description:
            descriptions = [
                f"Professional {name.lower()} for business users",
                f"Advanced {name.lower()} with enterprise features",
                f"Simple and intuitive {name.lower()}",
                f"Powerful {name.lower()} for professionals",
                f"Modern {name.lower()} with cloud integration"
            ]
            description = random.choice(descriptions)
        
        if not features:
            features = TestDataGenerator.random_features()
        
        if not category:
            category = random.choice(TestDataGenerator.APPLICATION_CATEGORIES)
        
        if not platform:
            platform = random.choice(TestDataGenerator.PLATFORMS)
        
        if not min_system_requirements:
            min_system_requirements = TestDataGenerator.random_system_requirements()
        
        return {
            "name": name,
            "version": version,
            "description": description,
            "features": features,
            "category": category,
            "platform": platform,
            "min_system_requirements": min_system_requirements,
            "user_id": user_id
        }
    
    @staticmethod
    def generate_multiple_applications(user_id: int, count: int = 3) -> List[Dict[str, Any]]:
        """Generate multiple random applications for a user"""
        applications = []
        for i in range(count):
            app = ApplicationDataGenerator.generate_application(user_id)
            applications.append(app)
        return applications

class CustomerDataGenerator:
    """Generates random customer data"""
    
    @staticmethod
    def generate_customer(
        user_id: int,
        name: str = None,
        email: str = None,
        company: str = None,
        phone: str = None,
        address: str = None,
        notes: str = None
    ) -> Dict[str, Any]:
        """Generate a random customer dictionary"""
        
        if not name:
            name = fake.name()
        
        if not email:
            email = fake.email()
        
        if not company:
            if random.random() < 0.7:  # 70% chance of having a company
                company_name = fake.company()
                suffix = random.choice(TestDataGenerator.COMPANY_SUFFIXES)
                company = f"{company_name} {suffix}"
            else:
                company = None
        
        if not phone:
            phone = fake.phone_number()
        
        if not address:
            address = fake.address()
        
        if not notes:
            note_templates = [
                "Customer since {year}",
                "Premium customer with annual subscription",
                "Enterprise customer with multiple licenses",
                "Startup company, trial license",
                "Individual user",
                "Small business customer",
                "Regular customer with good payment history"
            ]
            year = random.randint(2020, 2024)
            notes = random.choice(note_templates).format(year=year)
        
        return {
            "name": name,
            "email": email,
            "company": company,
            "phone": phone,
            "address": address,
            "notes": notes,
            "user_id": user_id
        }
    
    @staticmethod
    def generate_multiple_customers(user_id: int, count: int = 5) -> List[Dict[str, Any]]:
        """Generate multiple random customers for a user"""
        customers = []
        for i in range(count):
            customer = CustomerDataGenerator.generate_customer(user_id)
            customers.append(customer)
        return customers

class LicenseDataGenerator:
    """Generates random license data"""
    
    @staticmethod
    def generate_license(
        customer_id: int,
        application_id: int,
        expires_at: datetime = None,
        max_activations: int = None,
        features: Dict[str, bool] = None,
        notes: str = None,
        status: LicenseStatus = None
    ) -> Dict[str, Any]:
        """Generate a random license dictionary"""
        
        if not expires_at:
            expires_at = TestDataGenerator.random_expiration_date()
        
        if not max_activations:
            activation_options = [1, 2, 3, 5, 10, 25, 50, 100]
            max_activations = random.choice(activation_options)
        
        if not features:
            features = TestDataGenerator.random_features()
        
        if not notes:
            note_templates = [
                "Standard license for {customer_type}",
                "{duration} license with {features_count} features",
                "License for {max_activations} devices",
                "Professional license with support",
                "Enterprise license with all features",
                "Trial license for evaluation"
            ]
            
            customer_type = "business" if max_activations > 1 else "individual"
            duration = "annual" if expires_at else "perpetual"
            features_count = sum(features.values())
            
            notes = random.choice(note_templates).format(
                customer_type=customer_type,
                duration=duration,
                features_count=features_count,
                max_activations=max_activations
            )
        
        if not status:
            status = random.choice(list(LicenseStatus))
        
        return {
            "customer_id": customer_id,
            "application_id": application_id,
            "expires_at": expires_at,
            "max_activations": max_activations,
            "features": features,
            "notes": notes,
            "status": status
        }
    
    @staticmethod
    def generate_multiple_licenses(
        customer_id: int,
        application_id: int,
        count: int = 1
    ) -> List[Dict[str, Any]]:
        """Generate multiple random licenses for a customer-application pair"""
        licenses = []
        for i in range(count):
            license_data = LicenseDataGenerator.generate_license(customer_id, application_id)
            licenses.append(license_data)
        return licenses

class CompleteTestDataGenerator:
    """Generates complete test data sets for users"""
    
    @staticmethod
    def generate_user_with_data(
        username: str = None,
        email: str = None,
        full_name: str = None,
        password: str = None,
        description: str = None,
        app_count: int = None,
        customer_count: int = None,
        licenses_per_customer: int = None
    ) -> Dict[str, Any]:
        """Generate a complete user with applications, customers, and licenses"""
        
        # Generate user
        user = UserDataGenerator.generate_user_create(
            username=username,
            email=email,
            full_name=full_name,
            password=password,
            description=description
        )
        
        # Set default counts if not specified
        if app_count is None:
            app_count = random.randint(1, 4)
        if customer_count is None:
            customer_count = random.randint(2, 8)
        if licenses_per_customer is None:
            licenses_per_customer = random.randint(1, 3)
        
        # Generate applications (we'll need user_id later)
        applications = []
        for i in range(app_count):
            app = ApplicationDataGenerator.generate_application(user_id=0)  # Placeholder
            applications.append(app)
        
        # Generate customers
        customers = []
        for i in range(customer_count):
            customer = CustomerDataGenerator.generate_customer(user_id=0)  # Placeholder
            customers.append(customer)
        
        # Generate licenses for each customer-application combination
        all_licenses = []
        for customer in customers:
            for application in applications:
                licenses = LicenseDataGenerator.generate_multiple_licenses(
                    customer_id=0,  # Placeholder
                    application_id=0,  # Placeholder
                    count=licenses_per_customer
                )
                all_licenses.extend(licenses)
        
        return {
            "user": user,
            "applications": applications,
            "customers": customers,
            "licenses": all_licenses
        }
    
    @staticmethod
    def generate_multiple_users_with_data(
        user_count: int = 3,
        app_count_range: tuple = (1, 4),
        customer_count_range: tuple = (2, 8),
        licenses_per_customer_range: tuple = (1, 3)
    ) -> List[Dict[str, Any]]:
        """Generate multiple users with complete data sets"""
        users_with_data = []
        
        for i in range(user_count):
            app_count = random.randint(*app_count_range)
            customer_count = random.randint(*customer_count_range)
            licenses_per_customer = random.randint(*licenses_per_customer_range)
            
            user_data = CompleteTestDataGenerator.generate_user_with_data(
                app_count=app_count,
                customer_count=customer_count,
                licenses_per_customer=licenses_per_customer
            )
            
            users_with_data.append(user_data)
        
        return users_with_data

# Convenience functions for quick data generation
def generate_random_user() -> UserCreate:
    """Quick function to generate a random user"""
    return UserDataGenerator.generate_user_create()

def generate_random_application(user_id: int) -> Dict[str, Any]:
    """Quick function to generate a random application"""
    return ApplicationDataGenerator.generate_application(user_id)

def generate_random_customer(user_id: int) -> Dict[str, Any]:
    """Quick function to generate a random customer"""
    return CustomerDataGenerator.generate_customer(user_id)

def generate_random_license(customer_id: int, application_id: int) -> Dict[str, Any]:
    """Quick function to generate a random license"""
    return LicenseDataGenerator.generate_license(customer_id, application_id)

def generate_test_dataset(
    user_count: int = 3,
    apps_per_user: int = 2,
    customers_per_user: int = 5,
    licenses_per_customer: int = 1
) -> List[Dict[str, Any]]:
    """Generate a complete test dataset with multiple users"""
    return CompleteTestDataGenerator.generate_multiple_users_with_data(
        user_count=user_count,
        app_count_range=(1, apps_per_user),
        customer_count_range=(2, customers_per_user),
        licenses_per_customer_range=(1, licenses_per_customer)
    )
