import asyncio

import pytest

from app.scheduler.simulation_job import job_duration_seconds
from app.scheduler.simulation_orchestrator import (
    InvalidSimulationTransitionError,
    SimulationJobNotFoundError,
    SimulationOrchestrator,
)
from app.shared.enums import SimulationStatus


async def successful_executor(job, cancel_event):
    assert job.status == SimulationStatus.RUNNING
    assert not cancel_event.is_set()


async def failing_executor(job, cancel_event):
    raise RuntimeError("engine failed")


@pytest.mark.asyncio
async def test_job_lifecycle_completes_successfully():
    orchestrator = SimulationOrchestrator(executor=successful_executor)
    job = orchestrator.create_job("twin-1", "baseline")

    assert job.status == SimulationStatus.PENDING
    assert orchestrator.queue_job(job.id).status == SimulationStatus.QUEUED
    assert orchestrator.start_job(job.id).status == SimulationStatus.STARTING

    await orchestrator.run_job(job.id)

    completed = orchestrator.get_job(job.id)
    assert completed.status == SimulationStatus.COMPLETED
    assert completed.progress == 100.0
    assert job_duration_seconds(completed) is not None


@pytest.mark.asyncio
async def test_run_job_tracks_failures():
    orchestrator = SimulationOrchestrator(executor=failing_executor)
    job = orchestrator.create_job("twin-1", "failure-case")
    orchestrator.queue_job(job.id)
    orchestrator.start_job(job.id)

    await orchestrator.run_job(job.id)

    failed = orchestrator.get_job(job.id)
    assert failed.status == SimulationStatus.FAILED
    assert failed.error_message == "engine failed"
    assert failed.completed_at is not None


@pytest.mark.asyncio
async def test_running_job_can_be_cancelled():
    async def waiting_executor(job, cancel_event):
        while not cancel_event.is_set():
            await asyncio.sleep(0.01)

    orchestrator = SimulationOrchestrator(executor=waiting_executor)
    job = orchestrator.create_job("twin-1", "cancel-case")
    orchestrator.queue_job(job.id)
    orchestrator.start_job(job.id)

    task = asyncio.create_task(orchestrator.run_job(job.id))
    while orchestrator.get_job(job.id).status != SimulationStatus.RUNNING:
        await asyncio.sleep(0.01)

    cancelled = orchestrator.cancel_job(job.id)
    await task

    assert cancelled.status == SimulationStatus.CANCELLED
    assert orchestrator.get_job(job.id).completed_at is not None


def test_invalid_transition_is_rejected():
    orchestrator = SimulationOrchestrator(executor=successful_executor)
    job = orchestrator.create_job("twin-1", "baseline")

    with pytest.raises(InvalidSimulationTransitionError):
        orchestrator.start_job(job.id)


def test_missing_job_is_rejected():
    orchestrator = SimulationOrchestrator(executor=successful_executor)

    with pytest.raises(SimulationJobNotFoundError):
        orchestrator.get_job("missing")
