from typing import Any, Dict

from structlog.contextvars import bind_contextvars, clear_contextvars, get_contextvars


class LoggingContextManager:
    """
    Manages the thread-local context variables for structlog.
    Useful for binding request IDs, user IDs, or simulation tick numbers
    to all logs emitted within a given execution context.
    """

    @staticmethod
    def bind(**kwargs: Any) -> None:
        """Binds key-value pairs to the current log context."""
        bind_contextvars(**kwargs)

    @staticmethod
    def clear() -> None:
        """Clears all bound context variables."""
        clear_contextvars()

    @staticmethod
    def get_context() -> Dict[str, Any]:
        """Retrieves the currently bound context variables."""
        return get_contextvars()
