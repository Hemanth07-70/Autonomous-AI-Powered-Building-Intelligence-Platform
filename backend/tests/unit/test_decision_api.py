from fastapi.testclient import TestClient

from app.main import create_app
from app.orchestrator.decision_engine import DecisionEngine
from app.scheduler.simulation_orchestrator import SimulationOrchestrator
from app.shared.enums import GoalType, PlanStatus


def make_client() -> TestClient:
    app = create_app()
    app.state.simulation_orchestrator = SimulationOrchestrator()
    app.state.decision_engine = DecisionEngine(app.state.simulation_orchestrator)
    return TestClient(app)


def test_create_list_get_goal_and_generate_plan():
    client = make_client()

    create_response = client.post(
        "/api/decision/goals",
        json={
            "goal_type": GoalType.ENERGY_REDUCTION.value,
            "priority": 2,
            "building_id": "building-1",
            "parameters": {"minutes_per_job": 3},
        },
    )

    assert create_response.status_code == 201
    goal = create_response.json()
    assert goal["goal_type"] == GoalType.ENERGY_REDUCTION.value

    list_response = client.get("/api/decision/goals")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    get_response = client.get(f"/api/decision/goals/{goal['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == goal["id"]

    plan_response = client.post(f"/api/decision/goals/{goal['id']}/plan")
    assert plan_response.status_code == 200
    plan = plan_response.json()
    assert plan["status"] == PlanStatus.READY.value
    assert len(plan["execution_order"]) == 4

    get_plan_response = client.get(f"/api/decision/plans/{plan['id']}")
    assert get_plan_response.status_code == 200
    assert get_plan_response.json()["id"] == plan["id"]


def test_missing_goal_and_plan_return_404():
    client = make_client()

    assert client.get("/api/decision/goals/missing").status_code == 404
    assert client.post("/api/decision/goals/missing/plan").status_code == 404
    assert client.get("/api/decision/plans/missing").status_code == 404


def test_invalid_goal_payload_returns_422():
    client = make_client()

    response = client.post(
        "/api/decision/goals",
        json={
            "goal_type": GoalType.HVAC.value,
            "priority": 0,
            "building_id": "building-1",
        },
    )

    assert response.status_code == 422
