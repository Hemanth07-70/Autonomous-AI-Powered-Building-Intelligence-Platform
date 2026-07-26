from typing import Any, MutableMapping

import structlog


def drop_healthcheck_logs(
    logger: structlog.types.WrappedLogger,
    method_name: str,
    event_dict: MutableMapping[str, Any],
) -> MutableMapping[str, Any]:
    """
    Structlog processor that filters out high-frequency, low-value health check logs.
    If a log matches the health check path, raise structlog.DropEvent.
    """
    url = event_dict.get("url", "")
    if isinstance(url, str) and "/health" in url:
        raise structlog.DropEvent

    return event_dict
