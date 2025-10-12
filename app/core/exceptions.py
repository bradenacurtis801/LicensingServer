from fastapi import HTTPException, status

class LicenseManagementException(Exception):
    """Base exception for license management system"""
    pass

class LicenseNotFoundException(LicenseManagementException):
    """Raised when license key is not found"""
    pass

class LicenseExpiredException(LicenseManagementException):
    """Raised when license has expired"""
    pass

class LicenseInactiveException(LicenseManagementException):
    """Raised when license is not active"""
    pass

class MaxActivationsReachedException(LicenseManagementException):
    """Raised when maximum activations are reached"""
    pass

class InvalidLicenseFormatException(LicenseManagementException):
    """Raised when license key format is invalid"""
    pass

class CustomerNotFoundException(LicenseManagementException):
    """Raised when customer is not found"""
    def __init__(self, customer_id: int):
        self.customer_id = customer_id
        super().__init__(f"Customer {customer_id} not found")

class ApplicationNotFoundException(LicenseManagementException):
    """Raised when application is not found"""
    def __init__(self, application_id: int):
        self.application_id = application_id
        super().__init__(f"Application {application_id} not found")

class ActivationFormNotFoundException(LicenseManagementException):
    """Raised when activation form is not found"""
    def __init__(self, message: str):
        super().__init__(message)

# Authentication exceptions
class AuthenticationException(LicenseManagementException):
    """Base class for authentication exceptions"""
    pass

class UserNotFoundException(AuthenticationException):
    """Raised when user is not found"""
    def __init__(self, message: str = "User not found"):
        super().__init__(message)

class InvalidCredentialsException(AuthenticationException):
    """Raised when credentials are invalid"""
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message)

class TokenNotFoundException(AuthenticationException):
    """Raised when token is not found"""
    def __init__(self, message: str = "Token not found"):
        super().__init__(message)

class PermissionDeniedException(AuthenticationException):
    """Raised when user lacks required permissions"""
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message)

class TokenExpiredException(AuthenticationException):
    """Raised when token has expired"""
    def __init__(self, message: str = "Token has expired"):
        super().__init__(message)

class InvalidTokenException(AuthenticationException):
    """Raised when token is invalid"""
    def __init__(self, message: str = "Invalid token"):
        super().__init__(message)

class UserAlreadyExistsException(AuthenticationException):
    """Raised when trying to create a user that already exists"""
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(f"User with {field} '{value}' already exists")

class CustomerAlreadyExistsException(LicenseManagementException):
    """Raised when trying to create a customer that already exists"""
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Customer with email '{email}' already exists")

class ApplicationAlreadyExistsException(LicenseManagementException):
    """Raised when trying to create an application that already exists"""
    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Application with name '{name}' already exists")

# HTTP Exception mapping
def map_to_http_exception(exc: LicenseManagementException) -> HTTPException:
    """Map custom exceptions to HTTP exceptions"""
    mapping = {
        # License exceptions
        LicenseNotFoundException: (status.HTTP_404_NOT_FOUND, "License key not found"),
        LicenseExpiredException: (status.HTTP_403_FORBIDDEN, "License has expired"),
        LicenseInactiveException: (status.HTTP_403_FORBIDDEN, "License is not active"),
        MaxActivationsReachedException: (status.HTTP_403_FORBIDDEN, "Maximum activations reached"),
        InvalidLicenseFormatException: (status.HTTP_400_BAD_REQUEST, "Invalid license key format"),
        CustomerNotFoundException: (status.HTTP_404_NOT_FOUND, lambda exc: f"Customer {exc.customer_id} not found"),
        ApplicationNotFoundException: (status.HTTP_404_NOT_FOUND, lambda exc: f"Application {exc.application_id} not found"),
        ActivationFormNotFoundException: (status.HTTP_404_NOT_FOUND, "Activation form not found"),
        
        # Authentication exceptions
        UserNotFoundException: (status.HTTP_404_NOT_FOUND, lambda exc: str(exc)),
        InvalidCredentialsException: (status.HTTP_401_UNAUTHORIZED, lambda exc: str(exc)),
        TokenNotFoundException: (status.HTTP_404_NOT_FOUND, lambda exc: str(exc)),
        PermissionDeniedException: (status.HTTP_403_FORBIDDEN, lambda exc: str(exc)),
        TokenExpiredException: (status.HTTP_401_UNAUTHORIZED, lambda exc: str(exc)),
        InvalidTokenException: (status.HTTP_401_UNAUTHORIZED, lambda exc: str(exc)),
        UserAlreadyExistsException: (status.HTTP_400_BAD_REQUEST, lambda exc: str(exc)),
        CustomerAlreadyExistsException: (status.HTTP_400_BAD_REQUEST, lambda exc: str(exc)),
        ApplicationAlreadyExistsException: (status.HTTP_400_BAD_REQUEST, lambda exc: str(exc)),
        AuthenticationException: (status.HTTP_401_UNAUTHORIZED, lambda exc: str(exc)),
    }
    
    if type(exc) in mapping:
        status_code, detail = mapping[type(exc)]
        if callable(detail):
            detail = detail(exc)
        return HTTPException(status_code=status_code, detail=detail)
    
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error"
    )

# Exception handler decorator for FastAPI routes
def handle_exceptions(func):
    """Decorator to automatically handle custom exceptions in FastAPI routes"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except LicenseManagementException as exc:
            raise map_to_http_exception(exc)
    return wrapper