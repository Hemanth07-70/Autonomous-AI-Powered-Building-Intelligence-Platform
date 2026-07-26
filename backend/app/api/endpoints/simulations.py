from typing import List

from fastapi import APIRouter, Request, status

from app.core.exceptions import BadRequestException, NotFoundException
from app.scheduler.simulation_job import (
    SimulationJobCreate,
    SimulationJobRead,
    to_job_read,
)
from app.scheduler.simulation_orchestrator import (
    InvalidSimulationTransitionError,
    SimulationJobNotFoundError,
    SimulationOrchestrator,
)
from app.shared.enums import SimulationStatus

router = APIRouter(prefix="/api/simulations")


def get_orchestrator(request: Request) -> SimulationOrchestrator:
    return request.app.state.simulation_orchestrator


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=SimulationJobRead,
    summary="Create Simulation Job",
)
async def create_simulation_job(
    payload: SimulationJobCreate, request: Request
) -> SimulationJobRead:
    orchestrator = get_orchestrator(request)
    job = orchestrator.create_job(
        twin_id=payload.twin_id,
        scenario_name=payload.scenario_name,
        output_directory=payload.output_directory,
    )
    return to_job_read(job)


@router.get(
    "",
    response_model=List[SimulationJobRead],
    summary="List Simulation Jobs",
)
async def list_simulation_jobs(request: Request) -> List[SimulationJobRead]:
    orchestrator = get_orchestrator(request)
    return [to_job_read(job) for job in orchestrator.list_jobs()]


@router.get(
    "/{job_id}",
    response_model=SimulationJobRead,
    summary="Get Simulation Job",
)
async def get_simulation_job(job_id: str, request: Request) -> SimulationJobRead:
    orchestrator = get_orchestrator(request)
    try:
        return to_job_read(orchestrator.get_job(job_id))
    except SimulationJobNotFoundError as exc:
        raise NotFoundException(str(exc)) from exc


@router.post(
    "/{job_id}/start",
    response_model=SimulationJobRead,
    summary="Start Simulation Job",
)
async def start_simulation_job(job_id: str, request: Request) -> SimulationJobRead:
    orchestrator = get_orchestrator(request)
    scheduler = request.app.state.task_scheduler
    try:
        job = orchestrator.get_job(job_id)
        if job.status == SimulationStatus.PENDING:
            job = orchestrator.queue_job(job_id)
        if job.status == SimulationStatus.QUEUED:
            job = orchestrator.start_job(job_id)
        else:
            raise InvalidSimulationTransitionError(
                f"Cannot start job {job.id} from status {job.status.value}"
            )
        scheduler.schedule(orchestrator.run_job(job_id))
        return to_job_read(job)
    except SimulationJobNotFoundError as exc:
        raise NotFoundException(str(exc)) from exc
    except InvalidSimulationTransitionError as exc:
        raise BadRequestException(str(exc)) from exc


@router.post(
    "/{job_id}/cancel",
    response_model=SimulationJobRead,
    summary="Cancel Simulation Job",
)
async def cancel_simulation_job(job_id: str, request: Request) -> SimulationJobRead:
    orchestrator = get_orchestrator(request)
    try:
        return to_job_read(orchestrator.cancel_job(job_id))
    except SimulationJobNotFoundError as exc:
        raise NotFoundException(str(exc)) from exc
    except InvalidSimulationTransitionError as exc:
        raise BadRequestException(str(exc)) from exc
