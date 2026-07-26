from app.ai.planner import AIPlanner
from app.orchestrator.decision_engine import DecisionEngine
from app.scheduler.simulation_orchestrator import SimulationOrchestrator
from app.shared.enums import GoalType


class MockOllamaClient:
    model = "qwen3"

    def __init__(self):
        self.prompt = None

    def ensure_model_available(self):
        return None

    def chat_completion(self, prompt):
        self.prompt = prompt
        return (
            '{"goal_type":"THERMAL_COMFORT","building_id":"building-a",'
            '"priority":2,"constraints":{"target_pmv":0.5},"parameters":{}}'
        )

    def run_inference(self, prompt):
        return self.chat_completion(prompt)


def test_ai_planner_generates_decision_goal():
    client = MockOllamaClient()
    decision_engine = DecisionEngine(SimulationOrchestrator())
    planner = AIPlanner(client, decision_engine)

    goal = planner.plan("Run thermal comfort analysis")

    assert goal.goal_type == GoalType.THERMAL_COMFORT
    assert goal.building_id == "building-a"
    assert goal.constraints["target_pmv"] == 0.5
    assert "Run thermal comfort analysis" in client.prompt
    assert decision_engine.get_goal(goal.id) == goal


def test_ai_planner_chat_response_contains_goal():
    planner = AIPlanner(MockOllamaClient(), DecisionEngine(SimulationOrchestrator()))

    response, goal = planner.chat("Run thermal comfort analysis")

    assert "Created THERMAL_COMFORT decision goal" in response
    assert goal.goal_type == GoalType.THERMAL_COMFORT
