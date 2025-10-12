from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.services.activation_service import ActivationService
from app.models.schemas import ActivationResponse
from app.models.database import User
from app.dependencies import get_activation_service, require_activation_read, require_activation_delete

router = APIRouter()

@router.get("/", response_model=List[ActivationResponse])
def list_activations(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_activation_read()),
    service: ActivationService = Depends(get_activation_service)
):
    """List activations for the authenticated user"""
    return service.list_activations_for_user(current_user, skip=skip, limit=limit)

@router.get("/license/{license_id}", response_model=List[ActivationResponse])
def get_license_activations(
    license_id: int,
    current_user: User = Depends(require_activation_read()),
    service: ActivationService = Depends(get_activation_service)
):
    """Get all activations for a specific license (user must own the license)"""
    return service.get_activations_for_license(license_id, current_user)

@router.delete("/{activation_id}")
def deactivate_machine(
    activation_id: int,
    current_user: User = Depends(require_activation_delete()),
    service: ActivationService = Depends(get_activation_service)
):
    """Deactivate a machine (user must own the activation)"""
    success = service.deactivate_machine(activation_id, current_user)
    if not success:
        raise HTTPException(status_code=404, detail="Activation not found or access denied")
    return {"message": "Machine deactivated successfully"}