"""
Customer endpoints for managing customers
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.services.customer_service import CustomerService
from app.models.schemas import CustomerCreate, CustomerResponse, CustomerUpdate
from app.models.database import User
from app.dependencies import (
    get_customer_service, require_customer_read, require_customer_write, 
    require_customer_delete
)

router = APIRouter()


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer_data: CustomerCreate,
    current_user: User = Depends(require_customer_write()),
    service: CustomerService = Depends(get_customer_service)
) -> CustomerResponse:
    """Create a new customer"""
    return service.create_customer(customer_data, current_user)


@router.get("/", response_model=List[CustomerResponse])
def list_customers(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_customer_read()),
    service: CustomerService = Depends(get_customer_service)
) -> List[CustomerResponse]:
    """List all customers for the authenticated user"""
    return service.list_customers(current_user, skip=skip, limit=limit)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    current_user: User = Depends(require_customer_read()),
    service: CustomerService = Depends(get_customer_service)
) -> CustomerResponse:
    """Get a specific customer"""
    return service.get_customer(customer_id, current_user)


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer_update: CustomerUpdate,
    current_user: User = Depends(require_customer_write()),
    service: CustomerService = Depends(get_customer_service)
) -> CustomerResponse:
    """Update a customer"""
    return service.update_customer(customer_id, customer_update, current_user)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    customer_id: int,
    current_user: User = Depends(require_customer_delete()),
    service: CustomerService = Depends(get_customer_service)
):
    """Delete a customer"""
    success = service.delete_customer(customer_id, current_user)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return None