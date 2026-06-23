"""APP configuration settings."""

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OPENAI_API_KEY: SecretStr = Field(
        ..., description="OpenAI secret key for LangChain"
    )
    APP_ENV: str = Field(
        default="production", description="Application environment (dev/prod)"
    )
    LOG_LEVEL: str = Field(
        default="INFO", description="Global application logging level"
    )

    model_config = SettingsConfigDict(
        env_file="../.env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
