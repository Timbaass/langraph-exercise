from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    GROQ_API_KEY: str
    POSTGRES_DB_URI: str
    ENUYGUN_MCP_URL: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", env_file_encoding="utf-8", extra="ignore"
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()
