"""
Constants for application data storage and configuration
"""
import os
import platform
import logging
from pathlib import Path
from typing import Dict, Any

# Set up logger
logger = logging.getLogger(__name__)

# System detection
SYSTEM = platform.system().lower()
IS_WINDOWS = SYSTEM == "windows"
IS_LINUX = SYSTEM == "linux"
IS_DARWIN = SYSTEM == "darwin"  # macOS

PROJECT_ROOT = Path(__file__).parent.parent.parent

# Base directories
if IS_WINDOWS:
    # Windows paths
    APP_DATA_BASE = Path(os.environ.get("APPDATA", os.path.expanduser("~")))
    LOGS_DIR = APP_DATA_BASE / "LicensingServer" / "logs"
    DATA_DIR = APP_DATA_BASE / "LicensingServer" / "data"
    CACHE_DIR = APP_DATA_BASE / "LicensingServer" / "cache"
    CONFIG_DIR = APP_DATA_BASE / "LicensingServer" / "config"
    TEMP_DIR = Path(os.getenv("TEMP", "C:/Windows/Temp")) / "LicensingServer"
    
elif IS_LINUX:
    # Linux paths (Docker-friendly)
    APP_DATA_BASE = Path("/var/lib/licensing-server")
    LOGS_DIR = Path("/var/log/licensing-server")
    DATA_DIR = Path("/var/lib/licensing-server/data")
    CACHE_DIR = Path("/var/cache/licensing-server")
    CONFIG_DIR = Path("/etc/licensing-server")
    TEMP_DIR = Path("/tmp/licensing-server")
    
else:
    # macOS paths
    APP_DATA_BASE = Path.home() / "Library" / "Application Support" / "LicensingServer"
    LOGS_DIR = APP_DATA_BASE / "logs"
    DATA_DIR = APP_DATA_BASE / "data"
    CACHE_DIR = APP_DATA_BASE / "cache"
    CONFIG_DIR = APP_DATA_BASE / "config"
    TEMP_DIR = Path("/tmp/licensing-server")

# File storage paths
FILE_PATHS = {
    "logs": LOGS_DIR,
    "data": DATA_DIR,
    "config": CONFIG_DIR,
    # "cache": CACHE_DIR,
    # "temp": TEMP_DIR,
    # "database_backups": DATA_DIR / "backups",
    # "license_files": DATA_DIR / "licenses",
    # "exports": DATA_DIR / "exports",
    # "uploads": DATA_DIR / "uploads"
}

# Logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(levelname)s - %(pathname)s:%(lineno)d - %(threadName)s - %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s - %(levelname)s - %(pathname)s:%(lineno)d - %(threadName)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "detailed",
            "filename": str(LOGS_DIR / "app.log"),
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        }
    },
    "loggers": {
        "": {
            "level": "INFO",
            "handlers": ["console"]
        },
        "app": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False
        },
        "sqlalchemy": {
            "level": logging.WARNING,
            "handlers": ["console", "file"],
            "propagate": False
        },
        "uvicorn": {
            "level": logging.INFO,
            "handlers": ["console", "file"],
            "propagate": False
        },
        "uvicorn.access": {
            "level": logging.WARNING,
            "handlers": ["console", "file"],
            "propagate": False
        }
    },

}

def ensure_directories():
    """Create all necessary directories if they don't exist"""
    for path_name, path in FILE_PATHS.items():
        if isinstance(path, Path):
            path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Ensured directory exists: {path}")

def get_database_config(environment: str = "development") -> Dict[str, Any]:
    """Get database configuration for specified environment"""
    # Import here to avoid circular import
    from app.config import settings
    
    return {
        "development": {
            "url": settings.database_url,
            "pool_size": 5,
            "max_overflow": 10,
            "pool_pre_ping": True,
            "pool_recycle": 300
        },
        "production": {
            "url": settings.database_url,
            "pool_size": 20,
            "max_overflow": 30,
            "pool_pre_ping": True,
            "pool_recycle": 3600
        },
        "docker": {
            "url": settings.database_url,
            "pool_size": 10,
            "max_overflow": 20,
            "pool_pre_ping": True,
            "pool_recycle": 300
        }
    }[environment]

def get_app_constants() -> Dict[str, Any]:
    """Get application constants using settings"""
    # Import here to avoid circular import
    from app.config import settings
    
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": "Enterprise license management and validation system",
        "max_file_size": 10 * 1024 * 1024,  # 10MB
        "max_upload_files": 5,
        "session_timeout": 3600,  # 1 hour
        "rate_limit_requests": settings.rate_limit_requests,
        "rate_limit_window": settings.rate_limit_window,
        "license_key_length": settings.license_key_length,
        "max_activations_default": settings.max_activations_default
    }

def get_security_constants() -> Dict[str, Any]:
    """Get security constants using settings"""
    # Import here to avoid circular import
    from app.config import settings
    
    return {
        "jwt_secret_key": settings.secret_key,
        "jwt_algorithm": "HS256",
        "jwt_expiration": 3600,  # 1 hour
        "password_min_length": 8,
        "bcrypt_rounds": 12,
        "api_key_length": 32
    }

def get_file_path(path_name: str) -> Path:
    """Get a specific file path by name"""
    if path_name not in FILE_PATHS:
        raise ValueError(f"Unknown path name: {path_name}")
    return FILE_PATHS[path_name]

def is_docker_environment() -> bool:
    """Check if running in Docker environment"""
    return os.path.exists("/.dockerenv") or os.getenv("DOCKER_ENV") == "true" 