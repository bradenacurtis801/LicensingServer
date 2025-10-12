# main.py
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
from typing import List
import logging.config
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

import app.config as config
from app.config import settings
from app.database.connection import create_db_and_tables
from app.database.postgres import wait_for_postgres_ready, init_postgres_schema, check_postgres_connection
from app.api.v1.api import api_router
from app.core.exceptions import LicenseManagementException, map_to_http_exception
from app.core.constants import ensure_directories, LOGGING_CONFIG
from app.core.rate_limiting import limiter
from app.core.signing import init_signing_key

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("app")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting License Management System...")
    logger.info("Creating application directories...")
    ensure_directories()
    
    # Wait for PostgreSQL to be ready
    logger.info("Waiting for PostgreSQL to be ready...")
    try:
        await wait_for_postgres_ready()
        await init_postgres_schema()
    except Exception as e:
        logger.error(f"Failed to initialize PostgreSQL: {e}")
        raise
    
    init_signing_key(settings.rsa_private_key_path)
    logger.info("Application startup complete!")
    yield
    
    # Shutdown
    logger.info("Shutting down application...")

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
    openapi_tags=[
        {"name": "Authentication", "description": "User authentication and authorization endpoints"},
        {"name": "Applications", "description": "Application management endpoints"},
        {"name": "Customers", "description": "Customer management endpoints"},
        {"name": "Licenses", "description": "License management endpoints"},
        {"name": "Activations", "description": "License activation endpoints"},
        {"name": "Validation", "description": "License validation endpoints"},
        {"name": "Activation Forms", "description": "Activation form management endpoints"},
    ]
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

cors_origins = settings.cors_origins

# In development, allow all origins for easier debugging
if config.is_development:
    cors_origins = ["*"]  # Allow all origins in development

# Add security schemes to OpenAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    logger.debug(f"{request.method} {request.url}")
    if request.method == "OPTIONS":
        logger.debug(f"Preflight from origin: {request.headers.get('origin')}")
    response = await call_next(request)
    logger.debug(f"Response: {response.status_code}")
    return response

# Global exception handler
@app.exception_handler(LicenseManagementException)
async def license_exception_handler(request: Request, exc: LicenseManagementException):
    http_exc = map_to_http_exception(exc)
    return JSONResponse(
        status_code=http_exc.status_code,
        content={"detail": http_exc.detail}
    )

# Include API routes
app.include_router(api_router, prefix=settings.api_v1_prefix)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db_status = "unknown"
    try:
        db_status = "healthy" if await check_postgres_connection() else "unhealthy"
    except:
        db_status = "unhealthy"
    
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "database": db_status
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with basic information"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs_url": "/docs",
        "health_url": "/health"
    }
if __name__ == "__main__":
    import uvicorn

    host = settings.backend_host if config.is_production else "0.0.0.0"

    uvicorn.run(
        "app.main:app",
        host=host,
        port=settings.backend_port,
        reload=settings.debug
    )
