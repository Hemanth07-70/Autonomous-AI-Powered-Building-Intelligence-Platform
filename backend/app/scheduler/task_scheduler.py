import asyncio
from typing import Awaitable, List

import structlog

logger = structlog.get_logger("scheduler.task_scheduler")


class TaskScheduler:
    """
    Manages the execution of one-off or scheduled background async tasks.
    """

    def __init__(self) -> None:
        self._background_tasks: List[asyncio.Task] = []
        logger.info("TaskScheduler initialized")

    def schedule(self, coroutine: Awaitable[None]) -> None:
        """Schedules a coroutine to run in the background."""
        task = asyncio.create_task(coroutine)
        self._background_tasks.append(task)

        # Optionally, add a done callback to remove it from the list
        task.add_done_callback(self._background_tasks.remove)
        logger.debug("Background task scheduled")

    async def shutdown(self) -> None:
        """Cancels all pending background tasks gracefully."""
        logger.info(
            "TaskScheduler shutting down", pending_tasks=len(self._background_tasks)
        )
        for task in self._background_tasks:
            task.cancel()

        if self._background_tasks:
            await asyncio.gather(*self._background_tasks, return_exceptions=True)
        logger.info("TaskScheduler shutdown complete")
