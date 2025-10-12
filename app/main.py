# main.py
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
from typing import List
import logging.config

from app.config import settings
from app.database.connection import create_db_and_tables
from app.database.postgres import wait_for_postgres_ready, init_postgres_schema, check_postgres_connection
from app.api.v1.api import api_router
from app.core.exceptions import LicenseManagementException, map_to_http_exception
from app.core.constants import ensure_directories, LOGGING_CONFIG
from app.scripts.db_management import start_app_managed_postgres, stop_app_managed_postgres

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("app")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting License Management System...")
    logger.info("Creating application directories...")
    ensure_directories()
    
    # Start app-managed PostgreSQL container if enabled
    if settings.app_managed_db:
        logger.info("Starting app-managed PostgreSQL container...")
        start_app_managed_postgres()
    
    # Wait for PostgreSQL to be ready
    logger.info("Waiting for PostgreSQL to be ready...")
    try:
        await wait_for_postgres_ready()
        await init_postgres_schema()
    except Exception as e:
        logger.error(f"Failed to initialize PostgreSQL: {e}")
        raise
    
    logger.info("Application startup complete!")
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    # if settings.app_managed_db:
    #     logger.info("Stopping app-managed PostgreSQL container...")
    #     stop_app_managed_postgres()

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

# Add security schemes to OpenAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure OpenAPI security schemes
# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
    
#     openapi_schema = get_openapi(
#         title=app.title,
#         version=app.version,
#         description=app.description,
#         routes=app.routes,
#     )
    
#     # Add security schemes
#     openapi_schema["components"]["securitySchemes"] = {
#         "bearerAuth": {
#             "type": "http",
#             "scheme": "bearer",
#             "bearerFormat": "JWT",
#             "description": "JWT token or API token (starts with 'lt_')"
#         }
#             "description": "Username and password"
#         }
#     }
    
#     # REMOVED: Don't add global security requirements
#     # This allows each endpoint to specify its own security requirements
    
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema

# app.openapi = custom_openapi

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
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.backend_port,
        reload=settings.debug
    )
