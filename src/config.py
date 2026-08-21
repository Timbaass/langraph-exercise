from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from pathlib import Path

from langchain_openai import ChatOpenAI

BASE_DIR = Path(__file__).resolve().parent.parent

GROQ_MODEL = "openai/gpt-oss-120b"
ROUTING_MODEL = "openai/gpt-oss-20b"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    GROQ_API_KEY: str
    POSTGRES_DB_URI: str
    ENUYGUN_MCP_URL: str
    LANGFUSE_SECRET_KEY: str
    LANGFUSE_PUBLIC_KEY: str
    LANGFUSE_BASE_URL: str
    LITELLM_API_KEY: str
    LITELLM_BASE_URL: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", env_file_encoding="utf-8", extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


def create_qwen_llm(model: str = "Qwen/Qwen3.5-122B", enable_thinking: bool = False) -> ChatOpenAI:
    return ChatOpenAI(
        model=model,
        openai_api_key=get_settings().LITELLM_API_KEY,
        openai_api_base=get_settings().LITELLM_BASE_URL,
        temperature=0,
        extra_body={"chat_template_kwargs": {"enable_thinking": enable_thinking}},
    )