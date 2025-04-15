import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"  # Алгоритм для JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Время жизни токена

    TOKEN_URL: str
    MEMBERSHIP_SERVICE_URL: str
    
    class Config:
        env_file = ".env"


settings = Settings()