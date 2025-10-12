# endpoints/auth.py
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import HTTPBearer
from typing import List

from app.services.auth_service import AuthService
from app.models.schemas import (
    UserCreate, UserResponse, UserUpdate, UserLogin, UserChangePassword,
    APITokenCreate, APITokenResponse, APITokenCreateResponse, APITokenUpdate,
    TokenResponse, UserBusinessRoleUpdate, UserSystemRoleUpdate
)
from app.models.database import User
from app.dependencies import (
    get_auth_service, get_current_user,
    require_user_management, require_token_management
)
from app.core.exceptions import InvalidCredentialsException
from app.models.database import UserRole

router = APIRouter()

# Authentication endpoints (public)
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
) -> UserResponse:
    """Register a new user (public endpoint for first user, or admin-only)"""
    return auth_service.create_user(user_data)

@router.post("/login", response_model=TokenResponse)
def login(
    login_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
) -> TokenResponse:
    """Login and get session token"""
    user = auth_service.authenticate_user(login_data.username, login_data.password)
    if not user:
        raise InvalidCredentialsException("Incorrect username or password")
    
    return auth_service.create_login_session(user)

# Protected endpoints (require authentication)
@router.post("/change-password")
def change_password(
    password_data: UserChangePassword,
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Change current user's password"""
    return auth_service.change_password(current_user.id, password_data)

@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """Get current user information"""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        business_role=current_user.business_role,
        system_role=current_user.system_role,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )

# API Token Management
@router.post("/tokens", response_model=APITokenCreateResponse, status_code=status.HTTP_201_CREATED)
def create_api_token(
    token_data: APITokenCreate,
    current_user: User = Depends(require_token_management()),
    auth_service: AuthService = Depends(get_auth_service)
) -> APITokenCreateResponse:
    """Create a new API token"""
    return auth_service.create_api_token(current_user, token_data)

@router.get("/tokens", response_model=List[APITokenResponse])
def list_api_tokens(
    current_user: User = Depends(require_token_management()),
    auth_service: AuthService = Depends(get_auth_service)
) -> List[APITokenResponse]:
    """List current user's API tokens"""
    return auth_service.list_api_tokens(current_user.id)

@router.put("/tokens/{token_id}", response_model=APITokenResponse)
def update_api_token(
    token_id: int,
    token_update: APITokenUpdate,
    current_user: User = Depends(require_token_management()),
    auth_service: AuthService = Depends(get_auth_service)
) -> APITokenResponse:
    """Update an API token (full update)"""
    return auth_service.update_api_token(current_user.id, token_id, token_update)

@router.patch("/tokens/{token_id}", response_model=APITokenResponse)
def patch_api_token(
    token_id: int,
    token_update: APITokenUpdate,
    current_user: User = Depends(require_token_management()),
    auth_service: AuthService = Depends(get_auth_service)
) -> APITokenResponse:
    """Partially update an API token (incremental changes)"""
    return auth_service.update_api_token(current_user.id, token_id, token_update)

@router.delete("/tokens/{token_id}")
def delete_api_token(
    token_id: int,
    current_user: User = Depends(require_token_management()),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Delete an API token"""
    return auth_service.delete_api_token(current_user.id, token_id)

# User Management (Admin endpoints)
@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    current_user: User = Depends(require_user_management()),
    auth_service: AuthService = Depends(get_auth_service)
) -> UserResponse:
    """Create a new user (admin only)"""
    return auth_service.create_user(user_data)

@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_user_management()),
    auth_service: AuthService = Depends(get_auth_service)
) -> List[UserResponse]:
    """Get all users (admin only)"""
    return auth_service.get_all_users(skip=skip, limit=limit)

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    current_user: User = Depends(require_user_management()),
    auth_service: AuthService = Depends(get_auth_service)
) -> UserResponse:
    """Get user by ID (admin only)"""
    return auth_service.get_user(user_id)

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    update_data: UserUpdate,
    current_user: User = Depends(require_user_management()),
    auth_service: AuthService = Depends(get_auth_service)
) -> UserResponse:
    """Update user (admin only)"""
    return auth_service.update_user(user_id, update_data)

@router.put("/users/{user_id}/business-role", response_model=UserResponse)
def update_user_business_role(
    user_id: int,
    role_update: UserBusinessRoleUpdate,
    current_user: User = Depends(require_user_management()),
    auth_service: AuthService = Depends(get_auth_service)
) -> UserResponse:
    """Update user business role (system admin only) - only USER role available"""
    return auth_service.update_user_business_role(user_id, role_update.business_role, current_user)

@router.put("/users/{user_id}/system-role", response_model=UserResponse)
def update_user_system_role(
    user_id: int,
    role_update: UserSystemRoleUpdate,
    current_user: User = Depends(require_user_management()),
    auth_service: AuthService = Depends(get_auth_service)
) -> UserResponse:
    """Update user system role (system admin only)"""
    return auth_service.update_user_system_role(user_id, role_update.system_role, current_user)
