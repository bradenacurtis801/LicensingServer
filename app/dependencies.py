# dependencies.py
from typing import Generator, List, Optional, Annotated
from sqlmodel import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database.connection import get_session
from app.services.customer_service import CustomerService
from app.services.application_service import ApplicationService
from app.services.license_service import LicenseService
from app.services.activation_service import ActivationService
from app.services.validation_service import ValidationService
from app.services.activation_form_service import ActivationFormService
from app.services.auth_service import AuthService
from app.models.database import User, TokenScope
from app.core.auth_config import get_user_permissions

# Security scheme
security = HTTPBearer(auto_error=False)  # ← Don't raise error if missing

def get_db() -> Session:
    """Database dependency"""
    return next(get_session())

def get_auth_service(db: Session = Depends(get_session)) -> AuthService:
    return AuthService(db)

def get_customer_service(db: Session = Depends(get_session)) -> CustomerService:
    return CustomerService(db)

def get_application_service(db: Session = Depends(get_session)) -> ApplicationService:
    return ApplicationService(db)

def get_license_service(db: Session = Depends(get_session)) -> LicenseService:
    return LicenseService(db)

def get_activation_service(db: Session = Depends(get_session)) -> ActivationService:
    return ActivationService(db)

def get_validation_service(db: Session = Depends(get_session)) -> ValidationService:
    return ValidationService(db)

def get_activation_form_service(db: Session = Depends(get_session)) -> ActivationFormService:
    return ActivationFormService(db)

# Unified authentication - handles both session tokens and API tokens
async def get_current_user(
    bearer_credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> User:
    """Get current user from session token or API token"""
    
    if not bearer_credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = bearer_credentials.credentials
    
    # Try API token first (they start with 'lt_')
    if token.startswith('lt_'):
        result = auth_service.verify_api_token(token)
        if result:
            user, scopes = result
            return user
    
    # Try session token (they start with 'st_')
    if token.startswith('st_'):
        user = auth_service.verify_session_token(token)
        if user:
            return user
    
    # If neither worked, raise authentication error
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )

# For endpoints that need scopes - accepts both session tokens (full permissions) and API tokens (subset permissions)
async def get_current_user_with_scopes(
    bearer_credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> tuple[User, List[TokenScope]]:
    """Get current user and scopes - accepts both session tokens (full) and API tokens (subset)"""
    if not bearer_credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = bearer_credentials.credentials
    
    # Try API token first (they start with 'lt_')
    if token.startswith('lt_'):
        result = auth_service.verify_api_token(token)
        if result:
            return result
    
    # Try session token (they start with 'st_') - session tokens have full permissions
    if token.startswith('st_'):
        user = auth_service.verify_session_token(token)
        if user:
            # Session tokens have all permissions based on user's roles
            from app.core.auth_config import get_user_permissions
            permissions = get_user_permissions(user.business_role, user.system_role)
            return user, permissions
    
    # If neither worked, raise authentication error
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )

# Scope-based permission dependencies
def require_scope(required_scope: TokenScope):
    """Dependency factory for scope-based permissions - accepts both session and API tokens"""
    async def check_scope(
        user_and_scopes: tuple[User, List[TokenScope]] = Depends(get_current_user_with_scopes)
    ) -> User:
        user, scopes = user_and_scopes
        if required_scope not in scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required scope: {required_scope}"
            )
        return user
    return check_scope

# Convenient permission dependencies
def require_license_read():
    """Require license read scope"""
    return require_scope(TokenScope.LICENSE_READ)

def require_license_write():
    """Require license write scope"""
    return require_scope(TokenScope.LICENSE_WRITE)

def require_license_delete():
    """Require license delete scope"""
    return require_scope(TokenScope.LICENSE_DELETE)

def require_customer_read():
    """Require customer read scope"""
    return require_scope(TokenScope.CUSTOMER_READ)

def require_customer_write():
    """Require customer write scope"""
    return require_scope(TokenScope.CUSTOMER_WRITE)

def require_customer_delete():
    """Require customer delete scope"""
    return require_scope(TokenScope.CUSTOMER_DELETE)

def require_application_read():
    """Require application read scope"""
    return require_scope(TokenScope.APPLICATION_READ)

def require_application_write():
    """Require application write scope"""
    return require_scope(TokenScope.APPLICATION_WRITE)

def require_application_delete():
    """Require application delete scope"""
    return require_scope(TokenScope.APPLICATION_DELETE)

