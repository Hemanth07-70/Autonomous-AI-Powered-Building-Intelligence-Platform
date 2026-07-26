from abc import ABC, abstractmethod
from typing import Dict, Optional

import structlog

logger = structlog.get_logger("telemetry.metrics")


class MetricsInterface(ABC):
    """
    Interface for tracking business and technical metrics.
    """

    @abstractmethod
    def increment_counter(
        self, name: str, tags: Optional[Dict[str, str]] = None
    ) -> None:
        """Increments a counter metric."""
        pass

    @abstractmethod
    def record_gauge(
        self, name: str, value: float, tags: Optional[Dict[str, str]] = None
    ) -> None:
        """Records a point-in-time value."""
        pass


class DefaultMetrics(MetricsInterface):
    """
    Default implementation of metrics tracker routing to logs.
    """

    def __init__(self) -> None:
        logger.info("DefaultMetrics initialized")

    def increment_counter(
        self, name: str, tags: Optional[Dict[str, str]] = None
    ) -> None:
        tags = tags or {}
        logger.debug("Counter incremented", metric_name=name, tags=tags)

    def record_gauge(
        self, name: str, value: float, tags: Optional[Dict[str, str]] = None
    ) -> None:
        tags = tags or {}
        logger.debug("Gauge recorded", metric_name=name, value=value, tags=tags)
