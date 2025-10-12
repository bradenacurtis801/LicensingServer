# api.py
from fastapi import APIRouter
from app.api.v1.endpoints import applications, customers, licenses, activations, validation, activation_forms, auth

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(applications.router, prefix="/applications", tags=["Applications"])
api_router.include_router(customers.router, prefix="/customers", tags=["Customers"])
api_router.include_router(licenses.router, prefix="/licenses", tags=["Licenses"])
api_router.include_router(activations.router, prefix="/activations", tags=["Activations"])
api_router.include_router(validation.router, prefix="/validation", tags=["Validation"])
api_router.include_router(activation_forms.router, prefix="/activation-forms", tags=["Activation Forms"])