def require_activation_read():
    """Require activation read scope"""
    return require_scope(TokenScope.ACTIVATION_READ)

def require_activation_write():
    """Require activation write scope"""
    return require_scope(TokenScope.ACTIVATION_WRITE)

def require_activation_delete():
    """Require activation delete scope"""
    return require_scope(TokenScope.ACTIVATION_DELETE)

def require_validation():
    """Require validation scope"""
    return require_scope(TokenScope.VALIDATION)

def require_user_management():
    """Require user management scope"""
    return require_scope(TokenScope.USER_MANAGEMENT)

def require_token_management():
    """Require token management scope"""
    return require_scope(TokenScope.TOKEN_MANAGEMENT)

# Role-based dependencies (for backward compatibility)
def require_admin():
    """Require admin role"""
    async def check_admin(current_user: User = Depends(get_current_user)) -> User:
        if current_user.system_role != "system_admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        return current_user
    return check_admin

def require_manager_or_above():
    """Require manager or admin role"""
    async def check_manager(current_user: User = Depends(get_current_user)) -> User:
        if current_user.system_role not in ["system_admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Manager or admin access required"
            )
        return current_user
    return check_manager

def require_developer_or_above():
    """Require developer, manager, or admin role"""
    async def check_developer(current_user: User = Depends(get_current_user)) -> User:
        if current_user.system_role not in ["system_admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Developer access or higher required"
            )
        return current_user
    return check_developer

# Optional authentication - for endpoints that work with or without auth
async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    auth_service: AuthService = Depends(get_auth_service)
) -> Optional[User]:
    """Get current user if authenticated, None otherwise"""
    if not credentials:
        return None
    
    try:
        return await get_current_user(bearer_credentials=credentials, auth_service=auth_service)
    except HTTPException:
        return None

# Resource ownership validation
async def require_resource_owner(
    resource_user_id: int,
    current_user: User = Depends(get_current_user)
) -> User:
    """Ensure current user owns the resource or is admin"""
    if current_user.system_role != "system_admin" and current_user.id != resource_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own resources"
        )
    return current_user

# Utility function to check multiple scopes
def require_any_scope(*required_scopes: TokenScope):
    """Dependency factory for requiring any of multiple scopes"""
    async def check_any_scope(
        user_and_scopes: tuple[User, List[TokenScope]] = Depends(get_current_user_with_scopes)
    ) -> User:
        user, scopes = user_and_scopes
        if any(scope in scopes for scope in required_scopes):
            return user
        
        scope_names = [scope.value for scope in required_scopes]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Insufficient permissions. Required any of: {', '.join(scope_names)}"
        )
    return check_any_scope

def require_all_scopes(*required_scopes: TokenScope):
    """Dependency factory for requiring all specified scopes"""
    async def check_all_scopes(
        user_and_scopes: tuple[User, List[TokenScope]] = Depends(get_current_user_with_scopes)
    ) -> User:
        user, scopes = user_and_scopes
        if all(scope in scopes for scope in required_scopes):
            return user
        
        scope_names = [scope.value for scope in required_scopes]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Insufficient permissions. Required all of: {', '.join(scope_names)}"
        )
    return check_all_scopes

# Enhanced permission dependencies with better error messages
def require_license_management():
    """Require license read OR write permissions"""
    return require_any_scope(TokenScope.LICENSE_READ, TokenScope.LICENSE_WRITE)

def require_customer_management():
    """Require customer read OR write permissions"""
    return require_any_scope(TokenScope.CUSTOMER_READ, TokenScope.CUSTOMER_WRITE)

def require_application_management():
    """Require application read OR write permissions"""
    return require_any_scope(TokenScope.APPLICATION_READ, TokenScope.APPLICATION_WRITE)

# Admin-only endpoints
def require_admin_access():
    """Require admin role for sensitive operations"""
    async def check_admin(current_user: User = Depends(get_current_user)) -> User:
        if current_user.system_role != "system_admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Administrator access required"
            )
        return current_user
    return check_admin

# Context-aware dependencies that return both user and scopes
def get_user_context():
    """Get user and scopes for context-aware operations"""
    async def get_context(
        user_and_scopes: tuple[User, List[TokenScope]] = Depends(get_current_user_with_scopes)
    ) -> tuple[User, List[TokenScope]]:
        return user_and_scopes
    return get_context