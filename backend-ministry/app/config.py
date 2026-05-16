from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "Ministry Sync API"
    DEBUG: bool = False
    
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "ministry_db"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "secret"
    
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    SECRET_KEY: str = "change-me-in-prod"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()