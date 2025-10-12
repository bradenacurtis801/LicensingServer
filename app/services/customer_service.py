"""
Customer service for managing customers
"""
import json
from typing import List, Optional, Dict, Any
from sqlmodel import Session, select
from app.models.database import Customer, User
from app.models.schemas import CustomerCreate, CustomerResponse, CustomerUpdate
from app.core.exceptions import CustomerNotFoundException


class CustomerService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_customer(self, customer_data: CustomerCreate, user: User) -> CustomerResponse:
        """Create a new customer"""
        # Check if customer with same email already exists for this user
        existing_customer = self.db.exec(
            select(Customer).where(
                Customer.email == customer_data.email,
                Customer.user_id == user.id
            )
        ).first()
        
        if existing_customer:
            from app.core.exceptions import CustomerAlreadyExistsException
            raise CustomerAlreadyExistsException(customer_data.email)
        
        # Create customer with user ownership
        db_customer = Customer(
            name=customer_data.name,
            email=customer_data.email,
            company=customer_data.company,
            user_id=user.id
        )
        
        self.db.add(db_customer)
        self.db.commit()
        self.db.refresh(db_customer)
        
        return self._to_response(db_customer)
    
    def get_customer(self, customer_id: int, user: User) -> CustomerResponse:
        """Get a customer by ID (with ownership check)"""
        customer = self.db.exec(
            select(Customer).where(
                Customer.id == customer_id,
                Customer.user_id == user.id
            )
        ).first()
        
        if not customer:
            raise CustomerNotFoundException(customer_id)
        
        return self._to_response(customer)
    
    def get_customer_by_email(self, email: str, user: User) -> Optional[CustomerResponse]:
        """Get a customer by email (with ownership check)"""
        customer = self.db.exec(
            select(Customer).where(
                Customer.email == email,
                Customer.user_id == user.id
            )
        ).first()
        
        if not customer:
            return None
        
        return self._to_response(customer)
    
    def list_customers(self, user: User, skip: int = 0, limit: int = 100) -> List[CustomerResponse]:
        """List all customers for a user"""
        customers = self.db.exec(
            select(Customer)
            .where(Customer.user_id == user.id)
            .offset(skip)
            .limit(limit)
        ).all()
        
        return [self._to_response(customer) for customer in customers]
    
    def update_customer(self, customer_id: int, customer_update: CustomerUpdate, user: User) -> CustomerResponse:
        """Update a customer (with ownership check)"""
        customer = self.db.exec(
            select(Customer).where(
                Customer.id == customer_id,
                Customer.user_id == user.id
            )
        ).first()
        
        if not customer:
            raise CustomerNotFoundException(customer_id)
        
        # Update fields
        update_data = customer_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(customer, field, value)
        
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        
        return self._to_response(customer)
    
    def delete_customer(self, customer_id: int, user: User) -> bool:
        """Delete a customer (with ownership check)"""
        customer = self.db.exec(
            select(Customer).where(
                Customer.id == customer_id,
                Customer.user_id == user.id
            )
        ).first()
        
        if not customer:
            return False
        
        self.db.delete(customer)
        self.db.commit()
        return True
    
    def get_or_create_customer(self, customer_data: CustomerCreate, user: User) -> CustomerResponse:
        """Get existing customer or create new one"""
        # Try to find existing customer
        existing_customer = self.db.exec(
            select(Customer).where(
                Customer.email == customer_data.email,
                Customer.user_id == user.id
            )
        ).first()
        
        if existing_customer:
            return self._to_response(existing_customer)
        
        # Create new customer
        return self.create_customer(customer_data, user)
    
    def _to_response(self, customer: Customer) -> CustomerResponse:
        """Convert Customer model to CustomerResponse"""
        return CustomerResponse(
            id=customer.id,
            name=customer.name,
            email=customer.email,
            company=customer.company,
            created_at=customer.created_at
        )