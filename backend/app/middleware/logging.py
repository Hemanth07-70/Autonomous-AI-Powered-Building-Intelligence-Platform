import time
from typing import Awaitable, Callable

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger("api.access")


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all incoming HTTP requests and their responses.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start_time = time.time()

        # Log request start
        logger.info(
            "Request started",
            method=request.method,
            url=str(request.url),
            client=request.client.host if request.client else None,
        )

        try:
            response = await call_next(request)

            # Calculate duration
            process_time = time.time() - start_time

            logger.info(
                "Request completed",
                method=request.method,
                url=str(request.url),
                status_code=response.status_code,
                duration_s=process_time,
            )
            return response

        except Exception as e:
            process_time = time.time() - start_time
            logger.exception(
                "Request failed",
                method=request.method,
                url=str(request.url),
                duration_s=process_time,
                error=str(e),
            )
            raise
