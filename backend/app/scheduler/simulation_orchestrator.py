import asyncio
import threading
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Dict, List, Optional
from uuid import uuid4

import structlog

from app.energyplus.digital_twin import DigitalTwinManager
from app.energyplus.energyplus_adapter import EnergyPlusAdapter
from app.energyplus.repository import SimulationRepository
from app.energyplus.simulation_controller import SimulationController
from app.scheduler.simulation_job import SimulationJob, job_duration_seconds, utc_now
from app.scheduler.simulation_job_repository import (
    DuplicateSimulationJobError,
    SimulationJobRepository,
)
from app.shared.enums import SimulationStatus

logger = structlog.get_logger("scheduler.simulation_orchestrator")

ControllerFactory = Callable[[], SimulationController]
JobExecutor = Callable[[SimulationJob, threading.Event], Awaitable[None]]

TERMINAL_STATUSES = {
    SimulationStatus.COMPLETED,
    SimulationStatus.FAILED,
    SimulationStatus.CANCELLED,
}

VALID_TRANSITIONS = {
    SimulationStatus.PENDING: {
        SimulationStatus.QUEUED,
        SimulationStatus.CANCELLED,
    },
    SimulationStatus.QUEUED: {
        SimulationStatus.STARTING,
        SimulationStatus.CANCELLED,
    },
    SimulationStatus.STARTING: {
        SimulationStatus.RUNNING,
        SimulationStatus.FAILED,
        SimulationStatus.CANCELLED,
    },
    SimulationStatus.RUNNING: {
        SimulationStatus.COMPLETED,
        SimulationStatus.FAILED,
        SimulationStatus.CANCELLED,
    },
}


class SimulationJobNotFoundError(Exception):
    pass


class InvalidSimulationTransitionError(Exception):
    pass


