from typing import Any, Dict, Optional

from fastapi import status


class AppException(Exception):
    """
    Base exception for IntelliBuild AI application.
    All custom exceptions should inherit from this.
    """

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class NotFoundException(AppException):
    def __init__(
        self,
        message: str = "Resource not found",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, status.HTTP_404_NOT_FOUND, details)


class BadRequestException(AppException):
    def __init__(
        self, message: str = "Bad request", details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, details)


class UnauthorizedException(AppException):
    def __init__(
        self, message: str = "Unauthorized", details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED, details)
