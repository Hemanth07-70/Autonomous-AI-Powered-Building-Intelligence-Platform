from pathlib import Path

from app.energyplus.errors import MissingWeatherError


class WeatherManager:
    """
    Utility for validating and introspecting EnergyPlus EPW weather files.
    """

    @staticmethod
    def validate(epw_path: str) -> Path:
        """
        Validates that the given EPW weather path exists.

        Args:
            epw_path: Path to the EPW file.

        Raises:
            MissingWeatherError: If the file does not exist or is not a file.

        Returns:
            Path object of the validated EPW file.
        """
        path = Path(epw_path)
        if not path.exists():
            raise MissingWeatherError(f"EPW file not found at path: {path.absolute()}")
        if not path.is_file():
            raise MissingWeatherError(f"Path is not a valid file: {path.absolute()}")
        return path
