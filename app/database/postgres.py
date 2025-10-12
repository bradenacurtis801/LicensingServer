import asyncio
import socket
import time
import logging
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from app.config import settings

# Set up logger
logger = logging.getLogger(__name__)

# Create async engine for PostgreSQL
async_engine = create_async_engine(
    settings.database_url.replace("postgresql://", "postgresql+asyncpg://", 1),
    echo=settings.debug,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=10
)

# Create async session factory
async_session = sessionmaker(
    async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_async_session() -> AsyncSession:
    """Get async database session"""
    async with async_session() as session:
        yield session

async def wait_for_postgres_ready(uri: str = None, timeout: int = 30):
    """Wait for PostgreSQL to be ready"""
    if uri is None:
        uri = settings.database_url
    
    # Convert to asyncpg format
    raw_uri = uri.replace("postgresql://", "postgresql+asyncpg://", 1)
    logger.info(f"Waiting for PostgreSQL at {uri}")
    
    start = asyncio.get_event_loop().time()
    while True:
        try:
            conn = await asyncpg.connect(raw_uri.replace("postgresql+asyncpg://", "postgresql://", 1))
            await conn.execute("SELECT 1")
            await conn.close()
            logger.info("PostgreSQL is ready")
            return
        except Exception as e:
            if asyncio.get_event_loop().time() - start > timeout:
                raise TimeoutError(f"PostgreSQL did not become ready: {e}")
            logger.info(f"Still waiting... ({asyncio.get_event_loop().time() - start:.1f}s)")
            await asyncio.sleep(1)

async def init_postgres_schema():
    """Initialize PostgreSQL schema"""
    logger.info("Initializing PostgreSQL schema...")
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    logger.info("PostgreSQL schema initialized")

async def check_postgres_connection():
    """Check if PostgreSQL connection is working"""
    try:
        async with async_engine.begin() as conn:
            result = await conn.execute("SELECT 1")
            logger.info("PostgreSQL connection successful")
            return True
    except Exception as e:
        logger.error(f"PostgreSQL connection failed: {e}")
        return False 