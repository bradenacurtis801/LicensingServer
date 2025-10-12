"""
Application service for managing applications
"""
import json
from typing import List, Optional, Dict, Any
from sqlmodel import Session, select
from app.models.database import Application, User
from app.models.schemas import ApplicationCreate, ApplicationResponse, ApplicationUpdate
from app.core.exceptions import ApplicationNotFoundException


class ApplicationService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_application(self, application_data: ApplicationCreate, user: User) -> ApplicationResponse:
        """Create a new application"""
        # Check if application with same name already exists for this user
        existing_application = self.db.exec(
            select(Application).where(
                Application.name == application_data.name,
                Application.user_id == user.id
            )
        ).first()
        
        if existing_application:
            from app.core.exceptions import ApplicationAlreadyExistsException
            raise ApplicationAlreadyExistsException(application_data.name)
        
        # Create application with user ownership
        db_application = Application(
            name=application_data.name,
            version=application_data.version,
            description=application_data.description,
            features=json.dumps(application_data.features) if application_data.features else None,
            user_id=user.id
        )
        
        self.db.add(db_application)
        self.db.commit()
        self.db.refresh(db_application)
        
        return self._to_response(db_application)
    
    def get_application(self, application_id: int, user: User) -> ApplicationResponse:
        """Get an application by ID (with ownership check)"""
        application = self.db.exec(
            select(Application).where(
                Application.id == application_id,
                Application.user_id == user.id
            )
        ).first()
        
        if not application:
            raise ApplicationNotFoundException(application_id)
        
        return self._to_response(application)
    
    def get_application_by_name(self, name: str, user: User) -> Optional[ApplicationResponse]:
        """Get an application by name (with ownership check)"""
        application = self.db.exec(
            select(Application).where(
                Application.name == name,
                Application.user_id == user.id
            )
        ).first()
        
        if not application:
            return None
        
        return self._to_response(application)
    
    def list_applications(self, user: User, skip: int = 0, limit: int = 100) -> List[ApplicationResponse]:
        """List all applications for a user"""
        applications = self.db.exec(
            select(Application)
            .where(Application.user_id == user.id)
            .offset(skip)
            .limit(limit)
        ).all()
        
        return [self._to_response(application) for application in applications]
    
    def update_application(self, application_id: int, application_update: ApplicationUpdate, user: User) -> ApplicationResponse:
        """Update an application (with ownership check)"""
        application = self.db.exec(
            select(Application).where(
                Application.id == application_id,
                Application.user_id == user.id
            )
        ).first()
        
        if not application:
            raise ApplicationNotFoundException(application_id)
        
        # Update fields
        update_data = application_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == 'features' and value is not None:
                setattr(application, field, json.dumps(value))
            else:
                setattr(application, field, value)
        
        self.db.add(application)
        self.db.commit()
        self.db.refresh(application)
        
        return self._to_response(application)
    
    def delete_application(self, application_id: int, user: User) -> bool:
        """Delete an application (with ownership check)"""
        application = self.db.exec(
            select(Application).where(
                Application.id == application_id,
                Application.user_id == user.id
            )
        ).first()
        
        if not application:
            return False
        
        self.db.delete(application)
        self.db.commit()
        return True
    
    def get_or_create_application(self, application_data: ApplicationCreate, user: User) -> ApplicationResponse:
        """Get existing application or create new one"""
        # Try to find existing application
        existing_application = self.db.exec(
            select(Application).where(
                Application.name == application_data.name,
                Application.user_id == user.id
            )
        ).first()
        
        if existing_application:
            return self._to_response(existing_application)
        
        # Create new application
        return self.create_application(application_data, user)
    
    def _to_response(self, application: Application) -> ApplicationResponse:
        """Convert Application model to ApplicationResponse"""
        features = None
        if application.features:
            try:
                features = json.loads(application.features)
            except json.JSONDecodeError:
                features = {}
        
        return ApplicationResponse(
            id=application.id,
            name=application.name,
            version=application.version,
            description=application.description,
            features=features,
            created_at=application.created_at
        )