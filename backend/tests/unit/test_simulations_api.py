import asyncio

from fastapi.testclient import TestClient

from app.main import create_app
from app.scheduler.simulation_orchestrator import SimulationOrchestrator
from app.shared.enums import SimulationStatus


async def successful_executor(job, cancel_event):
    await asyncio.sleep(0)


def make_client() -> TestClient:
    app = create_app()
    app.state.simulation_orchestrator = SimulationOrchestrator(
        executor=successful_executor
    )
    return TestClient(app)


def test_create_list_and_get_simulation_job():
    client = make_client()

    create_response = client.post(
        "/api/simulations",
        json={"twin_id": "twin-1", "scenario_name": "baseline"},
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["status"] == SimulationStatus.PENDING.value

    list_response = client.get("/api/simulations")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    get_response = client.get(f"/api/simulations/{created['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == created["id"]


def test_start_simulation_job_schedules_background_execution():
    client = make_client()
    created = client.post(
        "/api/simulations",
        json={"twin_id": "twin-1", "scenario_name": "baseline"},
    ).json()

    start_response = client.post(f"/api/simulations/{created['id']}/start")
    assert start_response.status_code == 200
    assert start_response.json()["status"] == SimulationStatus.STARTING.value

    details = client.get(f"/api/simulations/{created['id']}").json()
    assert details["status"] in {
        SimulationStatus.STARTING.value,
        SimulationStatus.RUNNING.value,
        SimulationStatus.COMPLETED.value,
    }


def test_cancel_simulation_job():
    client = make_client()
    created = client.post(
        "/api/simulations",
        json={"twin_id": "twin-1", "scenario_name": "baseline"},
    ).json()

    response = client.post(f"/api/simulations/{created['id']}/cancel")
    assert response.status_code == 200
    assert response.json()["status"] == SimulationStatus.CANCELLED.value


def test_missing_simulation_job_returns_404():
    client = make_client()

    response = client.get("/api/simulations/missing")
    assert response.status_code == 404
