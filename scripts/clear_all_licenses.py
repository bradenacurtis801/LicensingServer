#!/usr/bin/env python3
"""Script to clear all license keys from the database"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select
from app.database.connection import engine
from app.models.database import LicenseKey, Customer, Application, User

def clear_all_licenses():
    """Clear all license keys from the database"""
    try:
        print("🗑️  Clearing all license keys from database...")
        print("=" * 60)
        
        with Session(engine) as session:
            # Get count of existing licenses
            license_count = session.exec(select(LicenseKey)).all()
            print(f"Found {len(license_count)} existing licenses")
            
            if not license_count:
                print("✅ No licenses to clear")
                return
            
            # Show what we're about to delete
            print("\n📋 Licenses to be deleted:")
            for license_key in license_count:
                # Get customer and application info
                customer = session.get(Customer, license_key.customer_id)
                application = session.get(Application, license_key.application_id)
                user = session.get(User, customer.user_id) if customer else None
                
                if customer and application and user:
                    print(f"  - {user.username}: {customer.name} - {application.name} (ID: {license_key.id})")
                else:
                    print(f"  - License ID: {license_key.id} (orphaned)")
            
            # Confirm deletion
            print(f"\n⚠️  This will permanently delete {len(license_count)} license keys!")
            response = input("Are you sure? Type 'YES' to confirm: ")
            
            if response != "YES":
                print("❌ Operation cancelled")
                return
            
            # Delete all licenses
            print("\n🗑️  Deleting licenses...")
            deleted_count = 0
            
            for license_key in license_count:
                try:
                    session.delete(license_key)
                    deleted_count += 1
                    print(f"  ✅ Deleted license ID: {license_key.id}")
                except Exception as e:
                    print(f"  ❌ Failed to delete license ID {license_key.id}: {e}")
            
            # Commit the changes
            session.commit()
            
            print(f"\n🎉 Successfully deleted {deleted_count} out of {len(license_count)} licenses")
            
            # Verify deletion
            remaining_licenses = session.exec(select(LicenseKey)).all()
            print(f"📊 Remaining licenses in database: {len(remaining_licenses)}")
            
            if len(remaining_licenses) == 0:
                print("✅ All licenses successfully cleared!")
            else:
                print("⚠️  Some licenses may not have been deleted")
                
    except Exception as e:
        print(f"❌ Error during license clearing: {e}")
        return False
    
    return True

def clear_licenses_for_user(username: str):
    """Clear licenses for a specific user only"""
    try:
        print(f"🗑️  Clearing licenses for user: {username}")
        print("=" * 60)
        
        with Session(engine) as session:
            # Find the user
            user = session.exec(select(User).where(User.username == username)).first()
            if not user:
                print(f"❌ User '{username}' not found")
                return False
            
            # Get all customers for this user
            customers = session.exec(select(Customer).where(Customer.user_id == user.id)).all()
            if not customers:
                print(f"✅ User '{username}' has no customers")
                return True
            
            # Get all licenses for these customers
            customer_ids = [c.id for c in customers]
            licenses = session.exec(
                select(LicenseKey).where(LicenseKey.customer_id.in_(customer_ids))
            ).all()
            
            if not licenses:
                print(f"✅ User '{username}' has no licenses")
                return True
            
            print(f"Found {len(licenses)} licenses for user '{username}'")
            
            # Show what we're about to delete
            print("\n📋 Licenses to be deleted:")
            for license_key in licenses:
                customer = session.get(Customer, license_key.customer_id)
                application = session.get(Application, license_key.application_id)
                if customer and application:
                    print(f"  - {customer.name} - {application.name} (ID: {license_key.id})")
            
            # Confirm deletion
            print(f"\n⚠️  This will delete {len(licenses)} licenses for user '{username}'!")
            response = input("Are you sure? Type 'YES' to confirm: ")
            
            if response != "YES":
                print("❌ Operation cancelled")
                return False
            
            # Delete licenses
            print("\n🗑️  Deleting licenses...")
            deleted_count = 0
            
            for license_key in licenses:
                try:
                    session.delete(license_key)
                    deleted_count += 1
                    print(f"  ✅ Deleted license ID: {license_key.id}")
                except Exception as e:
                    print(f"  ❌ Failed to delete license ID {license_key.id}: {e}")
            
            # Commit the changes
            session.commit()
            
            print(f"\n🎉 Successfully deleted {deleted_count} licenses for user '{username}'")
            
    except Exception as e:
        print(f"❌ Error during license clearing: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🗑️  License Clearing Script")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        # Clear licenses for specific user
        username = sys.argv[1]
        clear_licenses_for_user(username)
    else:
        # Clear all licenses
        print("Usage:")
        print("  python scripts/clear_all_licenses.py          # Clear all licenses")
        print("  python scripts/clear_all_licenses.py admin    # Clear licenses for specific user")
        print()
        
        clear_all_licenses()
