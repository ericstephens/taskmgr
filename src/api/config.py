"""
Configuration settings for the API.
"""
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """API settings."""
    API_TITLE: str = "Task Manager API"
    API_DESCRIPTION: str = "API for managing tasks in the Task Manager application"
    API_VERSION: str = "1.0.0"
    
    # Database settings
    DB_USER: str = os.getenv("DB_USER", "taskmgr")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "taskmgr_password")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "taskmgr_db")
    DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # CORS settings
    CORS_ORIGINS: list[str] = ["*"]  # In production, replace with specific origins
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]
    
    class Config:
        """Pydantic settings config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Create settings instance
settings = Settings()
