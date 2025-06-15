from pydantic_settings import BaseSettings
from typing import List, Optional
from pathlib import Path

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "Price Intelligence System"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 1
    
    # Security
    SECRET_KEY: str = Field(
        default="your-secret-key-here",  # Change this in production!
        description="Secret key for JWT token generation and other security needs"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    
    # Database (imported from database.py)
    DATABASE_URL: str = db_settings.DATABASE_URL
    ASYNC_DATABASE_URL: str = db_settings.ASYNC_DATABASE_URL
    DB_POOL_SIZE: int = db_settings.DB_POOL_SIZE
    DB_MAX_OVERFLOW: int = db_settings.DB_MAX_OVERFLOW
    DB_POOL_TIMEOUT: int = db_settings.DB_POOL_TIMEOUT
    DB_POOL_RECYCLE: int = db_settings.DB_POOL_RECYCLE
    DB_ECHO: bool = db_settings.DB_ECHO
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Rate limiting
    RATE_LIMIT: int = 100  # requests per minute
    
    # Scraper settings
    SCRAPER_USER_AGENT: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    SCRAPER_TIMEOUT: int = 30  # seconds
    
    # Proxy settings
    USE_PROXIES: bool = False
    PROXY_LIST: List[str] = []
    
    # Redis settings (for rate limiting and caching)
    REDIS_URL: Optional[str] = None
    
    # Sentry settings (for error tracking)
    SENTRY_DSN: Optional[str] = None
    
    # Application URLs
    FRONTEND_URL: str = "http://localhost:3000"
    
    # File upload settings
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Email settings
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: str = "noreply@example.com"
    
    @property
    def is_production(self) -> bool:
        """Check if the application is running in production."""
        return self.ENVIRONMENT.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if the application is running in development."""
        return self.ENVIRONMENT.lower() == "development"
    
    @property
    def is_testing(self) -> bool:
        """Check if the application is running tests."""
        return self.ENVIRONMENT.lower() == "test"
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
        
        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            # Load .env file from project root if it exists
            env_file = Path(__file__).parent.parent / ".env"
            if env_file.exists():
                return env_settings, init_settings, file_secret_settings
            return env_settings, init_settings, file_secret_settings


# Create settings instance
settings = Settings()

# Ensure upload directory exists
import os
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

env_file = Path(".env")
if not env_file.exists():
    with open(env_file, "w") as f:
        f.write("""# Price Intelligence API Configuration
# Database
DATABASE_URL=sqlite:///./price_intelligence.db

# Security
SECRET_KEY=your-secret-key-here

# Logging
LOG_LEVEL=INFO
""")

settings = Settings()
