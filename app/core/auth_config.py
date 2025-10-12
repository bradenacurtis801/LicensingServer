from app.models.database import UserRole, SystemRole, TokenScope

# Authentication configuration
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Business role permissions mapping (for license management)
BUSINESS_ROLE_PERMISSIONS = {
    UserRole.USER: [
        # Standard user - can manage their own resources
        TokenScope.LICENSE_READ, TokenScope.LICENSE_WRITE, TokenScope.LICENSE_DELETE,
        TokenScope.CUSTOMER_READ, TokenScope.CUSTOMER_WRITE, TokenScope.CUSTOMER_DELETE,
        TokenScope.APPLICATION_READ, TokenScope.APPLICATION_WRITE, TokenScope.APPLICATION_DELETE,
        TokenScope.ACTIVATION_READ, TokenScope.ACTIVATION_WRITE, TokenScope.ACTIVATION_DELETE,
        TokenScope.VALIDATION,
        TokenScope.TOKEN_MANAGEMENT
    ]
}

# System role permissions mapping (for user management)
SYSTEM_ROLE_PERMISSIONS = {
    SystemRole.SYSTEM_ADMIN: [
        # Can manage users and system settings
        TokenScope.USER_MANAGEMENT,
        TokenScope.TOKEN_MANAGEMENT
    ],
    SystemRole.USER: [
        # Regular user - no special system permissions
    ]
}

def has_business_permission(business_role: UserRole, required_scope: TokenScope) -> bool:
    """Check if a business role has a specific permission"""
    return required_scope in BUSINESS_ROLE_PERMISSIONS.get(business_role, [])

def has_system_permission(system_role: SystemRole, required_scope: TokenScope) -> bool:
    """Check if a system role has a specific permission"""
    return required_scope in SYSTEM_ROLE_PERMISSIONS.get(system_role, [])

def get_user_permissions(business_role: UserRole, system_role: SystemRole) -> list[TokenScope]:
    """Get all permissions for a user based on their roles"""
    business_permissions = BUSINESS_ROLE_PERMISSIONS.get(business_role, [])
    system_permissions = SYSTEM_ROLE_PERMISSIONS.get(system_role, [])
    return list(set(business_permissions + system_permissions))