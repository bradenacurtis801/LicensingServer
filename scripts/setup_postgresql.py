#!/usr/bin/env python3
"""
PostgreSQL setup script for License Management System
"""
import os
import sys
import subprocess
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_postgresql_installed():
    """Check if PostgreSQL is installed"""
    try:
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"PostgreSQL found: {result.stdout.strip()}")
            return True
        else:
            logger.error("PostgreSQL not found in PATH")
            return False
    except FileNotFoundError:
        logger.error("PostgreSQL not installed or not in PATH")
        return False

def create_database():
    """Create the database if it doesn't exist"""
    # Parse connection string
    # postgresql://postgres:password@localhost/license_db
    parts = settings.database_url.replace('postgresql://', '').split('/')
    auth_host = parts[0]
    db_name = parts[1]
    
    user_pass, host = auth_host.split('@')
    user, password = user_pass.split(':')
    
    try:
        # Connect to PostgreSQL server (not specific database)
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database='postgres'  # Default database
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()
        
        if not exists:
            logger.info(f"Creating database: {db_name}")
            cursor.execute(f"CREATE DATABASE {db_name}")
            logger.info(f"Database '{db_name}' created successfully")
        else:
            logger.info(f"Database '{db_name}' already exists")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        return False

def test_connection():
    """Test the database connection"""
    try:
        from app.database.connection import engine
        from sqlmodel import SQLModel
        
        # Test connection
        with engine.connect() as conn:
            logger.info("✅ Database connection successful")
        
        # Test table creation
        SQLModel.metadata.create_all(engine)
        logger.info("✅ Table creation successful")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🐘 PostgreSQL Setup for License Management System")
    print("=" * 50)
    
    # Check PostgreSQL installation
    if not check_postgresql_installed():
        print("\n❌ PostgreSQL not found!")
        print("Please install PostgreSQL first:")
        print("  - Windows: Download from https://www.postgresql.org/download/windows/")
        print("  - macOS: brew install postgresql")
        print("  - Ubuntu: sudo apt-get install postgresql postgresql-contrib")
        return False
    
    # Create database
    if not create_database():
        print("\n❌ Failed to create database!")
        print("Please check your PostgreSQL credentials in config.py")
        return False
    
    # Test connection
    if not test_connection():
        print("\n❌ Failed to connect to database!")
        return False
    
    print("\n✅ PostgreSQL setup completed successfully!")
    print("\nNext steps:")
    print("1. Update your .env file with correct PostgreSQL credentials")
    print("2. Run: python run_server.py")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 