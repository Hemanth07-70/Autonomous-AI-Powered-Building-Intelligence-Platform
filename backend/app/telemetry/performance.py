import time
from contextlib import contextmanager
from typing import Iterator

import structlog

from app.telemetry.metrics import MetricsInterface

logger = structlog.get_logger("telemetry.performance")


class PerformanceTracker:
    """
    Tracks and records the execution performance of critical application segments.
    """

    def __init__(self, metrics: MetricsInterface) -> None:
        self._metrics = metrics
        logger.info("PerformanceTracker initialized")

    @contextmanager
    def measure_time(self, operation_name: str) -> Iterator[None]:
        """
        Context manager to measure the time taken by a block of code.
        """
        start_time = time.perf_counter()
        logger.debug("Operation started", operation=operation_name)
        try:
            yield
        finally:
            duration = time.perf_counter() - start_time
            logger.debug(
                "Operation completed", operation=operation_name, duration_s=duration
            )
            self._metrics.record_gauge(f"perf.{operation_name}.duration", duration)
