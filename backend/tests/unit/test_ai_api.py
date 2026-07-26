from fastapi.testclient import TestClient

from app.ai.exceptions import InvalidAIResponse
from app.main import create_app
from app.orchestrator.decision_engine import DecisionEngine
from app.scheduler.simulation_orchestrator import SimulationOrchestrator
from app.shared.enums import GoalType


class MockOllamaClient:
    model = "qwen3"

    def health_check(self):
        return True

    def list_models(self):
        return ["qwen3:latest"]


class MockAIPlanner:
    def __init__(self, decision_engine):
        self._decision_engine = decision_engine

    def plan(self, message, building_id=None):
        return self._decision_engine.create_goal(
            goal_type=GoalType.ENERGY_REDUCTION,
            priority=1,
            building_id=building_id or "building-a",
            constraints={"target_reduction": 10},
            parameters={},
        )

    def chat(self, message, building_id=None):
        goal = self.plan(message, building_id=building_id)
        return "Created ENERGY_REDUCTION decision goal for building building-a.", goal


def make_client() -> TestClient:
    app = create_app()
    app.state.simulation_orchestrator = SimulationOrchestrator()
    app.state.decision_engine = DecisionEngine(app.state.simulation_orchestrator)
    app.state.ollama_client = MockOllamaClient()
    app.state.ai_planner = MockAIPlanner(app.state.decision_engine)
    return TestClient(app)


def test_ai_chat_endpoint():
    client = make_client()

    response = client.post(
        "/api/ai/chat",
        json={"message": "Reduce HVAC energy by 10%"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["response"].startswith("Created ENERGY_REDUCTION")
    assert payload["decision_goal"]["goal_type"] == GoalType.ENERGY_REDUCTION.value


def test_ai_plan_endpoint():
    client = make_client()

    response = client.post(
        "/api/ai/plan",
        json={"message": "Reduce HVAC energy by 10%"},
    )

    assert response.status_code == 200
    assert response.json()["constraints"]["target_reduction"] == 10


def test_ai_models_endpoint():
    client = make_client()

    response = client.get("/api/ai/models")

    assert response.status_code == 200
    assert response.json() == {
        "models": ["qwen3:latest"],
        "selected_model": "qwen3",
    }


def test_ai_health_endpoint():
    client = make_client()

    response = client.get("/api/ai/health")

    assert response.status_code == 200
    assert response.json() == {"available": True, "model": "qwen3"}


class FailingAIPlanner:
    def plan(self, message, building_id=None):
        raise InvalidAIResponse("AI response was not valid JSON")

    def chat(self, message, building_id=None):
        raise InvalidAIResponse("AI response was not valid JSON")


def test_ai_plan_endpoint_returns_bad_request_on_invalid_response():
    app = create_app()
    app.state.simulation_orchestrator = SimulationOrchestrator()
    app.state.decision_engine = DecisionEngine(app.state.simulation_orchestrator)
    app.state.ollama_client = MockOllamaClient()
    app.state.ai_planner = FailingAIPlanner()
    client = TestClient(app)

    response = client.post(
        "/api/ai/plan",
        json={"message": "Reduce HVAC energy by 10%"},
    )

    assert response.status_code == 400
    assert "AI response was not valid JSON" in response.json()["error"]["message"]
