from typing import Any, Tuple

import structlog


def configure_custom_logging(debug_mode: bool) -> Tuple[Any, ...]:
    """
    Returns the tuple of structlog processors based on environment.
    This logic can be utilized by the core logging setup to keep it clean.
    """
    processors: Tuple[Any, ...] = (
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    )

    if debug_mode:
        processors += (structlog.dev.ConsoleRenderer(colors=True),)
    else:
        processors += (structlog.processors.JSONRenderer(),)

    return processors
