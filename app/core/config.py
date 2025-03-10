"""Configuration settings for the application.

This module provides configuration settings for the application using Pydantic's
BaseSettings class, which loads environment variables and provides type validation.
"""

import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, EmailStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings.

    This class defines all the configuration settings for the application.
    Values are loaded from environment variables and validated.
    """

    # Configuration for loading environment variables
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )

    # API settings
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    PROJECT_NAME: str = "API Performance Optimization"
    DESCRIPTION: str = "High-performance API service with FastAPI, MySQL, and Redis"
    VERSION: str = "0.1.0"

    # CORS settings
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """Parse CORS origins from string or list.

        Args:
            v: String or list of CORS origins

        Returns:
            List of validated CORS origins
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database settings
    MYSQL_SERVER: str = "localhost"
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = ""
    MYSQL_DB: str = "api_performance"
    MYSQL_PORT: str = "3306"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @property
    def get_database_uri(self) -> str:
        """Get the database URI.

        Returns:
            Database URI string
        """
        if self.SQLALCHEMY_DATABASE_URI:
            return self.SQLALCHEMY_DATABASE_URI
        
        return (
            f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@"
            f"{self.MYSQL_SERVER}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
        )

    # Redis settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_CACHE_EXPIRE_SECONDS: int = 60 * 5  # 5 minutes

    # Rate limiting settings
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD_SECONDS: int = 60  # 1 minute

    # Email settings
    EMAILS_ENABLED: bool = False
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None
    EMAILS_TEMPLATES_DIR: str = "/app/app/email-templates/build"

    # Superuser settings
    FIRST_SUPERUSER: EmailStr = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin"

    # Logging settings
    LOG_LEVEL: str = "INFO"


# Create a global settings object
settings = Settings()