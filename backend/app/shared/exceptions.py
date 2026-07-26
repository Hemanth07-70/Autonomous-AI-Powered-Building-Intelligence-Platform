from typing import Any, Dict, Optional


class BaseAppException(Exception):
    """
    Enterprise base exception hierarchy for IntelliBuild AI.
    """

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(message)


class SimulationException(BaseAppException):
    """
    Raised when the simulation encounters a functional error.
    """

    pass


class ConfigurationException(BaseAppException):
    """
    Raised when there is an invalid configuration state.
    """

    pass


class ValidationException(BaseAppException):
    """
    Raised when validation of state or data fails.
    """

    pass
