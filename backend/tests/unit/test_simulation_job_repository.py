import pytest

from app.scheduler.simulation_job import SimulationJob
from app.scheduler.simulation_job_repository import (
    DuplicateSimulationJobError,
    SimulationJobRepository,
)
from app.shared.enums import SimulationStatus


def make_job(job_id: str = "job-1") -> SimulationJob:
    return SimulationJob(
        id=job_id,
        twin_id="twin-1",
        scenario_name="baseline",
        output_directory=f"simulation_outputs/{job_id}",
    )


def test_repository_save_find_list_update_delete():
    repository = SimulationJobRepository()
    job = repository.save(make_job())

    assert repository.find_by_id(job.id) == job
    assert repository.list() == [job]

    updated = job.model_copy(update={"status": SimulationStatus.QUEUED})
    repository.update(updated)
    assert repository.find_by_id(job.id).status == SimulationStatus.QUEUED

    repository.delete(job.id)
    assert repository.find_by_id(job.id) is None


def test_repository_rejects_duplicate_job():
    repository = SimulationJobRepository()
    repository.save(make_job())

    with pytest.raises(DuplicateSimulationJobError):
        repository.save(make_job())
