from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime, timedelta, timezone
import secrets
import hashlib
import json

from app.models.database import ActivationForm, OfflineActivationCode, LicenseKey, Activation
from app.models.schemas import (
    ActivationFormCreate, ActivationFormResponse, ActivationFormComplete,
    OfflineActivationCodeCreate, OfflineActivationCodeResponse
)
from app.core.exceptions import LicenseNotFoundException, ActivationFormNotFoundException
from app.services.license_service import LicenseService

class ActivationFormService:
    def __init__(self, db: Session):
        self.db = db
        self.license_service = LicenseService(db)
    
    def create_activation_form(self, form_data: ActivationFormCreate) -> ActivationFormResponse:
        """Create a new activation form request"""
        # Find the license key
        license_key = self.license_service.get_license_by_hash(
            self.license_service.generator.hash_key(form_data.license_key)
        )
        
        if not license_key:
            raise LicenseNotFoundException(f"License key not found")
        
        # Check if license is active
        if license_key.status != "active":
            raise ValueError("License is not active")
        
        # Check if license has expired
        if license_key.expires_at and license_key.expires_at <= datetime.now(timezone.utc):
            raise ValueError("License has expired")
        
        # Check if max activations reached
        if license_key.current_activations >= license_key.max_activations:
            raise ValueError("Maximum activations reached")
        
        # Generate request code (hardware fingerprint + random)
        request_code = self._generate_request_code(form_data.machine_id)
        
        # Create activation form
        db_form = ActivationForm(
            license_key_id=license_key.id,
            machine_id=form_data.machine_id,
            machine_name=form_data.machine_name,
            request_code=request_code,
            status="pending"
        )
        
        self.db.add(db_form)
        self.db.commit()
        self.db.refresh(db_form)
        
        return self._to_response(db_form)
    
    def complete_activation_form(self, complete_data: ActivationFormComplete) -> ActivationFormResponse:
        """Complete an activation form with activation code"""
        # Find the activation form
        form = self.db.exec(
            select(ActivationForm).where(ActivationForm.request_code == complete_data.request_code)
        ).first()
        
        if not form:
            raise ActivationFormNotFoundException("Activation form not found")
        
        if form.status != "pending":
            raise ValueError("Activation form is not pending")
        
        if form.expires_at <= datetime.now(timezone.utc):
            raise ValueError("Activation form has expired")
        
        # Verify activation code
        if not self._verify_activation_code(form.license_key_id, complete_data.activation_code):
            raise ValueError("Invalid activation code")
        
        # Create activation
        activation = Activation(
            license_key_id=form.license_key_id,
            machine_id=form.machine_id,
            machine_name=form.machine_name,
            status="active"
        )
        
        # Update license activation count
        license_key = self.db.get(LicenseKey, form.license_key_id)
        license_key.current_activations += 1
        
        # Mark form as completed
        form.status = "completed"
        form.activation_code = complete_data.activation_code
        form.completed_at = datetime.now(timezone.utc)
        
        self.db.add(activation)
        self.db.add(license_key)
        self.db.add(form)
        self.db.commit()
        self.db.refresh(form)
        
        return self._to_response(form)
    
    def generate_offline_activation_codes(self, code_data: OfflineActivationCodeCreate) -> List[OfflineActivationCodeResponse]:
        """Generate offline activation codes for a license"""
        # Verify license exists
        license_key = self.db.get(LicenseKey, code_data.license_key_id)
        if not license_key:
            raise LicenseNotFoundException(f"License {code_data.license_key_id} not found")
        
        codes = []
        for _ in range(code_data.quantity):
            activation_code = self._generate_activation_code()
            
            db_code = OfflineActivationCode(
                license_key_id=code_data.license_key_id,
                activation_code=activation_code,
                machine_id=code_data.machine_id
            )
            
            self.db.add(db_code)
            codes.append(db_code)
        
        self.db.commit()
        
        # Refresh all codes
        for code in codes:
            self.db.refresh(code)
        
        return [self._to_offline_response(code) for code in codes]
    
    def list_activation_forms(self, skip: int = 0, limit: int = 100) -> List[ActivationFormResponse]:
        """List activation forms"""
        forms = self.db.exec(
            select(ActivationForm).offset(skip).limit(limit)
        ).all()
        
        return [self._to_response(form) for form in forms]
    
    def get_activation_form(self, form_id: int) -> ActivationFormResponse:
        """Get activation form by ID"""
        form = self.db.get(ActivationForm, form_id)
        if not form:
            raise ActivationFormNotFoundException(f"Activation form {form_id} not found")
        
        return self._to_response(form)
    
    def _generate_request_code(self, machine_id: str) -> str:
        """Generate a unique request code"""
        # Combine machine ID with random data
        random_data = secrets.token_hex(16)
        combined = f"{machine_id}:{random_data}:{datetime.now(timezone.utc).isoformat()}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16].upper()
    
    def _generate_activation_code(self) -> str:
        """Generate a unique activation code"""
        # Generate 16-character alphanumeric code
        return ''.join(secrets.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(16))
    
    def _verify_activation_code(self, license_key_id: int, activation_code: str) -> bool:
        """Verify an activation code"""
        code = self.db.exec(
            select(OfflineActivationCode).where(
                OfflineActivationCode.license_key_id == license_key_id,
                OfflineActivationCode.activation_code == activation_code,
                OfflineActivationCode.is_used == False,
                OfflineActivationCode.expires_at > datetime.now(timezone.utc)
            )
        ).first()
        
        if code:
            # Mark as used
            code.is_used = True
            code.used_at = datetime.now(timezone.utc)
            self.db.add(code)
            self.db.commit()
            return True
        
        return False
    
    def _to_response(self, form: ActivationForm) -> ActivationFormResponse:
        """Convert database model to response schema"""
        return ActivationFormResponse(
            id=form.id,
            license_key_id=form.license_key_id,
            machine_id=form.machine_id,
            machine_name=form.machine_name,
            request_code=form.request_code,
            activation_code=form.activation_code,
            status=form.status,
            expires_at=form.expires_at,
            created_at=form.created_at,
            completed_at=form.completed_at
        )
    
    def _to_offline_response(self, code: OfflineActivationCode) -> OfflineActivationCodeResponse:
        """Convert offline activation code to response schema"""
        return OfflineActivationCodeResponse(
            id=code.id,
            license_key_id=code.license_key_id,
            activation_code=code.activation_code,
            machine_id=code.machine_id,
            is_used=code.is_used,
            expires_at=code.expires_at,
            created_at=code.created_at,
            used_at=code.used_at
        ) 