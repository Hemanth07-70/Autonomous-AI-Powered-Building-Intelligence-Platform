import pytest

from app.orchestrator.decision_engine import (
    RULES,
    DecisionEngine,
    DecisionGoalNotFoundError,
    InvalidDecisionGoalError,
)
from app.scheduler.simulation_orchestrator import SimulationOrchestrator
from app.shared.enums import GoalType, PlanStatus, SimulationStatus


@pytest.fixture
def decision_engine():
    return DecisionEngine(SimulationOrchestrator())


def test_goal_creation_and_validation(decision_engine):
    goal = decision_engine.create_goal(
        goal_type=GoalType.ENERGY_REDUCTION,
        priority=3,
        building_id="building-1",
        constraints={"max_runtime": 120},
        parameters={"minutes_per_job": 5},
    )

    assert goal.goal_type == GoalType.ENERGY_REDUCTION
    assert decision_engine.get_goal(goal.id) == goal
    assert decision_engine.list_goals() == [goal]


def test_invalid_goal_rejected(decision_engine):
    with pytest.raises(InvalidDecisionGoalError):
        decision_engine.create_goal(
            goal_type=GoalType.HVAC,
            priority=5,
            building_id=" ",
        )


def test_energy_reduction_plan_generation_creates_ordered_jobs(decision_engine):
    goal = decision_engine.create_goal(
        goal_type=GoalType.ENERGY_REDUCTION,
        priority=1,
        building_id="building-1",
        parameters={"minutes_per_job": 2},
    )

    plan = decision_engine.build_execution_plan(goal.id)

    assert plan.status == PlanStatus.READY
    assert plan.execution_order == plan.simulation_jobs
    assert len(plan.simulation_jobs) == len(RULES[GoalType.ENERGY_REDUCTION])
    assert plan.estimated_runtime == 8.0

    jobs = [
        decision_engine._simulation_orchestrator.get_job(job_id)
        for job_id in plan.execution_order
    ]
    assert [job.status for job in jobs] == [SimulationStatus.PENDING] * 4
    assert jobs[0].scenario_name.endswith("baseline")
    assert jobs[1].scenario_name.endswith("reduced_hvac")
    assert jobs[2].scenario_name.endswith("reduced_lighting")
    assert jobs[3].scenario_name.endswith("result_comparison")


def test_diagnostics_rule_engine(decision_engine):
    goal = decision_engine.create_goal(
        goal_type=GoalType.DIAGNOSTICS,
        priority=5,
        building_id="building-1",
    )

    plan = decision_engine.build_execution_plan(goal.id)
    jobs = [
        decision_engine._simulation_orchestrator.get_job(job_id)
        for job_id in plan.execution_order
    ]

    assert len(jobs) == 3
    assert jobs[1].scenario_name.endswith("equipment_analysis")
    assert jobs[2].scenario_name.endswith("fault_detection")


def test_missing_goal_rejected(decision_engine):
    with pytest.raises(DecisionGoalNotFoundError):
        decision_engine.build_execution_plan("missing")


def test_submit_plan_marks_jobs_starting(decision_engine):
    goal = decision_engine.create_goal(
        goal_type=GoalType.THERMAL_COMFORT,
        priority=4,
        building_id="building-1",
    )
    plan = decision_engine.build_execution_plan(goal.id)

    submitted = decision_engine.submit_plan(plan.id)

    assert submitted.status == PlanStatus.RUNNING
    for job_id in submitted.execution_order:
        assert (
            decision_engine._simulation_orchestrator.get_job(job_id).status
            == SimulationStatus.STARTING
        )
