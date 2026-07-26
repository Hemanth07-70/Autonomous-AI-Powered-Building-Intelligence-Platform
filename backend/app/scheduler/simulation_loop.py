import asyncio
from typing import Awaitable, Callable

import structlog

logger = structlog.get_logger("scheduler.simulation_loop")


class SimulationLoop:
    """
    Manages the continuous execution of the physics simulation steps.
    """

    def __init__(
        self, step_function: Callable[[], Awaitable[None]], interval_seconds: float
    ):
        self._step_function = step_function
        self._interval = interval_seconds
        self._is_running = False
        logger.info("SimulationLoop initialized", interval=interval_seconds)

    async def start(self) -> None:
        """Starts the infinite tick loop."""
        if self._is_running:
            return

        self._is_running = True
        logger.info("SimulationLoop started")

        while self._is_running:
            try:
                await self._step_function()
            except Exception as e:
                logger.error(
                    "Error during simulation tick", error=str(e), exc_info=True
                )

            await asyncio.sleep(self._interval)

    def stop(self) -> None:
        """Stops the loop on the next iteration."""
        logger.info("SimulationLoop stop requested")
        self._is_running = False
