import pytest

from app.orchestrator.decision_models import DecisionGoal, ExecutionPlan
from app.orchestrator.decision_repository import (
    DecisionRepository,
    DuplicateDecisionGoalError,
    DuplicateExecutionPlanError,
)
from app.shared.enums import GoalType


def make_goal(goal_id: str = "goal-1") -> DecisionGoal:
    return DecisionGoal(
        id=goal_id,
        goal_type=GoalType.ENERGY_REDUCTION,
        priority=5,
        building_id="building-1",
    )


def make_plan(plan_id: str = "plan-1") -> ExecutionPlan:
    return ExecutionPlan(
        id=plan_id,
        goal_id="goal-1",
        simulation_jobs=["job-1"],
        execution_order=["job-1"],
    )


def test_repository_stores_goals_and_plans():
    repository = DecisionRepository()
    goal = repository.save_goal(make_goal())
    plan = repository.save_plan(make_plan())

    assert repository.find_goal_by_id(goal.id) == goal
    assert repository.list_goals() == [goal]
    assert repository.find_plan_by_id(plan.id) == plan
    assert repository.list_plans() == [plan]

    updated = plan.model_copy(update={"estimated_runtime": 30.0})
    repository.update_plan(updated)
    assert repository.find_plan_by_id(plan.id).estimated_runtime == 30.0


def test_repository_rejects_duplicate_goals_and_plans():
    repository = DecisionRepository()
    repository.save_goal(make_goal())
    repository.save_plan(make_plan())

    with pytest.raises(DuplicateDecisionGoalError):
        repository.save_goal(make_goal())

    with pytest.raises(DuplicateExecutionPlanError):
        repository.save_plan(make_plan())
