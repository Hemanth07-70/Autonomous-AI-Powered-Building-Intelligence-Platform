from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnergyPlusConfig(BaseSettings):
    """
    Configuration for the EnergyPlus Simulation Engine adapter.
    Values can be overridden by environment variables prefixed with EPLUS_.
    """

    # Core paths
    energyplus_path: str = Field(
        default="/usr/local/EnergyPlus-23-2-0",
        description="Path to the EnergyPlus installation directory.",
    )
    idf_file_path: str = Field(
        default="models/building.idf",
        description="Path to the EnergyPlus IDF building model.",
    )
    weather_file_path: str = Field(
        default="models/weather.epw",
        description="Path to the EnergyPlus EPW weather file.",
    )
    output_directory: str = Field(
        default="eplus_out",
        description="Directory to store EnergyPlus simulation output files.",
    )

    # Runtime constraints
    timeout_seconds: int = Field(
        default=3600,
        description="Maximum allowed time for a single simulation run in seconds.",
    )
    max_runtime_minutes: int = Field(
        default=60, description="Maximum logical runtime allowed."
    )
    log_level: str = Field(
        default="INFO", description="Logging level for the EnergyPlus runtime engine."
    )

    model_config = SettingsConfigDict(
        env_prefix="EPLUS_", env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    def validate_paths(self):
        """
        Ensures that required directories exist or can be created.
        (Note: checking if IDF/EPW exist is handled by idf_loader and weather).
        """
        out_dir = Path(self.output_directory)
        if not out_dir.exists():
            out_dir.mkdir(parents=True, exist_ok=True)
