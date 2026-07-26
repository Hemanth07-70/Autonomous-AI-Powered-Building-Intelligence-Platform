from unittest.mock import MagicMock

from app.agents.graph import build_graph
from app.agents.state import AgentState
from app.orchestrator.decision_models import DecisionGoal, ExecutionPlan
from app.shared.enums import GoalType, PlanStatus


def test_agent_graph_execution():
    # Mock AI Planner
    mock_planner = MagicMock()
    mock_goal = DecisionGoal(
        id="goal-123",
        goal_type=GoalType.HVAC,
        building_id="building-a",
        priority=5,
        constraints={},
        parameters={},
    )
    mock_planner.plan.return_value = mock_goal

    # Mock Decision Engine
    mock_engine = MagicMock()
    mock_plan = ExecutionPlan(
        id="plan-123",
        goal_id="goal-123",
        simulation_jobs=["job-1"],
        execution_order=["job-1"],
        status=PlanStatus.CREATED,
        estimated_runtime=120.0,
    )
    mock_engine.generate_plan.return_value = mock_plan

    # Build Graph
    graph = build_graph(mock_planner, mock_engine)

    # Initial State
    initial_state = AgentState(
        user_request="Optimize HVAC for comfort",
        conversation_history=[],
        decision_goal=None,
        execution_plan=None,
        simulation_summary={"energy_used": 100, "comfort_score": 0.8},
        analytics=None,
        diagnostics=None,
        recommendations=None,
        errors=[],
        metadata={},
        timestamps={},
    )

    # Execute Graph
    final_state = graph.invoke(initial_state)

    # Assertions
    assert "decision_goal" in final_state
    assert final_state["decision_goal"]["id"] == "goal-123"
    assert "execution_plan" in final_state
    assert final_state["execution_plan"]["id"] == "plan-123"

    assert "analytics" in final_state
    assert final_state["analytics"]["energy_kpis"]["total_kwh"] == 105.0

    assert "diagnostics" in final_state
    assert len(final_state["diagnostics"]["hvac_inefficiencies"]) > 0

    assert "recommendations" in final_state
    assert len(final_state["recommendations"]) > 0
    assert final_state["recommendations"][0]["title"] == "Optimize HVAC Pre-Cooling"
