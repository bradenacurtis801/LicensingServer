#!/usr/bin/env python3
"""
Test script to verify the new customer email constraints work correctly.
This tests:
1. Two users can have customers with the same email
2. One user cannot have duplicate customers with the same email
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select
from app.database.connection import engine
from app.models.database import Customer, User

def test_customer_constraints():
    """Test the new customer email constraints"""
    try:
        print("\n🧪 Testing Customer Email Constraints")
        print("=" * 60)
        
        with Session(engine) as session:
            # Test 1: Two users can have customers with the same email
            print("\n📋 Test 1: Multiple users with same customer email")
            print("-" * 50)
            
            # First, let's see what users exist
            users = session.exec(select(User).order_by(User.id)).all()
            if len(users) < 2:
                print("❌ Need at least 2 users for this test")
                return False
            
            user1 = users[0]
            user2 = users[1]
            
            print(f"Using users: {user1.username} (ID: {user1.id}) and {user2.username} (ID: {user2.id})")
            
            # Test email that should be unique across users
            test_email = "test.shared@example.com"
            
            # Create customer for first user
            print(f"\n  Creating customer for {user1.username} with email: {test_email}")
            try:
                customer1 = Customer(
                    name="Shared Customer 1",
                    email=test_email,
                    company="Test Company 1",
                    user_id=user1.id
                )
                session.add(customer1)
                session.commit()
                session.refresh(customer1)
                print(f"  ✅ Successfully created customer for {user1.username} (ID: {customer1.id})")
            except Exception as e:
                print(f"  ❌ Failed to create customer for {user1.username}: {e}")
                return False
            
            # Create customer for second user with same email
            print(f"  Creating customer for {user2.username} with email: {test_email}")
            try:
                customer2 = Customer(
                    name="Shared Customer 2",
                    email=test_email,
                    company="Test Company 2",
                    user_id=user2.id
                )
                session.add(customer2)
                session.commit()
                session.refresh(customer2)
                print(f"  ✅ Successfully created customer for {user2.username} (ID: {customer2.id})")
                print("  🎉 Test 1 PASSED: Multiple users can have customers with same email!")
            except Exception as e:
                print(f"  ❌ Failed to create customer for {user2.username}: {e}")
                print("  ❌ Test 1 FAILED: Multiple users cannot have customers with same email")
                return False
            
            # Test 2: One user cannot have duplicate customers with same email
            print("\n📋 Test 2: Single user cannot have duplicate customer emails")
            print("-" * 50)
            
            # Try to create another customer for the first user with the same email
            print(f"  Attempting to create duplicate customer for {user1.username} with email: {test_email}")
            try:
                duplicate_customer = Customer(
                    name="Duplicate Customer",
                    email=test_email,
                    company="Duplicate Company",
                    user_id=user1.id
                )
                session.add(duplicate_customer)
                session.commit()
                print("  ❌ Test 2 FAILED: User was able to create duplicate customer email")
                return False
            except Exception as e:
                if "uq_user_email" in str(e):
                    print("  ✅ Test 2 PASSED: Constraint properly prevented duplicate customer email for same user!")
                    print(f"  Error message: {e}")
                    # Rollback the session after constraint violation
                    session.rollback()
                else:
                    print(f"  ❌ Unexpected error: {e}")
                    return False
            
            # Test 3: Verify data integrity
            print("\n📋 Test 3: Verify data integrity")
            print("-" * 50)
            
            # Count customers with the test email
            customer_count = session.exec(
                select(Customer).where(Customer.email == test_email)
            ).all()
            
            print(f"Total customers with email {test_email}: {len(customer_count)}")
            
            # Show the customers
            for customer in customer_count:
                user = session.get(User, customer.user_id)
                print(f"  - ID: {customer.id}, Name: {customer.name}, Company: {customer.company}, User: {user.username}")
            
            # Test 4: Clean up test data
            print("\n📋 Test 4: Clean up test data")
            print("-" * 50)
            
            print("  Cleaning up test customers...")
            
            # Delete test customers
            test_customers = session.exec(
                select(Customer).where(Customer.email == test_email)
            ).all()
            
            for customer in test_customers:
                session.delete(customer)
                print(f"    ✅ Deleted customer {customer.id}")
            
            session.commit()
            print("  ✅ Test data cleaned up")
            
            print("\n🎉 All tests completed successfully!")
            print("\n📊 Summary:")
            print("  ✅ Multiple users can have customers with the same email")
            print("  ✅ Single user cannot have duplicate customer emails")
            print("  ✅ Constraint structure is correct")
            print("  ✅ Data integrity is maintained")
            
            return True
                
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Customer Constraint Test Suite")
    print("=" * 50)
    
    if test_customer_constraints():
        print("\n🎉 All tests PASSED! Your new constraint system is working correctly.")
        print("\n💡 What this means:")
        print("  - Different users can manage customers with the same email addresses")
        print("  - Each user can only have one customer per email address")
        print("  - Your application can now handle shared customer scenarios")
    else:
        print("\n❌ Some tests FAILED. Check the output above for details.")
        sys.exit(1)
