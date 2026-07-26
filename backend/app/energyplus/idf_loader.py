from pathlib import Path

from app.energyplus.errors import MissingIDFError


class IDFLoader:
    """
    Utility for validating and introspecting EnergyPlus IDF files.
    """

    @staticmethod
    def validate(idf_path: str) -> Path:
        """
        Validates that the given IDF path exists.

        Args:
            idf_path: Path to the IDF file.

        Raises:
            MissingIDFError: If the file does not exist or is not a file.

        Returns:
            Path object of the validated IDF file.
        """
        path = Path(idf_path)
        if not path.exists():
            raise MissingIDFError(f"IDF file not found at path: {path.absolute()}")
        if not path.is_file():
            raise MissingIDFError(f"Path is not a valid file: {path.absolute()}")
        return path
