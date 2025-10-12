from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlmodel import Session, select
from app.models.database import Activation, LicenseKey, ActivationStatus, User, UserRole, Application
from app.models.schemas import ActivationResponse
from app.core.exceptions import LicenseNotFoundException

class ActivationService:
    def __init__(self, db: Session):
        self.db = db
    
    def handle_activation(
        self, 
        license_key: LicenseKey, 
        machine_id: str, 
        client_ip: Optional[str] = None
    ) -> Dict[str, Any]:
        """Handle machine activation for a license"""
        
        # Check if machine is already activated
        existing_activation = self.db.exec(
            select(Activation).where(
                Activation.license_key_id == license_key.id,
                Activation.machine_id == machine_id,
                Activation.status == ActivationStatus.ACTIVE
            )
        ).first()
        
        if existing_activation:
            # Update heartbeat for existing activation
            existing_activation.last_heartbeat = datetime.now(timezone.utc)
            self.db.add(existing_activation)
            self.db.commit()
            
            return {
                "success": True,
                "activation_id": existing_activation.id,
                "message": "Machine already activated, heartbeat updated"
            }
        
        # Check activation limits
        if license_key.current_activations >= license_key.max_activations:
            return {
                "success": False,
                "remaining_activations": 0,
                "message": "Maximum activations reached"
            }
        
        # Create new activation
        activation = Activation(
            license_key_id=license_key.id,
            machine_id=machine_id,
            ip_address=client_ip,
            status=ActivationStatus.ACTIVE
        )
        self.db.add(activation)
        
        # Update license activation count
        license_key.current_activations += 1
        self.db.add(license_key)
        
        self.db.commit()
        self.db.refresh(activation)
        
        return {
            "success": True,
            "activation_id": activation.id,
            "remaining_activations": license_key.max_activations - license_key.current_activations,
            "message": "Machine activated successfully"
        }
    
    def deactivate_machine(self, activation_id: int, current_user: User) -> bool:
        """Deactivate a specific machine (user can only deactivate their own activations)"""
        activation = self.db.get(Activation, activation_id)
        if not activation:
            return False
        
        # Check if user can access this activation
        if not self._can_access_activation(activation, current_user):
            return False
        
        # Update license activation count
        license_key = self.db.get(LicenseKey, activation.license_key_id)
        if license_key and license_key.current_activations > 0:
            license_key.current_activations -= 1
            self.db.add(license_key)
        
        # Remove activation
        self.db.delete(activation)
        self.db.commit()
        
        return True
    
    def list_activations_for_user(self, current_user: User, skip: int = 0, limit: int = 100) -> List[ActivationResponse]:
        """List activations for a specific user (filtered by ownership)"""
        # Users can only see activations for their own licenses
        activations = self.db.exec(
            select(Activation)
            .join(LicenseKey)
            .join(Application)
            .where(Application.user_id == current_user.id)
            .offset(skip)
            .limit(limit)
        ).all()
        
        return [self._to_response(activation) for activation in activations]
    
    def get_activations_for_license(self, license_id: int, current_user: User) -> List[ActivationResponse]:
        """Get all activations for a specific license (filtered by ownership)"""
        license_key = self.db.get(LicenseKey, license_id)
        if not license_key:
            return []
        
        # Check if user can access this license
        if not self._can_access_license(license_key, current_user):
            return []
        
        activations = self.db.exec(
            select(Activation).where(Activation.license_key_id == license_id)
        ).all()
        
        return [self._to_response(activation) for activation in activations]
    
    def _can_access_activation(self, activation: Activation, user: User) -> bool:
        """Check if user can access a specific activation"""
        # Get the license key and check ownership
        license_key = self.db.get(LicenseKey, activation.license_key_id)
        if not license_key:
            return False
        
        return self._can_access_license(license_key, user)
    
    def _can_access_license(self, license_key: LicenseKey, user: User) -> bool:
        """Check if user can access a specific license"""
        # Check if the license belongs to an application owned by the user
        application = self.db.get(Application, license_key.application_id)
        if not application:
            return False
        
        return application.owner_id == user.id
    
    def _to_response(self, activation: Activation) -> ActivationResponse:
        """Convert database model to response schema"""
        return ActivationResponse(
            id=activation.id,
            license_key_id=activation.license_key_id,
            machine_id=activation.machine_id,
            machine_name=activation.machine_name,
            ip_address=activation.ip_address,
            status=activation.status,
            activated_at=activation.activated_at,
            last_heartbeat=activation.last_heartbeat
        )