"""
License service for managing license keys
"""
import json
from datetime import datetime, timezone
from typing import List, Optional, Union, Dict, Any
from sqlmodel import Session, select
from app.models.database import LicenseKey, Customer, Application, User
from app.models.schemas import LicenseKeyCreate, LicenseKeyResponse, LicenseKeyUpdate, LicenseKeyGenerator, LicenseKeyWithRelationsResponse
from app.core.exceptions import CustomerNotFoundException, ApplicationNotFoundException, LicenseNotFoundException


class LicenseService:
    def __init__(self, db: Session):
        self.db = db
        self.generator = LicenseKeyGenerator()
    
    def create_license(self, license_data: LicenseKeyCreate, user: User) -> LicenseKeyResponse:
        """Create a new license key"""
        # Verify customer exists and belongs to user
        customer = self.db.exec(
            select(Customer).where(
                Customer.id == license_data.customer_id,
                Customer.user_id == user.id
            )
        ).first()
        if not customer:
            raise CustomerNotFoundException(license_data.customer_id)
        
        # Verify application exists and belongs to user
        application = self.db.exec(
            select(Application).where(
                Application.id == license_data.application_id,
                Application.user_id == user.id
            )
        ).first()
        if not application:
            raise ApplicationNotFoundException(license_data.application_id)
        
        # Generate license key
        license_key = self.generator.generate_key()
        key_hash = self.generator.hash_key(license_key)
        
        # Prepare database record
        db_data = license_data.dict()
        db_data['key_hash'] = key_hash
        if db_data.get('features') is not None:
            db_data['features'] = json.dumps(db_data['features'])
        
        # Create and save license
        db_license = LicenseKey(**db_data)
        self.db.add(db_license)
        self.db.commit()
        self.db.refresh(db_license)
        
        # Prepare response
        return self._to_response(db_license, include_key=license_key)
    
    def get_license(self, license_id: int, user: User) -> LicenseKeyResponse:
        """Get a license by ID (with ownership check)"""
        license_key = self.db.exec(
            select(LicenseKey)
            .join(Customer)
            .where(
                LicenseKey.id == license_id,
                Customer.user_id == user.id
            )
        ).first()
        
        if not license_key:
            raise LicenseNotFoundException(license_id)
        
        return self._to_response(license_key)
    
    def get_license_by_key(self, license_key: str, user: User) -> Optional[LicenseKeyResponse]:
        """Get a license by key (with ownership check)"""
        key_hash = self.generator.hash_key(license_key)
        
        db_license = self.db.exec(
            select(LicenseKey)
            .join(Customer)
            .where(
                LicenseKey.key_hash == key_hash,
                Customer.user_id == user.id
            )
        ).first()
        
        if not db_license:
            return None
        
        return self._to_response(db_license)
    
    def list_licenses(self, user: User, skip: int = 0, limit: int = 100, include_relations: bool = False) -> List[Union[LicenseKeyResponse, LicenseKeyWithRelationsResponse]]:
        """List all licenses for a user"""
        if include_relations:
            from app.models.schemas import CustomerResponse, ApplicationResponse
            
            # Eager load the related data
            licenses = self.db.exec(
                select(LicenseKey, Customer, Application)
                .join(Customer, LicenseKey.customer_id == Customer.id)
                .join(Application, LicenseKey.application_id == Application.id)
                .where(Customer.user_id == user.id)
                .offset(skip)
                .limit(limit)
            ).all()
            
            result = []
            for license_key, customer, application in licenses:
                # Convert to response format
                license_data = self._to_response(license_key).dict()
                
                # Add related data
                license_data['customer'] = CustomerResponse(
                    id=customer.id,
                    name=customer.name,
                    email=customer.email,
                    company=customer.company,
                    created_at=customer.created_at
                )
                
                # Parse features JSON string to dict if it exists
                features = None
                if application.features:
                    try:
                        import json
                        features = json.loads(application.features)
                    except (json.JSONDecodeError, TypeError):
                        features = None
                
                license_data['application'] = ApplicationResponse(
                    id=application.id,
                    name=application.name,
                    version=application.version,
                    description=application.description,
                    features=features,
                    created_at=application.created_at
                )
                
                result.append(LicenseKeyWithRelationsResponse(**license_data))
            
            return result
        else:
            licenses = self.db.exec(
                select(LicenseKey)
                .join(Customer)
                .where(Customer.user_id == user.id)
                .offset(skip)
                .limit(limit)
            ).all()
            
            return [self._to_response(license) for license in licenses]
    
    
    def update_license(self, license_id: int, license_update: LicenseKeyUpdate, user: User) -> LicenseKeyResponse:
        """Update a license (with ownership check)"""
        license_key = self.db.exec(
            select(LicenseKey)
            .join(Customer)
            .where(
                LicenseKey.id == license_id,
                Customer.user_id == user.id
            )
        ).first()
        
        if not license_key:
            raise LicenseNotFoundException(license_id)
        
        # Update fields
        update_data = license_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == 'features' and value is not None:
                setattr(license_key, field, json.dumps(value))
            else:
                setattr(license_key, field, value)
        
        license_key.updated_at = datetime.now(timezone.utc)
        
        self.db.add(license_key)
        self.db.commit()
        self.db.refresh(license_key)
        
        return self._to_response(license_key)
    
    def delete_license(self, license_id: int, user: User) -> bool:
        """Delete a license (with ownership check)"""
        license_key = self.db.exec(
            select(LicenseKey)
            .join(Customer)
            .where(
                LicenseKey.id == license_id,
                Customer.user_id == user.id
            )
        ).first()
        
        if not license_key:
            return False
        
        self.db.delete(license_key)
        self.db.commit()
        return True
    
    def block_license(self, license_id: int, user: User) -> LicenseKeyResponse:
        """Block a license (with ownership check)"""
        license_key = self.db.exec(
            select(LicenseKey)
            .join(Customer)
            .where(
                LicenseKey.id == license_id,
                Customer.user_id == user.id
            )
        ).first()
        
        if not license_key:
            raise LicenseNotFoundException(license_id)
        
        license_key.status = "blocked"
        license_key.updated_at = datetime.now(timezone.utc)
        
        self.db.add(license_key)
        self.db.commit()
        self.db.refresh(license_key)
        
        return self._to_response(license_key)
    
    def unblock_license(self, license_id: int, user: User) -> LicenseKeyResponse:
        """Unblock a license (with ownership check)"""
        license_key = self.db.exec(
            select(LicenseKey)
            .join(Customer)
            .where(
                LicenseKey.id == license_id,
                Customer.user_id == user.id
            )
        ).first()
        
        if not license_key:
            raise LicenseNotFoundException(license_id)
        
        license_key.status = "active"
        license_key.updated_at = datetime.now(timezone.utc)
        
        self.db.add(license_key)
        self.db.commit()
        self.db.refresh(license_key)
        
        return self._to_response(license_key)
    
    def _to_response(self, license_key: LicenseKey, include_key: Optional[str] = None) -> LicenseKeyResponse:
        """Convert LicenseKey model to LicenseKeyResponse"""
        features = None
        if license_key.features:
            try:
                features = json.loads(license_key.features)
            except json.JSONDecodeError:
                features = {}
        
        return LicenseKeyResponse(
            id=license_key.id,
            license_key=include_key or "***",  # Only show key on creation
            customer_id=license_key.customer_id,
            application_id=license_key.application_id,
            status=license_key.status,
            expires_at=license_key.expires_at,
            max_activations=license_key.max_activations,
            current_activations=license_key.current_activations,
            features=features,
            notes=license_key.notes,
            created_at=license_key.created_at,
            updated_at=license_key.updated_at
        )
    
