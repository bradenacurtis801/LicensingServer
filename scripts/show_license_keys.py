#!/usr/bin/env python3
"""
Script to display license keys from the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select
from app.database.connection import engine
from app.models.database import LicenseKey, Customer, Application
from app.utils.license_generator import LicenseKeyGenerator

def show_license_keys():
    """Display all license keys in the database"""
    
    with Session(engine) as session:
        # Get all licenses with customer and application info
        licenses = session.exec(
            select(LicenseKey)
            .order_by(LicenseKey.id)
        ).all()
        
        if not licenses:
            print("❌ No license keys found in database")
            print("Run 'python scripts/create_sample_data.py' first")
            return
        
        print("🔑 License Keys in Database:")
        print("=" * 50)
        
        for i, license_key in enumerate(licenses, 1):
            # Get customer and application info
            customer = session.get(Customer, license_key.customer_id)
            application = session.get(Application, license_key.application_id)
            
            print(f"\n{i}. License ID: {license_key.id}")
            print(f"   Customer: {customer.name} ({customer.email})")
            print(f"   Application: {application.name} v{application.version}")
            print(f"   Status: {license_key.status}")
            print(f"   Expires: {license_key.expires_at or 'Never'}")
            print(f"   Max Activations: {license_key.max_activations}")
            print(f"   Current Activations: {license_key.current_activations}")
            print(f"   Notes: {license_key.notes}")
            
            # Try to reconstruct the license key from hash (for testing purposes)
            # Note: This is not secure in production, just for development testing
            print(f"   Key Hash: {license_key.key_hash[:20]}...")
            print()

def create_test_license():
    """Create a new test license and show its key"""
    
    with Session(engine) as session:
        # Get first customer and application
        customer = session.exec(select(Customer).limit(1)).first()
        application = session.exec(select(Application).limit(1)).first()
        
        if not customer or not application:
            print("❌ No customers or applications found")
            print("Run 'python scripts/create_sample_data.py' first")
            return
        
        # Generate new license
        generator = LicenseKeyGenerator()
        license_key = generator.generate_key()
        key_hash = generator.hash_key(license_key)
        
        # Create license record
        db_license = LicenseKey(
            key_hash=key_hash,
            customer_id=customer.id,
            application_id=application.id,
            expires_at=None,  # Perpetual
            max_activations=1,
            features='{"basic_features": true, "advanced_features": true, "premium_support": true}',
            notes="Test license for development",
            status="active"
        )
        
        session.add(db_license)
        session.commit()
        session.refresh(db_license)
        
        print("✅ Created new test license:")
        print(f"   License Key: {license_key}")
        print(f"   Customer: {customer.name}")
        print(f"   Application: {application.name}")
        print(f"   Status: {db_license.status}")
        print()

if __name__ == "__main__":
    print("License Key Display Tool")
    print("=" * 30)
    
    try:
        show_license_keys()
        
        print("\n" + "=" * 50)
        print("Create a new test license? (y/n): ", end="")
        response = input().strip().lower()
        
        if response in ['y', 'yes']:
            create_test_license()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure the database is running and accessible") 