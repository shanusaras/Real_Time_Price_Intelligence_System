"""
Database configuration for the Price Intelligence System.

This module handles database connection configuration and URL generation.
"""
from typing import Optional
from urllib.parse import quote_plus

from pydantic import PostgresDsn, validator
from pydantic_settings import BaseSettings

class DatabaseSettings(BaseSettings):
    """Database connection settings."""
    
    DB_DRIVER: str = "mysql+pymysql"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "price_intelligence"
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 3600
    DB_ECHO: bool = False
    
    @property
    def DATABASE_URL(self) -> str:
        """Generate the synchronous database URL."""
        return self._build_database_url(async_=False)
    
    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Generate the asynchronous database URL."""
        return self._build_database_url(async_=True)
    
    def _build_database_url(self, async_: bool = False) -> str:
        """Build the database URL based on the configuration."""
        driver = self.DB_DRIVER
        if async_ and driver.startswith("mysql"):
            driver = "mysql+aiomysql"
        
        return (
            f"{driver}://{self.DB_USER}:{quote_plus(self.DB_PASSWORD)}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"
        )
    
    class Config:
        env_prefix = "DB_"
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Create settings instance
db_settings = DatabaseSettings()

# Export settings
__all__ = ["db_settings"]
