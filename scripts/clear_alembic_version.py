#!/usr/bin/env python3
"""
Script to clear the alembic_version table from the database.
This is needed when you want to start fresh with Alembic migrations.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from sqlalchemy import create_engine, text
from app.core.constants import PROJECT_ROOT

def load_env_file():
    """Load environment variables from .env file"""
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

def get_database_url():
    """Get database URL from environment variables"""
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url
    
    # Construct from individual variables
    postgres_db = os.getenv("POSTGRES_DB_NAME", "authdb")
    postgres_host = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port = os.getenv("POSTGRES_PORT", "5432")
    postgres_user = os.getenv("POSTGRES_USERNAME", "postgres")
    postgres_password = os.getenv("POSTGRES_PASSWORD", "supersecurepassword")
    
    return f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"

def clear_alembic_version():
    """Clear the alembic_version table"""
    try:
        # Load environment variables
        load_env_file()
        
        # Get database URL
        database_url = get_database_url()
        print(f"Connecting to database: {database_url.split('@')[1]}")  # Don't show password
        
        # Create engine
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Check if alembic_version table exists
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'alembic_version'
                );
            """))
            
            if result.scalar():
                print("Found alembic_version table, clearing it...")
                conn.execute(text("DELETE FROM alembic_version;"))
                conn.commit()
                print("✅ Successfully cleared alembic_version table")
            else:
                print("✅ No alembic_version table found (already clean)")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🧹 Clearing Alembic version table...")
    if clear_alembic_version():
        print("\n🎉 Database is now clean and ready for new Alembic migrations!")
        print("You can now run: python -m alembic revision --autogenerate -m 'baseline'")
    else:
        print("\n❌ Failed to clear Alembic version table")
        sys.exit(1)
