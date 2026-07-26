class EnergyPlusError(Exception):
    """Base exception for all EnergyPlus related errors."""

    pass


class MissingIDFError(EnergyPlusError):
    """Raised when the specified IDF file cannot be found or read."""

    pass


class MissingWeatherError(EnergyPlusError):
    """Raised when the specified weather (EPW) file cannot be found or read."""

    pass


class EnergyPlusRuntimeError(EnergyPlusError):
    """Raised when the EnergyPlus engine encounters a fatal error during execution."""

    pass


class CallbackError(EnergyPlusError):
    """Raised when an error occurs during an EnergyPlus callback execution."""

    pass
