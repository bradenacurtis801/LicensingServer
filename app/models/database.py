from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import List, Optional, Dict, Any
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import UniqueConstraint

# Enums
class LicenseStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    SUSPENDED = "suspended"
    REVOKED = "revoked"
    BLOCKED = "blocked"


class ActivationStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class UserRole(str, Enum):
    """Business roles for license management"""
    USER = "user"          # Standard user (manages own resources)

class SystemRole(str, Enum):
    """System administration roles"""
    SYSTEM_ADMIN = "system_admin"  # Can manage users and system settings
    USER = "user"                  # Regular user (default)

class TokenScope(str, Enum):
    # License management
    LICENSE_READ = "license:read"
    LICENSE_WRITE = "license:write"
    LICENSE_DELETE = "license:delete"
    
    # Customer management
    CUSTOMER_READ = "customer:read"
    CUSTOMER_WRITE = "customer:write"
    CUSTOMER_DELETE = "customer:delete"
    
    # Application management
    APPLICATION_READ = "application:read"
    APPLICATION_WRITE = "application:write"
    APPLICATION_DELETE = "application:delete"
    
    # Activation management
    ACTIVATION_READ = "activation:read"
    ACTIVATION_WRITE = "activation:write"
    ACTIVATION_DELETE = "activation:delete"
    
    # Validation (typically for SDK usage)
    VALIDATION = "validation"
    
    # Admin operations
    USER_MANAGEMENT = "user:management"
    TOKEN_MANAGEMENT = "token:management"

class UserBase(SQLModel):
    username: str = Field(unique=True, index=True, max_length=50)
    email: str = Field(unique=True, index=True, max_length=255)
    full_name: str = Field(max_length=255)
    business_role: UserRole = Field(default=UserRole.USER)  # Business role for license management
    system_role: SystemRole = Field(default=SystemRole.USER)     # System role for user management
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str = Field(max_length=255)
    
    # Relationships
    customers: List["Customer"] = Relationship(back_populates="owner")
    applications: List["Application"] = Relationship(back_populates="owner")
    sessions: List["Session"] = Relationship(back_populates="user")
    api_tokens: List["APIToken"] = Relationship(back_populates="user")

# Session model for login sessions (temporary, full permissions)
class SessionBase(SQLModel):
    user_id: int = Field(foreign_key="user.id")
    session_token: str = Field(unique=True, index=True, max_length=255)
    is_revoked: bool = Field(default=False)  # For immediate revocation
    expires_at: datetime = Field()
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_activity: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Session(SessionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    user: User = Relationship(back_populates="sessions")

# API Token model for custom access tokens (long-lived, specific scopes)
class APITokenBase(SQLModel):
    name: str = Field(max_length=100)  # Friendly name for the token
    token_hash: str = Field(unique=True, index=True, max_length=255)
    scopes: str = Field()  # JSON array of TokenScope values
    is_active: bool = Field(default=True)
    expires_at: Optional[datetime] = Field(default=None)
    last_used_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class APIToken(APITokenBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    
    # Relationships
    user: User = Relationship(back_populates="api_tokens")


class CustomerBase(SQLModel):
    name: str = Field(max_length=255)
    email: str = Field(index=True, max_length=255)  # Remove unique=True to allow same email across users
    company: Optional[str] = Field(default=None, max_length=255)
    user_id: int = Field(foreign_key="user.id")  # ADD THIS
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Customer(CustomerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    owner: "User" = Relationship(back_populates="customers")  # ADD THIS
    license_keys: List["LicenseKey"] = Relationship(back_populates="customer")
    
    __table_args__ = (
        UniqueConstraint("user_id", "email", name="uq_user_email"),
    )


class ApplicationBase(SQLModel):
    name: str = Field(max_length=255)
    version: str = Field(max_length=50)
    description: Optional[str] = Field(default=None)
    features: Optional[str] = Field(default=None)
    user_id: int = Field(foreign_key="user.id")  # ADD THIS
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Application(ApplicationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    owner: User = Relationship(back_populates="applications")  # ADD THIS
    license_keys: List["LicenseKey"] = Relationship(back_populates="application")


class LicenseKeyBase(SQLModel):
    key_hash: str = Field(unique=True, index=True)
    customer_id: Optional[int] = Field(foreign_key="customer.id", default=None)
    application_id: int = Field(foreign_key="application.id")
    status: LicenseStatus = Field(default=LicenseStatus.ACTIVE)
    expires_at: Optional[datetime] = Field(default=None)
    max_activations: int = Field(default=1)
    current_activations: int = Field(default=0)
    features: Optional[str] = Field(default=None)  # JSON string of enabled features
    notes: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class LicenseKey(LicenseKeyBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationships
    customer: Customer = Relationship(back_populates="license_keys")
    application: Application = Relationship(back_populates="license_keys")
    activations: List["Activation"] = Relationship(back_populates="license_key")
    activation_forms: List["ActivationForm"] = Relationship(
        back_populates="license_key"
    )


class ActivationBase(SQLModel):
    license_key_id: int = Field(foreign_key="licensekey.id")
    machine_id: str = Field(max_length=255)  # Hardware fingerprint
    machine_name: Optional[str] = Field(default=None, max_length=255)
    ip_address: Optional[str] = Field(default=None, max_length=45)
    status: ActivationStatus = Field(default=ActivationStatus.ACTIVE)
    activated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_heartbeat: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Activation(ActivationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationships
    license_key: LicenseKey = Relationship(back_populates="activations")

# New models for activation forms
class ActivationFormBase(SQLModel):
    license_key_id: int = Field(foreign_key="licensekey.id")
    machine_id: str = Field(
        max_length=255
    )  # Hardware fingerprint from offline computer
    machine_name: Optional[str] = Field(default=None, max_length=255)
    request_code: str = Field(max_length=255)  # Code generated by offline computer
    activation_code: Optional[str] = Field(
        default=None, max_length=255
    )  # Code to activate offline
    status: str = Field(default="pending")  # pending, completed, expired
    expires_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=24)
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = Field(default=None)


class ActivationForm(ActivationFormBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationships
    license_key: LicenseKey = Relationship(back_populates="activation_forms")


# Offline activation codes for batch generation
class OfflineActivationCodeBase(SQLModel):
    license_key_id: int = Field(foreign_key="licensekey.id")
    activation_code: str = Field(max_length=255, unique=True, index=True)
    machine_id: Optional[str] = Field(default=None, max_length=255)
    is_used: bool = Field(default=False)
    expires_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=30)
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    used_at: Optional[datetime] = Field(default=None)


class OfflineActivationCode(OfflineActivationCodeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
