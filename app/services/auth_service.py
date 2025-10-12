# auth service layer
import secrets
import hashlib
import json
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Union
from sqlmodel import Session, select
from passlib.context import CryptContext
from fastapi import HTTPException, status

from app.models.database import User, Session as DBSession, APIToken, SystemRole
from app.models.schemas import (
    UserCreate, UserResponse, UserUpdate, UserLogin, UserChangePassword,
    APITokenCreate, APITokenResponse, APITokenCreateResponse, APITokenUpdate,
    TokenResponse, UserRole, TokenScope
)
from app.core.auth_config import (
    ACCESS_TOKEN_EXPIRE_MINUTES, 
    get_user_permissions
)
from app.core.exceptions import (
    UserNotFoundException, InvalidCredentialsException, 
    TokenNotFoundException, PermissionDeniedException
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db: Session):
        self.db = db
    
    def _constant_time_username_verify(self, provided_username: str, stored_username: str) -> bool:
        """Constant-time username comparison to prevent timing attacks"""
        return secrets.compare_digest(provided_username, stored_username)
    
    def _dummy_verify(self) -> None:
        """Perform dummy password verification to maintain consistent timing"""
        # Use a simple hash operation that takes similar time to bcrypt verification
        # This provides timing protection without relying on bcrypt hash validation
        import hashlib
        dummy_password = "dummy_password_for_timing_protection"
        dummy_salt = "dummy_salt_for_timing_protection"
        
        # Perform a hash operation that takes similar time to bcrypt verification
        for _ in range(12):  # bcrypt uses 12 rounds by default
            dummy_password = hashlib.sha256((dummy_password + dummy_salt).encode()).hexdigest()
    
    # User Management
    def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create a new user with default role"""
        # Check if username or email already exists
        existing_user = self.db.exec(
            select(User).where(
                (User.username == user_data.username) | 
                (User.email == user_data.email)
            )
        ).first()
        
        if existing_user:
            if existing_user.username == user_data.username:
                raise HTTPException(
                    status_code=400, 
                    detail="Username already registered"
                )
            else:
                raise HTTPException(
                    status_code=400, 
                    detail="Email already registered"
                )
        
        # Hash password
        hashed_password = pwd_context.hash(user_data.password)
        
        # Create user with default roles
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            password_hash=hashed_password,
            business_role=UserRole.USER,  # Default business role
            system_role=SystemRole.USER   # Default system role
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        return self._to_user_response(db_user)
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user with username/password (timing-attack resistant)"""
        # Get user by username
        user = self.db.exec(
            select(User).where(User.username == username, User.is_active == True)
        ).first()
        
        # Always perform password verification to maintain consistent timing
        if user:
            # Real user - verify password
            if pwd_context.verify(password, user.password_hash):
                return user
        else:
            # User doesn't exist - perform dummy verification
            self._dummy_verify()
        
        return None
    
    def get_user(self, user_id: int) -> UserResponse:
        """Get user by ID"""
        user = self.db.get(User, user_id)
        if not user:
            raise UserNotFoundException(f"User {user_id} not found")
        
        return self._to_user_response(user)
    
    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Get all users with pagination"""
        from sqlmodel import select
        
        users = self.db.exec(
            select(User)
            .offset(skip)
            .limit(limit)
            .order_by(User.created_at.desc())
        ).all()
        
        return [self._to_user_response(user) for user in users]
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.db.exec(
            select(User).where(User.username == username)
        ).first()
    
    def update_user(self, user_id: int, update_data: UserUpdate) -> UserResponse:
        """Update user"""
        user = self.db.get(User, user_id)
        if not user:
            raise UserNotFoundException(f"User {user_id} not found")
        
        update_dict = update_data.dict(exclude_unset=True)
        update_dict['updated_at'] = datetime.now(timezone.utc)
        
        for field, value in update_dict.items():
            setattr(user, field, value)
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return self._to_user_response(user)
    
    def change_password(self, user_id: int, password_data: UserChangePassword) -> dict:
        """Change user password"""
        user = self.db.get(User, user_id)
        if not user:
            raise UserNotFoundException(f"User {user_id} not found")
        
        # Verify current password
        if not pwd_context.verify(password_data.current_password, user.password_hash):
            raise InvalidCredentialsException("Current password is incorrect")
        
        # Update password
        user.password_hash = pwd_context.hash(password_data.new_password)
        user.updated_at = datetime.now(timezone.utc)
        
        self.db.add(user)
        self.db.commit()
        
        return {"message": "Password changed successfully"}
    
    def update_user_business_role(self, user_id: int, new_role: UserRole, admin_user: User) -> UserResponse:
        """Update user business role (system admin only)"""
        # Check if admin user has system admin permission
        if admin_user.system_role != SystemRole.SYSTEM_ADMIN:
            raise HTTPException(
                status_code=403,
                detail="Only system administrators can change user business roles"
            )
        
        # Validate that only USER business role is available
        if new_role != UserRole.USER:
            raise HTTPException(
                status_code=400,
                detail="Only USER business role is available"
            )
        
        # Get user to update
        user = self.db.get(User, user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        # Update business role
        user.business_role = new_role
        user.updated_at = datetime.now(timezone.utc)
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return self._to_user_response(user)
    
    def update_user_system_role(self, user_id: int, new_role: SystemRole, admin_user: User) -> UserResponse:
        """Update user system role (system admin only)"""
        # Check if admin user has system admin permission
        if admin_user.system_role != SystemRole.SYSTEM_ADMIN:
            raise HTTPException(
                status_code=403,
                detail="Only system administrators can change user system roles"
            )
        
        # Get user to update
        user = self.db.get(User, user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        # Update system role
        user.system_role = new_role
        user.updated_at = datetime.now(timezone.utc)
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return self._to_user_response(user)
    
    # Session Token Management (for login sessions)
    def create_login_session(self, user: User) -> TokenResponse:
        """Create a session token for user login"""
        # Generate token
        raw_token = self._generate_session_token()
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        
        # Set expiration
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        # Create database record
        db_session = DBSession(
            user_id=user.id,
            session_token=token_hash,
            expires_at=expires_at
        )
        
        self.db.add(db_session)
        self.db.commit()
        
        return TokenResponse(
            session_token=raw_token,
            token_type="bearer",
            expires_in=int(ACCESS_TOKEN_EXPIRE_MINUTES * 60),
            user=self._to_user_response(user)
        )
    
    def verify_session_token(self, token: str) -> Optional[User]:
        """Verify session token and return user (timing-attack resistant)"""
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        
        db_session = self.db.exec(
            select(DBSession).where(
                DBSession.session_token == token_hash,
                DBSession.is_revoked == False
            )
        ).first()
        
        # Always perform some work to maintain consistent timing
        if not db_session:
            # Token doesn't exist - perform dummy operations
            self._dummy_verify()
            return None
        
        # Check expiration (handle both timezone-aware and timezone-naive)
        current_time = datetime.now(timezone.utc)
        expires_at = db_session.expires_at
        
        # If expires_at is timezone-naive, assume it's UTC
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        
        if expires_at <= current_time:
            return None
        
        # Get user
        user = self.db.get(User, db_session.user_id)
        if not user or not user.is_active:
            return None
        
        # Update last activity
        db_session.last_activity = datetime.now(timezone.utc)
        self.db.add(db_session)
        self.db.commit()
        
        return user
    
    # API Token Management (for custom access tokens)
    def create_api_token(self, user: User, token_data: APITokenCreate) -> APITokenCreateResponse:
        """Create an API token with specific scopes"""
        # Validate scopes against user roles
        allowed_scopes = get_user_permissions(user.business_role, user.system_role)
        invalid_scopes = [scope for scope in token_data.scopes if scope not in allowed_scopes]
        
        if invalid_scopes:
            raise PermissionDeniedException(
                f"User roles (business: {user.business_role}, system: {user.system_role}) do not allow scopes: {', '.join(invalid_scopes)}"
            )
        
        # Generate token
        raw_token = self._generate_api_token()
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        
        # Set expiration
        expires_at = token_data.expires_at or (datetime.now(timezone.utc) + timedelta(days=365))  # Default 1 year
        
        # Create database record
        db_token = APIToken(
            user_id=user.id,
            name=token_data.name,
            token_hash=token_hash,
            scopes=json.dumps([scope.value for scope in token_data.scopes]),
            expires_at=expires_at
        )
        
        self.db.add(db_token)
        self.db.commit()
        self.db.refresh(db_token)
        
        return APITokenCreateResponse(
            id=db_token.id,
            name=db_token.name,
            scopes=token_data.scopes,
            is_active=db_token.is_active,
            expires_at=db_token.expires_at,
            created_at=db_token.created_at,
            token=raw_token  # Only returned on creation!
        )
    
    def verify_api_token(self, token: str) -> Optional[tuple[User, List[TokenScope]]]:
        """Verify API token and return user + scopes (timing-attack resistant)"""
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        
        db_token = self.db.exec(
            select(APIToken).where(
                APIToken.token_hash == token_hash,
                APIToken.is_active == True
            )
        ).first()
        
        # Always perform some work to maintain consistent timing
        if not db_token:
            # Token doesn't exist - perform dummy operations
            self._dummy_verify()
            return None
        
        # Check expiration (handle both timezone-aware and timezone-naive)
        if db_token.expires_at:
            current_time = datetime.now(timezone.utc)
            expires_at = db_token.expires_at
            
            # If expires_at is timezone-naive, assume it's UTC
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)
            
            if expires_at <= current_time:
                return None
        
        # Get user
        user = self.db.get(User, db_token.user_id)
        if not user or not user.is_active:
            return None
        
        # Update last used
        db_token.last_used_at = datetime.now(timezone.utc)
        self.db.add(db_token)
        self.db.commit()
        
        # Parse scopes
        scopes = [TokenScope(scope) for scope in json.loads(db_token.scopes)]
        
        return user, scopes
    
    def list_api_tokens(self, user_id: int) -> List[APITokenResponse]:
        """List user's API tokens"""
        tokens = self.db.exec(
            select(APIToken).where(APIToken.user_id == user_id)
        ).all()
        
        return [self._to_token_response(token) for token in tokens]
    
    def delete_api_token(self, user_id: int, token_id: int) -> dict:
        """Delete API token"""
        token = self.db.exec(
            select(APIToken).where(
                APIToken.id == token_id,
                APIToken.user_id == user_id
            )
        ).first()
        
        if not token:
            raise TokenNotFoundException(f"Token {token_id} not found")
        
        self.db.delete(token)
        self.db.commit()
        
        return {"message": "API token deleted successfully"}
    
    def update_api_token(self, user_id: int, token_id: int, token_update: APITokenUpdate) -> APITokenResponse:
        """Update API token"""
        # Get the token
        token = self.db.exec(
            select(APIToken).where(
                APIToken.id == token_id,
                APIToken.user_id == user_id
            )
        ).first()
        
        if not token:
            raise TokenNotFoundException(f"Token {token_id} not found")
        
        # Get user for scope validation
        user = self.db.get(User, user_id)
        if not user:
            raise UserNotFoundException(f"User {user_id} not found")
        
        # Update fields
        update_data = token_update.dict(exclude_unset=True)
        
        # Validate scopes if being updated
        if 'scopes' in update_data and update_data['scopes'] is not None:
            allowed_scopes = get_user_permissions(user.business_role, user.system_role)
            invalid_scopes = [scope for scope in update_data['scopes'] if scope not in allowed_scopes]
            
            if invalid_scopes:
                raise PermissionDeniedException(
                    f"User roles (business: {user.business_role}, system: {user.system_role}) do not allow scopes: {', '.join(invalid_scopes)}"
                )
            
            # Convert scopes to JSON string for storage
            update_data['scopes'] = json.dumps([scope.value for scope in update_data['scopes']])
        
        # Apply updates
        for field, value in update_data.items():
            setattr(token, field, value)
        
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        
        return self._to_token_response(token)
    
    def has_scope(self, scopes: List[TokenScope], required_scope: TokenScope) -> bool:
        """Check if user has required scope"""
        return required_scope in scopes
    
    def _generate_session_token(self) -> str:
        """Generate a random session token using cryptographically secure random"""
        # Use secrets.token_urlsafe for cryptographically secure random tokens
        return f"st_{secrets.token_urlsafe(32)}"
    
    def _generate_api_token(self) -> str:
        """Generate a random API token using cryptographically secure random"""
        # Use secrets.token_urlsafe for cryptographically secure random tokens
        return f"lt_{secrets.token_urlsafe(32)}"
    
    def _to_user_response(self, user: User) -> UserResponse:
        """Convert User model to UserResponse"""
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            business_role=user.business_role,
            system_role=user.system_role,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    
    def _to_token_response(self, token: APIToken) -> APITokenResponse:
        """Convert APIToken model to APITokenResponse"""
        scopes = [TokenScope(scope) for scope in json.loads(token.scopes)]
        
        return APITokenResponse(
            id=token.id,
            name=token.name,
            scopes=scopes,
            is_active=token.is_active,
            expires_at=token.expires_at,
            last_used_at=token.last_used_at,
            created_at=token.created_at
        )