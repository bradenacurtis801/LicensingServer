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
    
    # License settings
    license_key_length: int = Field(
        default=25,
        description="Length of generated license keys"
    )
    license_key_format: str = Field(
        default="XXXXX-XXXXX-XXXXX-XXXXX-XXXXX",
        description="Format template for license keys"
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
    
    # RSA Signature Settings
    rsa_private_key_path: Optional[str] = Field(
        default=None,
        description="Path to RSA private key PEM file for signing validation responses"
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
        
        return self
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        env_file_encoding = "utf-8"

# Create global settings instance
settings = Settings()

is_development = settings.node_env_value == "dev"
is_production = settings.node_env_value == "prod"