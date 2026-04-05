from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str = "postgresql://greenpulse:password@db:5432/greenpulse"
    api_title: str = "GreenPulse API"
    api_version: str = "1.0.0"
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
