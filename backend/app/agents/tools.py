from typing import Any, Dict


def format_decision_goal(goal: Dict[str, Any]) -> str:
    """Format DecisionGoal dict into a string for LLM context."""
    return f"Goal Type: {goal.get('goal_type')}\nConstraints: {goal.get('constraints')}\nBuilding ID: {goal.get('building_id')}"


def format_execution_plan(plan: Dict[str, Any]) -> str:
    """Format ExecutionPlan dict into a string for LLM context."""
    return f"Execution Plan ID: {plan.get('id')}\nJobs: {plan.get('simulation_jobs')}\nEstimated Runtime: {plan.get('estimated_runtime')}"


def format_simulation_summary(summary: Dict[str, Any]) -> str:
    """Format SimulationSummary dict into a string for LLM context."""
    return (
        f"Simulation Status: {summary.get('status')}\nOutputs: {summary.get('outputs')}"
    )
