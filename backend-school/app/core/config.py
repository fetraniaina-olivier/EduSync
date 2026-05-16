# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    MINISTRY_API_URL: str
    SCHOOL_CODE: str
    SCHOOL_SECRET: str
    SCHOOL_ID: str
    DATABASE_URL: str = "sqlite+aiosqlite:///./school.db"

    # ✅ Configuration pour charger automatiquement .env
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# ✅ Instance globale
settings = Settings()