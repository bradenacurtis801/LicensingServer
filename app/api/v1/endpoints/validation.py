from fastapi import APIRouter, Depends, Request
from app.services.validation_service import ValidationService
from app.models.schemas import LicenseValidationRequest, LicenseValidationResponse
from app.dependencies import get_validation_service

router = APIRouter()

@router.post("/", response_model=LicenseValidationResponse)
def validate_license(
    request: LicenseValidationRequest,
    client_request: Request,
    service: ValidationService = Depends(get_validation_service)
):
    """Validate a license key and machine combination"""
    client_ip = client_request.client.host if client_request.client else None
    return service.validate_license(request, client_ip)

@router.post("/heartbeat", response_model=LicenseValidationResponse)
def license_heartbeat(
    request: LicenseValidationRequest,
    client_request: Request,
    service: ValidationService = Depends(get_validation_service)
):
    """Send a heartbeat to keep activation alive (same as validation)"""
    client_ip = client_request.client.host if client_request.client else None
    return service.validate_license(request, client_ip)