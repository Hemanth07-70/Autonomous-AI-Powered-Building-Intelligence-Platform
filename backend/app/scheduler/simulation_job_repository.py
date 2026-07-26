import threading
from typing import Dict, List, Optional

from app.scheduler.simulation_job import SimulationJob


class DuplicateSimulationJobError(Exception):
    pass


class SimulationJobRepository:
    """
    Thread-safe in-memory repository for simulation execution metadata.
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._jobs: Dict[str, SimulationJob] = {}

    def save(self, job: SimulationJob) -> SimulationJob:
        with self._lock:
            if job.id in self._jobs:
                raise DuplicateSimulationJobError(
                    f"Simulation job already exists: {job.id}"
                )
            self._jobs[job.id] = job
            return job

    def update(self, job: SimulationJob) -> SimulationJob:
        with self._lock:
            self._jobs[job.id] = job
            return job

    def delete(self, job_id: str) -> None:
        with self._lock:
            self._jobs.pop(job_id, None)

    def find_by_id(self, job_id: str) -> Optional[SimulationJob]:
        with self._lock:
            return self._jobs.get(job_id)

    def list(self) -> List[SimulationJob]:
        with self._lock:
            return sorted(self._jobs.values(), key=lambda job: job.created_at)
