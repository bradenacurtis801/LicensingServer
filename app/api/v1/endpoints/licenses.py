"""
License endpoints for managing license keys
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.services.license_service import LicenseService
from app.models.schemas import LicenseKeyCreate, LicenseKeyResponse, LicenseKeyUpdate
from app.models.database import User
from app.dependencies import (
    get_license_service, require_license_read, require_license_write, 
    require_license_delete
)

router = APIRouter()


@router.post("/", response_model=LicenseKeyResponse, status_code=status.HTTP_201_CREATED)
def create_license(
    license_data: LicenseKeyCreate,
    current_user: User = Depends(require_license_write()),
    service: LicenseService = Depends(get_license_service)
) -> LicenseKeyResponse:
    """Create a new license key"""
    return service.create_license(license_data, current_user)


@router.get("/", response_model=List[LicenseKeyResponse])
def list_licenses(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_license_read()),
    service: LicenseService = Depends(get_license_service)
) -> List[LicenseKeyResponse]:
    """List all licenses for the authenticated user"""
    return service.list_licenses(current_user, skip=skip, limit=limit)


@router.get("/{license_id}", response_model=LicenseKeyResponse)
def get_license(
    license_id: int,
    current_user: User = Depends(require_license_read()),
    service: LicenseService = Depends(get_license_service)
) -> LicenseKeyResponse:
    """Get a specific license"""
    return service.get_license(license_id, current_user)


@router.put("/{license_id}", response_model=LicenseKeyResponse)
def update_license(
    license_id: int,
    license_update: LicenseKeyUpdate,
    current_user: User = Depends(require_license_write()),
    service: LicenseService = Depends(get_license_service)
) -> LicenseKeyResponse:
    """Update a license"""
    return service.update_license(license_id, license_update, current_user)


@router.delete("/{license_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_license(
    license_id: int,
    current_user: User = Depends(require_license_delete()),
    service: LicenseService = Depends(get_license_service)
):
    """Delete a license"""
    success = service.delete_license(license_id, current_user)
    if not success:
        raise HTTPException(status_code=404, detail="License not found")
    
    return None


@router.post("/{license_id}/block", response_model=LicenseKeyResponse)
def block_license(
    license_id: int,
    current_user: User = Depends(require_license_write()),
    service: LicenseService = Depends(get_license_service)
) -> LicenseKeyResponse:
    """Block a license key"""
    return service.block_license(license_id, current_user)


@router.post("/{license_id}/unblock", response_model=LicenseKeyResponse)
def unblock_license(
    license_id: int,
    current_user: User = Depends(require_license_write()),
    service: LicenseService = Depends(get_license_service)
) -> LicenseKeyResponse:
    """Unblock a license key"""
    return service.unblock_license(license_id, current_user)