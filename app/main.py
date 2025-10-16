# main.py
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
from typing import List
import logging.config

import app.config as config
from app.config import settings
from app.database.connection import create_db_and_tables
from app.database.postgres import wait_for_postgres_ready, init_postgres_schema, check_postgres_connection
from app.api.v1.api import api_router
from app.graphql.schema import schema
from app.graphql.context import get_graphql_context
from strawberry.fastapi import GraphQLRouter
from strawberry.asgi import GraphQL
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

# Add debug middleware to log all requests
@app.middleware("http")
async def debug_middleware(request: Request, call_next):
    print(f"🔍 DEBUG: Incoming request: {request.method} {request.url}")
    print(f"🔍 DEBUG: Headers: {dict(request.headers)}")
    
    # Highlight preflight requests
    if request.method == "OPTIONS":
        print("🚨 PREFLIGHT REQUEST DETECTED!")
        print(f"🚨 Origin: {request.headers.get('origin')}")
        print(f"🚨 Access-Control-Request-Method: {request.headers.get('access-control-request-method')}")
        print(f"🚨 Access-Control-Request-Headers: {request.headers.get('access-control-request-headers')}")
    
    # Highlight requests with Authorization header
    auth_header = request.headers.get('authorization') or request.headers.get('Authorization')
    if auth_header:
        print(f"🔑 AUTHORIZATION HEADER FOUND: {auth_header}")
    else:
        print("❌ NO AUTHORIZATION HEADER")
    
    response = await call_next(request)
    print(f"🔍 DEBUG: Response status: {response.status_code}")
    
    # Log CORS response headers
    cors_headers = {k: v for k, v in response.headers.items() if k.lower().startswith('access-control')}
    if cors_headers:
        print(f"🌐 CORS Response headers: {cors_headers}")
    
    return response

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

# Add GraphQL endpoint
graphql_app = GraphQLRouter(schema, context_getter=get_graphql_context)
app.include_router(graphql_app, prefix="/graphql")

app.add_route("/graphql-playground", GraphQL(schema))


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

# Debug endpoint for OPTIONS requests
@app.options("/{path:path}")
async def debug_options(path: str, request: Request):
    """Debug endpoint to handle OPTIONS requests"""
    print(f"🚨 OPTIONS request to: /{path}")
    print(f"🚨 Origin: {request.headers.get('origin')}")
    print(f"🚨 Access-Control-Request-Method: {request.headers.get('access-control-request-method')}")
    print(f"🚨 Access-Control-Request-Headers: {request.headers.get('access-control-request-headers')}")
    
    # Return a proper CORS response
    from fastapi.responses import Response
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": request.headers.get('origin', '*'),
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Allow-Credentials": "true",
        }
    )

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
