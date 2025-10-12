from typing import Optional
from datetime import datetime, timezone
from sqlmodel import Session, select
from app.models.database import LicenseKey, Activation
from app.models.schemas import LicenseValidationRequest, LicenseValidationResponse
from app.utils.license_generator import LicenseKeyGenerator
from app.core.exceptions import InvalidLicenseFormatException
from app.services.license_service import LicenseService
from app.services.activation_service import ActivationService
import json
from app.models.database import LicenseStatus, ActivationStatus

class ValidationService:
    def __init__(self, db: Session):
        self.db = db
        self.license_service = LicenseService(db)
        self.activation_service = ActivationService(db)
        self.generator = LicenseKeyGenerator()
    
    def validate_license(
        self, 
        request: LicenseValidationRequest, 
        client_ip: Optional[str] = None
    ) -> LicenseValidationResponse:
        """Validate a license key and machine combination"""
        
        # Step 1: Validate key format
        if not self.generator.validate_key_format(request.license_key):
            return LicenseValidationResponse(
                valid=False,
                message="Invalid license key format"
            )
        
        # Step 2: Find license in database
        key_hash = self.generator.hash_key(request.license_key)
        license_key = self.license_service.get_license_by_hash(key_hash)
        
        if not license_key:
            return LicenseValidationResponse(
                valid=False,
                message="License key not found"
            )
        
        # Step 3: Check license status
        if license_key.status.value != "active":
            return LicenseValidationResponse(
                valid=False,
                license_id=license_key.id,
                status=license_key.status,
                message=f"License is {license_key.status.value}"
            )
        
        # Step 4: Check expiration
        if license_key.expires_at and license_key.expires_at <= datetime.now(timezone.utc):
            # Update license status to expired
            from app.models.database import LicenseStatus
            license_key.status = LicenseStatus.EXPIRED
            self.db.add(license_key)
            self.db.commit()
            
            return LicenseValidationResponse(
                valid=False,
                license_id=license_key.id,
                status=license_key.status,
                expires_at=license_key.expires_at,
                message="License has expired"
            )
        
        # Step 5: Handle activation
        activation_result = self.activation_service.handle_activation(
            license_key, request.machine_id, client_ip
        )
        
        if not activation_result["success"]:
            return LicenseValidationResponse(
                valid=False,
                license_id=license_key.id,
                remaining_activations=activation_result.get("remaining_activations", 0),
                message=activation_result["message"]
            )
        
        # Step 6: Parse features
        features = None
        if license_key.features:
            try:
                features = json.loads(license_key.features)
            except json.JSONDecodeError:
                features = {}
        
        # Step 7: Return successful validation
        return LicenseValidationResponse(
            valid=True,
            license_id=license_key.id,
            customer_id=license_key.customer_id,
            application_id=license_key.application_id,
            status=license_key.status,
            expires_at=license_key.expires_at,
            features=features,
            remaining_activations=license_key.max_activations - license_key.current_activations,
            message="License is valid"
        )