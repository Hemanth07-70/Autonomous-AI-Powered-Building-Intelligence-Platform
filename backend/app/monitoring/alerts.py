from typing import Callable, List

import structlog

logger = structlog.get_logger("monitoring.alerts")


class AlertManager:
    """
    Manages system alerts and notification dispatching based on threshold breaches.
    """

    def __init__(self) -> None:
        self._handlers: List[Callable[[str, str], None]] = []
        logger.info("AlertManager initialized")

    def register_handler(self, handler: Callable[[str, str], None]) -> None:
        """Registers a new alert output handler."""
        self._handlers.append(handler)
        logger.debug("Alert handler registered")

    def dispatch_alert(self, severity: str, message: str) -> None:
        """Dispatches an alert to all registered handlers."""
        logger.warning("Dispatching alert", severity=severity, message=message)
        for handler in self._handlers:
            try:
                handler(severity, message)
            except Exception as e:
                logger.error(
                    "Failed to execute alert handler", error=str(e), exc_info=True
                )
