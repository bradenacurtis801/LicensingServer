import hashlib
import json
import secrets
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, validator
from sqlmodel import Field, Relationship, SQLModel
from app.models.database import UserRole, SystemRole, TokenScope, LicenseStatus, ActivationStatus

# User Management Schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    password: str
    # No roles specified during registration - users get default roles

    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username must be alphanumeric (with _ or - allowed)')
        return v

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class UserBusinessRoleUpdate(BaseModel):
    business_role: UserRole

class UserSystemRoleUpdate(BaseModel):
    system_role: SystemRole

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    business_role: UserRole
    system_role: SystemRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserChangePassword(BaseModel):
    current_password: str
    new_password: str

    @validator('new_password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v
    
# API Token Management Schemas (for custom access tokens)
class APITokenCreate(BaseModel):
    name: str
    scopes: List[TokenScope]
    expires_at: Optional[datetime] = None

    @validator('name')
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Token name cannot be empty')
        return v.strip()

class APITokenResponse(BaseModel):
    id: int
    name: str
    scopes: List[TokenScope]
    is_active: bool
    expires_at: Optional[datetime]
    last_used_at: Optional[datetime]
    created_at: datetime
    # Note: We don't return the actual token value for security

class APITokenCreateResponse(BaseModel):
    """Response when creating a new API token - includes the actual token value"""
    id: int
    name: str
    scopes: List[TokenScope]
    is_active: bool
    expires_at: Optional[datetime]
    created_at: datetime
    token: str  # Only returned on creation!

class APITokenUpdate(BaseModel):
    name: Optional[str] = None
    scopes: Optional[List[TokenScope]] = None
    is_active: Optional[bool] = None
    expires_at: Optional[datetime] = None

# Authentication Response Schemas
class TokenResponse(BaseModel):
    session_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
    user: UserResponse


# API Schemas (Pydantic BaseModel)
class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    company: Optional[str] = None
    # user_id will be set from authentication context

class CustomerResponse(BaseModel):
    id: int
    name: str
    email: str
    company: Optional[str]
    created_at: datetime


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    company: Optional[str] = None


class ApplicationCreate(BaseModel):
    name: str
    version: str
    description: Optional[str] = None
    features: Optional[Dict[str, Any]] = None
    # user_id will be set from authentication context


class ApplicationResponse(BaseModel):
    id: int
    name: str
    version: str
    description: Optional[str]
    features: Optional[Dict[str, Any]]
    created_at: datetime


class ApplicationUpdate(BaseModel):
    name: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None
    features: Optional[Dict[str, Any]] = None


class LicenseKeyCreate(BaseModel):
    customer_id: int
    application_id: int
    expires_at: Optional[datetime] = None
    max_activations: int = 1
    features: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None

    @validator("expires_at")
    def validate_expiration(cls, v):
        if v:
            # Convert to UTC if timezone-aware, otherwise assume UTC
            if v.tzinfo is not None:
                v_utc = v.astimezone(timezone.utc).replace(tzinfo=None)
            else:
                v_utc = v

            if v_utc <= datetime.utcnow():
                raise ValueError("Expiration date must be in the future")
        return v


class LicenseKeyResponse(BaseModel):
    id: int
    license_key: str  # The actual key (only shown on creation)
    customer_id: int
    application_id: int
    status: LicenseStatus
    expires_at: Optional[datetime]
    max_activations: int
    current_activations: int
    features: Optional[Dict[str, Any]]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime


class LicenseKeyUpdate(BaseModel):
    status: Optional[LicenseStatus] = None
    expires_at: Optional[datetime] = None
    max_activations: Optional[int] = None
    features: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None


class ActivationCreate(BaseModel):
    license_key: str  # The actual license key
    machine_id: str
    machine_name: Optional[str] = None


class ActivationResponse(BaseModel):
    id: int
    license_key_id: int
    machine_id: str
    machine_name: Optional[str]
    ip_address: Optional[str]
    status: ActivationStatus
    activated_at: datetime
    last_heartbeat: datetime


class ActivationFormCreate(BaseModel):
    license_key: str  # The actual license key
    machine_id: str
    machine_name: Optional[str] = None


class ActivationFormResponse(BaseModel):
    id: int
    license_key_id: int
    machine_id: str
    machine_name: Optional[str]
    request_code: str
    activation_code: Optional[str]
    status: str
    expires_at: datetime
    created_at: datetime
    completed_at: Optional[datetime]


class ActivationFormComplete(BaseModel):
    request_code: str
    activation_code: str


class OfflineActivationCodeCreate(BaseModel):
    license_key_id: int
    machine_id: Optional[str] = None
    quantity: int = 1


class OfflineActivationCodeResponse(BaseModel):
    id: int
    license_key_id: int
    activation_code: str
    machine_id: Optional[str]
    is_used: bool
    expires_at: datetime
    created_at: datetime
    used_at: Optional[datetime]


class LicenseValidationRequest(BaseModel):
    license_key: str
    machine_id: str


class LicenseValidationResponse(BaseModel):
    valid: bool
    license_id: Optional[int] = None
    customer_id: Optional[int] = None
    application_id: Optional[int] = None
    status: Optional[LicenseStatus] = None
    expires_at: Optional[datetime] = None
    features: Optional[Dict[str, Any]] = None
    remaining_activations: Optional[int] = None
    message: Optional[str] = None


# Utility functions for license key generation
class LicenseKeyGenerator:
    @staticmethod
    def generate_key(length: int = 25) -> str:
        """Generate a random license key"""
        # Generate random bytes and convert to base32 (removes confusing chars)
        key_bytes = secrets.token_bytes(length)
        key = secrets.token_urlsafe(length)[:length].upper()

        # Format as XXXXX-XXXXX-XXXXX-XXXXX-XXXXX
        formatted_key = "-".join([key[i : i + 5] for i in range(0, len(key), 5)])
        return formatted_key

    @staticmethod
    def hash_key(key: str) -> str:
        """Hash a license key for storage"""
        return hashlib.sha256(key.encode()).hexdigest()

    @staticmethod
    def validate_key_format(key: str) -> bool:
        """Validate license key format"""
        # Remove dashes and check if it's alphanumeric and correct length
        clean_key = key.replace("-", "")
        return len(clean_key) == 25 and clean_key.isalnum()


# Database helper functions
def serialize_features(features: Optional[Dict[str, Any]]) -> Optional[str]:
    """Convert features dict to JSON string for database storage"""
    if features is None:
        return None
    return json.dumps(features)


def deserialize_features(features_json: Optional[str]) -> Optional[Dict[str, Any]]:
    """Convert JSON string back to features dict"""
    if features_json is None:
        return None
    try:
        return json.loads(features_json)
    except json.JSONDecodeError:
        return None
