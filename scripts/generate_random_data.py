"""
Example script showing how to use the test data generator utilities.
Run this to see examples of randomly generated data.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.test_data_generator import (
    generate_random_user,
    generate_random_application,
    generate_random_customer,
    generate_random_license,
    generate_test_dataset,
    UserDataGenerator,
    ApplicationDataGenerator,
    CustomerDataGenerator,
    LicenseDataGenerator,
    CompleteTestDataGenerator
)

def demonstrate_individual_generators():
    """Show examples of individual data generators"""
    print("\n🔧 Individual Data Generators")
    print("=" * 50)
    
    # Generate a random user
    print("\n👤 Random User:")
    user = generate_random_user()
    print(f"  Username: {user.username}")
    print(f"  Email: {user.email}")
    print(f"  Full Name: {user.full_name}")
    # Note: business_role and system_role are assigned after user creation, not during
    
    # Generate a random application
    print("\n📱 Random Application:")
    app = generate_random_application(user_id=1)
    print(f"  Name: {app['name']}")
    print(f"  Version: {app['version']}")
    print(f"  Category: {app['category']}")
    print(f"  Platform: {app['platform']}")
    print(f"  Features: {len([f for f in app['features'].values() if f])} enabled")
    
    # Generate a random customer
    print("\n👥 Random Customer:")
    customer = generate_random_customer(user_id=1)
    print(f"  Name: {customer['name']}")
    print(f"  Email: {customer['email']}")
    print(f"  Company: {customer['company']}")
    print(f"  Phone: {customer['phone']}")
    
    # Generate a random license
    print("\n🔑 Random License:")
    license_data = generate_random_license(customer_id=1, application_id=1)
    print(f"  Max Activations: {license_data['max_activations']}")
    print(f"  Expires At: {license_data['expires_at']}")
    print(f"  Status: {license_data['status']}")
    print(f"  Notes: {license_data['notes']}")

def demonstrate_bulk_generation():
    """Show examples of bulk data generation"""
    print("\n\n📊 Bulk Data Generation")
    print("=" * 50)
    
    # Generate multiple users
    print("\n👥 Multiple Users:")
    users = UserDataGenerator.generate_multiple_users(count=3)
    for i, user in enumerate(users, 1):
        print(f"  {i}. {user.username} ({user.email})")
    
    # Generate multiple applications for a user
    print("\n📱 Multiple Applications:")
    apps = ApplicationDataGenerator.generate_multiple_applications(user_id=1, count=3)
    for i, app in enumerate(apps, 1):
        print(f"  {i}. {app['name']} v{app['version']} - {app['category']}")
    
    # Generate multiple customers for a user
    print("\n👥 Multiple Customers:")
    customers = CustomerDataGenerator.generate_multiple_customers(user_id=1, count=4)
    for i, customer in enumerate(customers, 1):
        company_info = f" ({customer['company']})" if customer['company'] else ""
        print(f"  {i}. {customer['name']}{company_info} - {customer['email']}")

def demonstrate_complete_datasets():
    """Show examples of complete dataset generation"""
    print("\n\n🎯 Complete Dataset Generation")
    print("=" * 50)
    
    # Generate a single user with complete data
    print("\n👤 Single User with Complete Data:")
    user_data = CompleteTestDataGenerator.generate_user_with_data(
        username="testuser",
        app_count=2,
        customer_count=3,
        licenses_per_customer=2
    )
    
    print(f"  User: {user_data['user'].username}")
    print(f"  Applications: {len(user_data['applications'])}")
    print(f"  Customers: {len(user_data['customers'])}")
    print(f"  Licenses: {len(user_data['licenses'])}")
    
    # Generate a complete test dataset
    print("\n📊 Complete Test Dataset:")
    dataset = generate_test_dataset(
        user_count=2,
        apps_per_user=2,
        customers_per_user=3,
        licenses_per_customer=1
    )
    
    total_apps = sum(len(user['applications']) for user in dataset)
    total_customers = sum(len(user['customers']) for user in dataset)
    total_licenses = sum(len(user['licenses']) for user in dataset)
    
    print(f"  Total Users: {len(dataset)}")
    print(f"  Total Applications: {total_apps}")
    print(f"  Total Customers: {total_customers}")
    print(f"  Total Licenses: {total_licenses}")

def demonstrate_customization():
    """Show examples of customizing generated data"""
    print("\n\n⚙️  Data Customization")
    print("=" * 50)
    
    # Custom user with specific attributes
    print("\n👤 Custom User:")
    custom_user = UserDataGenerator.generate_user_create()
    print(f"  Username: {custom_user.username}")
    print(f"  Email: {custom_user.email}")
    # Note: business_role and system_role are not available on UserCreate objects
    
    # Custom application with specific features
    print("\n📱 Custom Application:")
    custom_features = {
        "basic_features": True,
        "advanced_features": True,
        "premium_support": True,
        "cloud_sync": False,
        "offline_mode": True
    }
    
    custom_app = ApplicationDataGenerator.generate_application(
        user_id=1,
        name="CustomApp",
        category="Security",
        platform="Desktop",
        features=custom_features
    )
    print(f"  Name: {custom_app['name']}")
    print(f"  Category: {custom_app['category']}")
    print(f"  Platform: {custom_app['platform']}")
    print(f"  Features: {custom_features}")

def main():
    """Main demonstration function"""
    print("🚀 Test Data Generator Utilities Demo")
    print("=" * 60)
    
    try:
        demonstrate_individual_generators()
        demonstrate_bulk_generation()
        demonstrate_complete_datasets()
        demonstrate_customization()
        
        print("\n\n✅ Demo completed successfully!")
        print("\n💡 Usage Tips:")
        print("  - Use individual generators for specific data needs")
        print("  - Use bulk generators for testing multiple scenarios")
        print("  - Use complete dataset generators for integration testing")
        print("  - Customize any field by passing specific values")
        print("  - All data is realistic and follows your schema requirements")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
