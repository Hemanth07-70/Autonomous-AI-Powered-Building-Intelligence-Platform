from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from app.energyplus.simulation_state import SimulationSnapshot
from app.shared.enums import SimulationStatus


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class SimulationJob(BaseModel):
    """
    Execution metadata for a single simulation run.
    """

    id: str = Field(default_factory=lambda: str(uuid4()))
    twin_id: str
    scenario_name: str
    status: SimulationStatus = SimulationStatus.PENDING
    created_at: datetime = Field(default_factory=utc_now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress: float = Field(default=0.0, ge=0.0, le=100.0)
    simulation_state: Optional[SimulationSnapshot] = None
    error_message: Optional[str] = None
    output_directory: str


class SimulationJobCreate(BaseModel):
    twin_id: str
    scenario_name: str
    output_directory: Optional[str] = None


class SimulationJobRead(BaseModel):
    id: str
    twin_id: str
    scenario_name: str
    status: SimulationStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress: float
    simulation_state: Optional[SimulationSnapshot] = None
    error_message: Optional[str] = None
    output_directory: str
    duration_seconds: Optional[float] = None


def job_duration_seconds(job: SimulationJob) -> Optional[float]:
    if job.started_at is None or job.completed_at is None:
        return None
    return (job.completed_at - job.started_at).total_seconds()


def to_job_read(job: SimulationJob) -> SimulationJobRead:
    return SimulationJobRead(
        **job.model_dump(), duration_seconds=job_duration_seconds(job)
    )
