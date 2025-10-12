#!/usr/bin/env python3
"""
Clear all data from the database
"""
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session
from sqlalchemy import text
from app.database.connection import engine, create_db_and_tables
from app.models.database import Customer, Application, LicenseKey, Activation, ActivationForm, OfflineActivationCode

def clear_database():
    """Clear all data from the database"""
    print("🗑️  Clearing database...")
    
    with Session(engine) as session:
        # Delete in reverse order of dependencies
        session.exec(text("DELETE FROM offlineactivationcode"))
        session.exec(text("DELETE FROM activationform"))
        session.exec(text("DELETE FROM activation"))
        session.exec(text("DELETE FROM licensekey"))
        session.exec(text("DELETE FROM application"))
        session.exec(text("DELETE FROM customer"))
        
        session.commit()
    
    print("✅ Database cleared successfully!")

if __name__ == "__main__":
    clear_database() 