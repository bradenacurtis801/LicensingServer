from fastapi import APIRouter, Depends, status
from typing import List
from app.services.activation_form_service import ActivationFormService
from app.models.schemas import (
    ActivationFormCreate, ActivationFormResponse, ActivationFormComplete,
    OfflineActivationCodeCreate, OfflineActivationCodeResponse
)
from app.dependencies import get_activation_form_service

router = APIRouter()

@router.post("/", response_model=ActivationFormResponse, status_code=status.HTTP_201_CREATED)
def create_activation_form(
    form_data: ActivationFormCreate,
    service: ActivationFormService = Depends(get_activation_form_service)
):
    """Create a new activation form request (for offline computers)"""
    return service.create_activation_form(form_data)

@router.post("/complete", response_model=ActivationFormResponse)
def complete_activation_form(
    complete_data: ActivationFormComplete,
    service: ActivationFormService = Depends(get_activation_form_service)
):
    """Complete an activation form with activation code"""
    return service.complete_activation_form(complete_data)

@router.post("/offline-codes", response_model=List[OfflineActivationCodeResponse])
def generate_offline_codes(
    code_data: OfflineActivationCodeCreate,
    service: ActivationFormService = Depends(get_activation_form_service)
):
    """Generate offline activation codes for a license"""
    return service.generate_offline_activation_codes(code_data)

@router.get("/", response_model=List[ActivationFormResponse])
def list_activation_forms(
    skip: int = 0,
    limit: int = 100,
    service: ActivationFormService = Depends(get_activation_form_service)
):
    """List all activation forms"""
    return service.list_activation_forms(skip=skip, limit=limit)

@router.get("/{form_id}", response_model=ActivationFormResponse)
def get_activation_form(
    form_id: int,
    service: ActivationFormService = Depends(get_activation_form_service)
):
    """Get a specific activation form"""
    return service.get_activation_form(form_id) 