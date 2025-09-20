"""
Configuration management for the Advanced Accounts Agent.
Handles environment variables and application settings.
"""

import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Google AI Studio Configuration
    google_ai_api_key: str = Field(default="", alias="GOOGLE_AI_STUDIO_API_KEY")
    google_ai_model: str = Field(default="gemini-1.5-flash", alias="GOOGLE_AI_MODEL")
    
    # Xero Configuration
    xero_client_id: str = Field(default="", alias="XERO_CLIENT_ID")
    xero_client_secret: str = Field(default="", alias="XERO_CLIENT_SECRET")
    xero_tenant_id: Optional[str] = Field(default=None, alias="XERO_TENANT_ID")
    
    # Application Configuration
    app_name: str = Field(default="Advanced Accounts Agent", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    
    # Server Configuration
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    
    # Agent Configuration
    max_retries: int = Field(default=3, env="MAX_RETRIES")
    timeout_seconds: int = Field(default=30, env="TIMEOUT_SECONDS")
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore"
    }


# Global settings instance - load dotenv first
load_dotenv()
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings


def validate_environment() -> bool:
    """Validate that all required environment variables are set."""
    settings = get_settings()
    
    missing_vars = []
    if not settings.google_ai_api_key:
        missing_vars.append("GOOGLE_AI_STUDIO_API_KEY")
    if not settings.xero_client_id:
        missing_vars.append("XERO_CLIENT_ID")
    if not settings.xero_client_secret:
        missing_vars.append("XERO_CLIENT_SECRET")
    
    if missing_vars:
        print(f"⚠️  Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these variables in your environment or create a .env file")
        print("Example .env file content:")
        print("GOOGLE_AI_STUDIO_API_KEY=your_google_ai_studio_api_key_here")
        print("XERO_CLIENT_ID=your_xero_client_id_here")
        print("XERO_CLIENT_SECRET=your_xero_client_secret_here")
        return False
    
    return True


if __name__ == "__main__":
    # Test configuration loading
    if validate_environment():
        print("✅ Configuration loaded successfully!")
        print(f"App: {settings.app_name} v{settings.app_version}")
        print(f"Google AI Model: {settings.google_ai_model}")
        print(f"Server: {settings.host}:{settings.port}")
    else:
        print("❌ Configuration validation failed!")
