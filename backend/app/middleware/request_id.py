import uuid
from typing import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from structlog.contextvars import bind_contextvars, clear_contextvars


class RequestIdMiddleware(BaseHTTPMiddleware):
    """
    Middleware to generate a unique request ID for each incoming request
    and bind it to the structlog context variables.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # Clear previous context variables to avoid cross-request contamination
        clear_contextvars()

        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        bind_contextvars(request_id=request_id)

        # Attach request_id to request state so other parts of the app can access it
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        return response
