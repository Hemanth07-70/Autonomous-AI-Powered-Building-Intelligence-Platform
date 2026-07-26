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

    # Ollama settings
    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen3"
    OLLAMA_TIMEOUT: float = 30.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()
