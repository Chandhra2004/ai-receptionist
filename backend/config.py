from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    openai_api_key: str
    
    # LiveKit Configuration
    livekit_url: str = "ws://localhost:7880"
    livekit_api_key: str
    livekit_api_secret: str
    
    # Firebase Configuration
    firebase_credentials_path: str = "./firebase-credentials.json"
    
    # Application Configuration
    environment: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    frontend_url: str = "http://localhost:3000"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
