import asyncio
from typing import Awaitable, Callable

import structlog

logger = structlog.get_logger("scheduler.polling")


class PollingService:
    """
    Generic service to poll external systems or databases at a defined interval.
    """

    def __init__(
        self, callback: Callable[[], Awaitable[None]], interval_seconds: float
    ):
        self._callback = callback
        self._interval = interval_seconds
        self._is_polling = False
        logger.info("PollingService initialized", interval=interval_seconds)

    async def start_polling(self) -> None:
        """Starts the background polling task."""
        self._is_polling = True
        logger.info("Polling started")

        while self._is_polling:
            try:
                await self._callback()
            except Exception as e:
                logger.error("Polling callback failed", error=str(e), exc_info=True)

            await asyncio.sleep(self._interval)

    def stop_polling(self) -> None:
        """Halts the polling task."""
        logger.info("Polling stop requested")
        self._is_polling = False
