"""
Application endpoints for managing applications
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.services.application_service import ApplicationService
from app.models.schemas import ApplicationCreate, ApplicationResponse, ApplicationUpdate
from app.models.database import User
from app.dependencies import (
    get_application_service, require_application_read, require_application_write, 
    require_application_delete
)

router = APIRouter()


@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(
    application_data: ApplicationCreate,
    current_user: User = Depends(require_application_write()),
    service: ApplicationService = Depends(get_application_service)
) -> ApplicationResponse:
    """Create a new application"""
    return service.create_application(application_data, current_user)


@router.get("/", response_model=List[ApplicationResponse])
def list_applications(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_application_read()),
    service: ApplicationService = Depends(get_application_service)
) -> List[ApplicationResponse]:
    """List all applications for the authenticated user"""
    return service.list_applications(current_user, skip=skip, limit=limit)


@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(
    application_id: int,
    current_user: User = Depends(require_application_read()),
    service: ApplicationService = Depends(get_application_service)
) -> ApplicationResponse:
    """Get a specific application"""
    return service.get_application(application_id, current_user)


@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: int,
    application_update: ApplicationUpdate,
    current_user: User = Depends(require_application_write()),
    service: ApplicationService = Depends(get_application_service)
) -> ApplicationResponse:
    """Update an application"""
    return service.update_application(application_id, application_update, current_user)


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    application_id: int,
    current_user: User = Depends(require_application_delete()),
    service: ApplicationService = Depends(get_application_service)
):
    """Delete an application"""
    success = service.delete_application(application_id, current_user)
    if not success:
        raise HTTPException(status_code=404, detail="Application not found")
    
    return None