class SimulationOrchestrator:
    """
    Single authority for simulation job execution and lifecycle tracking.
    """

    def __init__(
        self,
        repository: Optional[SimulationJobRepository] = None,
        controller_factory: Optional[ControllerFactory] = None,
        executor: Optional[JobExecutor] = None,
    ) -> None:
        self._repository = repository or SimulationJobRepository()
        self._controller_factory = controller_factory or self._default_controller
        self._executor = executor or self._execute_with_controller
        self._cancel_events: Dict[str, threading.Event] = {}
        self._active_controllers: Dict[str, SimulationController] = {}
        logger.info("SimulationOrchestrator initialized")

    def create_job(
        self,
        twin_id: str,
        scenario_name: str,
        output_directory: Optional[str] = None,
        job_id: Optional[str] = None,
    ) -> SimulationJob:
        resolved_job_id = job_id or str(uuid4())
        job = SimulationJob(
            id=resolved_job_id,
            twin_id=twin_id,
            scenario_name=scenario_name,
            output_directory=output_directory
            or self._default_output_directory(resolved_job_id),
        )
        try:
            self._repository.save(job)
        except DuplicateSimulationJobError as exc:
            logger.warning("Duplicate simulation job rejected", job_id=job.id)
            raise InvalidSimulationTransitionError(str(exc)) from exc

        self._cancel_events[job.id] = threading.Event()
        logger.info(
            "Simulation job created",
            job_id=job.id,
            twin_id=twin_id,
            scenario_name=scenario_name,
        )
        return job

    def queue_job(self, job_id: str) -> SimulationJob:
        job = self._get_existing_job(job_id)
        job = self._transition(job, SimulationStatus.QUEUED, progress=5.0)
        logger.info("Simulation job queued", job_id=job.id)
        return job

    def start_job(self, job_id: str) -> SimulationJob:
        job = self._get_existing_job(job_id)
        job = self._transition(job, SimulationStatus.STARTING, progress=10.0)
        logger.info("Simulation job starting", job_id=job.id)
        return job

    def cancel_job(self, job_id: str) -> SimulationJob:
        job = self._get_existing_job(job_id)
        if job.status in TERMINAL_STATUSES:
            return job

        self._cancel_events.setdefault(job.id, threading.Event()).set()
        controller = self._active_controllers.get(job.id)
        if controller is not None:
            try:
                controller.stop_simulation()
            except Exception as exc:
                logger.warning(
                    "Simulation controller stop failed during cancellation",
                    job_id=job.id,
                    error=str(exc),
                )

        job = self._transition(
            job,
            SimulationStatus.CANCELLED,
            completed_at=utc_now(),
            error_message="Simulation job was cancelled.",
        )
        logger.info("Simulation job cancelled", job_id=job.id)
        return job

    def get_job(self, job_id: str) -> SimulationJob:
        return self._get_existing_job(job_id)

    def list_jobs(self) -> List[SimulationJob]:
        return self._repository.list()

    async def run_job(self, job_id: str) -> None:
        job = self._get_existing_job(job_id)
        if job.status == SimulationStatus.CANCELLED:
            return
        if job.status != SimulationStatus.STARTING:
            raise InvalidSimulationTransitionError(
                f"Cannot run job {job.id} from status {job.status.value}"
            )

        cancel_event = self._cancel_events.setdefault(job.id, threading.Event())
        job = self._transition(
            job,
            SimulationStatus.RUNNING,
            started_at=utc_now(),
            progress=25.0,
        )
        logger.info("Simulation job running", job_id=job.id)

        try:
            await self._executor(job, cancel_event)
            latest_job = self._get_existing_job(job.id)
            if latest_job.status == SimulationStatus.CANCELLED:
                return
            self._transition(
                latest_job,
                SimulationStatus.COMPLETED,
                completed_at=utc_now(),
                progress=100.0,
            )
            completed_job = self._get_existing_job(job.id)
            logger.info(
                "Simulation job completed",
                job_id=job.id,
                duration=job_duration_seconds(completed_job),
                output_directory=completed_job.output_directory,
            )
        except asyncio.CancelledError:
            self.cancel_job(job.id)
            raise
        except Exception as exc:
            failed_job = self._get_existing_job(job.id)
            self._transition(
                failed_job,
                SimulationStatus.FAILED,
                completed_at=utc_now(),
                error_message=str(exc),
            )
            logger.error(
                "Simulation job failed",
                job_id=job.id,
                error=str(exc),
                exc_info=True,
            )
        finally:
            self.cleanup_job(job.id)

    def cleanup_job(self, job_id: str) -> None:
        self._active_controllers.pop(job_id, None)
        logger.debug("Simulation job cleanup complete", job_id=job_id)

    def _transition(
        self,
        job: SimulationJob,
        new_status: SimulationStatus,
        *,
        started_at=None,
        completed_at=None,
        progress: Optional[float] = None,
        error_message: Optional[str] = None,
        simulation_state=None,
    ) -> SimulationJob:
        allowed = VALID_TRANSITIONS.get(job.status, set())
        if new_status not in allowed:
            raise InvalidSimulationTransitionError(
                f"Invalid simulation transition: {job.status.value} -> "
                f"{new_status.value}"
            )

        updated = job.model_copy(
            update={
                "status": new_status,
                "started_at": started_at or job.started_at,
                "completed_at": completed_at or job.completed_at,
                "progress": progress if progress is not None else job.progress,
                "error_message": error_message,
                "simulation_state": simulation_state or job.simulation_state,
            }
        )
        return self._repository.update(updated)

    def _get_existing_job(self, job_id: str) -> SimulationJob:
        job = self._repository.find_by_id(job_id)
        if job is None:
            raise SimulationJobNotFoundError(f"Simulation job not found: {job_id}")
        return job

    def _default_output_directory(self, job_id: str) -> str:
        return str(Path("simulation_outputs") / job_id)

    def _default_controller(self) -> SimulationController:
        repository = SimulationRepository()
        twin_manager = DigitalTwinManager(repository)
        adapter = EnergyPlusAdapter()
        return SimulationController(adapter, twin_manager)

    async def _execute_with_controller(
        self, job: SimulationJob, cancel_event: threading.Event
    ) -> None:
        controller = self._controller_factory()
        self._active_controllers[job.id] = controller
        await asyncio.to_thread(controller.start_simulation)

        if cancel_event.is_set():
            return

        snapshot = controller.get_snapshot()
        current_job = self._get_existing_job(job.id)
        self._repository.update(
            current_job.model_copy(
                update={
                    "progress": 90.0,
                    "simulation_state": snapshot,
                }
            )
        )

        await asyncio.to_thread(controller.stop_simulation)
