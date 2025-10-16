# app/config.py
from pydantic_settings import BaseSettings
from typing import Optional, List
import os
import logging
from pydantic import Field, model_validator
from urllib.parse import quote_plus
from pathlib import Path
from typing import Literal

# Set up logger
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    node_env: Literal["dev", "prod", "development", "production"] = Field(default="dev")

    # Database
    database_url: str = Field(
        default="",
        description="Database connection URL (auto-constructed if empty)"
    )
    
    # PostgreSQL Settings
    postgres_username: str = Field(
        default="postgres",
        description="PostgreSQL username"
    )
    postgres_password: str = Field(
        default="password",
        description="PostgreSQL password"
    )
    postgres_db_name: str = Field(
        default="license_db",
        description="PostgreSQL database name"
    )
    postgres_host: str = Field(
        default="localhost",
        description="PostgreSQL host"
    )
    postgres_port: str = Field(
        default="5432",
        description="PostgreSQL port"
    )
    
    # App Managed Database Settings
    app_managed_db: bool = Field(
        default=False,
        description="Let the app manage database (create container and store in app data dir)"
    )
    
    # Application
    app_name: str = Field(
        default="License Management System",
        description="Application name"
    )
    app_version: str = Field(
        default="1.0.0",
        description="Application version"
    )
    debug: bool = Field(
        default=False,
        description="Debug mode"
    )
    backend_port: int = Field(
        default=8000,
        description="Backend port"
    )
    
    # Security
    secret_key: str = Field(
        default="your-super-secret-key-change-in-production-use-openssl-rand-hex-32",
        description="Secret key for JWT tokens"
    )
    
    # License settings
    license_key_length: int = Field(
        default=25,
        description="Length of generated license keys"
    )
    license_key_format: str = Field(
        default="XXXXX-XXXXX-XXXXX-XXXXX-XXXXX",
        description="Format template for license keys"
    )
    max_activations_default: int = Field(
        default=1,
        description="Default maximum activations per license"
    )
    
    # API settings
    api_v1_prefix: str = Field(
        default="/api/v1",
        description="API v1 prefix"
    )
    cors_origins: List[str] = Field(
        default=["*"],
        description="CORS allowed origins"
    )
    
    # Rate limiting
    rate_limit_requests: int = Field(
        default=100,
        description="Rate limit requests per window"
    )
    
    # RSA Signature Settings
    rsa_secret: Optional[str] = Field(
        default=None,
        description="RSA secret for signature verification (from RSA_SECRET env var)"
    )
    rate_limit_window: int = Field(
        default=3600,
        description="Rate limit window in seconds"
    )

    @property
    def node_env_value(self) -> str:
        """Map NODE_ENV environment variable to internal values."""
        import os

        env_value = os.getenv("NODE_ENV", "development")
        if env_value in ["production", "prod"]:
            return "prod"
        return "dev"
    
    @model_validator(mode='after')
    def construct_database_url(self):
        """Construct database URL if not provided"""
        if not self.database_url or self.database_url.strip() == "":
            # Check if app-managed PostgreSQL container is running
            try:
                from app.scripts.db_management import is_app_managed_postgres_running, get_app_managed_postgres_url
                if self.app_managed_db and is_app_managed_postgres_running():
                    self.database_url = get_app_managed_postgres_url()
                    logger.info(f"Using app-managed PostgreSQL: {self.database_url}")
                    return self
            except ImportError:
                pass
            
            # Use PostgreSQL with environment settings
            if self.postgres_password:
                self.database_url = (
                    f"postgresql://{quote_plus(self.postgres_username)}:{quote_plus(self.postgres_password)}"
                    f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db_name}"
                )
            else:
                self.database_url = (
                    f"postgresql://{quote_plus(self.postgres_username)}"
                    f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db_name}"
                )
            logger.info(f"Using environment PostgreSQL: {self.database_url}")
        
        # Load RSA secret from environment
        if not self.rsa_secret:
            self.rsa_secret = os.getenv("RSA_SECRET")
            if self.rsa_secret:
                logger.info("RSA secret loaded from environment")
            else:
                logger.warning("No RSA_SECRET found in environment - signature verification disabled")
        
        return self
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        env_file_encoding = "utf-8"

# Create global settings instance
settings = Settings()

is_development = settings.node_env_value == "dev"
is_production = settings.node_env_value == "prod"