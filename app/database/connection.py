# app/database/connection.py
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
import logging
from app.config import settings
from app.core.constants import get_database_config, is_docker_environment

# Set up logger
logger = logging.getLogger(__name__)

def get_database_type():
    """Detect database type from URL"""
    db_url = settings.database_url.lower()
    if db_url.startswith("postgresql"):
        return "PostgreSQL"
    elif db_url.startswith("mysql"):
        return "MySQL"
    else:
        return "Unknown"

# Get database configuration based on environment
env = "docker" if is_docker_environment() else "development"
db_config = get_database_config(env)

# PostgreSQL connection
connect_args = {}

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    connect_args=connect_args,
    pool_pre_ping=db_config["pool_pre_ping"],
    pool_recycle=db_config["pool_recycle"],
    pool_size=db_config["pool_size"],
    max_overflow=db_config["max_overflow"]
)

def create_db_and_tables():
    """Create database tables"""
    db_type = get_database_type()
    logger.info(f"Creating {db_type} database tables for environment: {env}")
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables created successfully")

def get_session() -> Generator[Session, None, None]:
    """Get database session"""
    with Session(engine) as session:
        yield session