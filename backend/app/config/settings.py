from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application Settings for IntelliBuild AI.
    Loads configurations from environment variables or .env file.
    """

    # Application settings
    APP_NAME: str = "IntelliBuild AI"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    LOG_LEVEL: Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"] = "INFO"

    # Database settings
    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/intellibuild"
    )

    # AI Provider settings
    AI_PROVIDER: str = "nvidia"
    NVIDIA_API_KEY: str = ""
    NVIDIA_MODEL: str = "meta/llama-3.1-70b-instruct"
    NVIDIA_BASE_URL: str = "https://integrate.api.nvidia.com/v1"
    AI_TEMPERATURE: float = 0.2
    AI_MAX_TOKENS: int = 2048
    AI_TIMEOUT: float = 120.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()
