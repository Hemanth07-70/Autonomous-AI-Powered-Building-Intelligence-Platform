from pathlib import Path
from typing import Dict, List, Optional
from uuid import uuid4

import structlog

from app.orchestrator.decision_models import DecisionGoal, ExecutionPlan
from app.orchestrator.decision_repository import (
    DecisionRepository,
    DuplicateDecisionGoalError,
)
from app.scheduler.simulation_orchestrator import SimulationOrchestrator
from app.shared.enums import GoalType, PlanStatus, SimulationStatus

logger = structlog.get_logger("orchestrator.decision_engine")


RULES: Dict[GoalType, List[str]] = {
    GoalType.ENERGY_REDUCTION: [
        "baseline",
        "reduced_hvac",
        "reduced_lighting",
        "result_comparison",
    ],
    GoalType.PEAK_LOAD: [
        "baseline",
        "peak_load_shift",
        "demand_response",
        "result_comparison",
    ],
    GoalType.THERMAL_COMFORT: [
        "baseline",
        "occupancy_simulation",
        "hvac_adjustment",
        "result_comparison",
    ],
    GoalType.HVAC: [
        "baseline",
        "hvac_variant",
        "ventilation_variant",
        "result_comparison",
    ],
    GoalType.LIGHTING: [
        "baseline",
        "daylighting_variant",
        "reduced_lighting",
        "result_comparison",
    ],
    GoalType.OCCUPANCY: [
        "baseline",
        "occupancy_simulation",
        "schedule_variant",
        "result_comparison",
    ],
    GoalType.CARBON: [
        "baseline",
        "carbon_intensity_variant",
        "reduced_hvac",
        "result_comparison",
    ],
    GoalType.WATER: [
        "baseline",
        "fixture_efficiency_variant",
        "irrigation_variant",
        "result_comparison",
    ],
    GoalType.DIAGNOSTICS: [
        "baseline",
        "equipment_analysis",
        "fault_detection",
    ],
}


class DecisionGoalNotFoundError(Exception):
    pass


class ExecutionPlanNotFoundError(Exception):
    pass


class InvalidDecisionGoalError(Exception):
    pass


class InvalidPlanStateError(Exception):
    pass


class DecisionEngine:
    """
    Deterministic engine that converts building goals into simulation plans.
    """

    def __init__(
        self,
        simulation_orchestrator: SimulationOrchestrator,
        repository: Optional[DecisionRepository] = None,
    ) -> None:
        self._simulation_orchestrator = simulation_orchestrator
        self._repository = repository or DecisionRepository()
        logger.info("DecisionEngine initialized")

    def create_goal(
        self,
        *,
        goal_type: GoalType,
        priority: int,
        building_id: str,
        constraints: Optional[dict] = None,
        parameters: Optional[dict] = None,
        goal_id: Optional[str] = None,
    ) -> DecisionGoal:
        goal = DecisionGoal(
            id=goal_id or str(uuid4()),
            goal_type=goal_type,
            priority=priority,
            building_id=building_id,
            constraints=constraints or {},
            parameters=parameters or {},
        )
        self.validate_goal(goal)
        try:
            saved = self._repository.save_goal(goal)
        except DuplicateDecisionGoalError as exc:
            logger.warning("Duplicate decision goal rejected", goal_id=goal.id)
            raise InvalidDecisionGoalError(str(exc)) from exc

        logger.info(
            "Decision goal created",
            goal_id=saved.id,
            goal_type=saved.goal_type.value,
            building_id=saved.building_id,
            priority=saved.priority,
        )
        return saved

    def validate_goal(self, goal: DecisionGoal) -> DecisionGoal:
        if not goal.building_id.strip():
            raise InvalidDecisionGoalError("building_id is required")
        if goal.goal_type not in RULES:
            raise InvalidDecisionGoalError(
                f"Unsupported goal type: {goal.goal_type.value}"
            )
        if not isinstance(goal.constraints, dict):
            raise InvalidDecisionGoalError("constraints must be a dictionary")
        if not isinstance(goal.parameters, dict):
            raise InvalidDecisionGoalError("parameters must be a dictionary")

        logger.info(
            "Decision goal validated",
            goal_id=goal.id,
            goal_type=goal.goal_type.value,
        )
        return goal

    def build_execution_plan(self, goal_id: str) -> ExecutionPlan:
        goal = self._get_existing_goal(goal_id)
        self.validate_goal(goal)

        scenarios = RULES[goal.goal_type]
        simulation_jobs = []
        for index, scenario in enumerate(scenarios, start=1):
            scenario_name = f"{goal.goal_type.value.lower()}_{index}_{scenario}"
            job = self._simulation_orchestrator.create_job(
                twin_id=goal.building_id,
                scenario_name=scenario_name,
                output_directory=str(
                    Path("simulation_outputs") / goal.id / scenario_name
                ),
            )
            simulation_jobs.append(job.id)

        plan = ExecutionPlan(
            goal_id=goal.id,
            simulation_jobs=simulation_jobs,
            execution_order=list(simulation_jobs),
            status=PlanStatus.READY,
            estimated_runtime=self.estimate_runtime(goal),
        )
        saved = self._repository.save_plan(plan)
        logger.info(
            "Execution plan generated",
            plan_id=saved.id,
            goal_id=goal.id,
            job_count=len(saved.simulation_jobs),
            estimated_runtime=saved.estimated_runtime,
        )
        return saved

    def estimate_runtime(self, goal: DecisionGoal) -> float:
        base_minutes_per_job = float(goal.parameters.get("minutes_per_job", 10.0))
        return len(RULES[goal.goal_type]) * base_minutes_per_job

    def submit_plan(self, plan_id: str) -> ExecutionPlan:
        plan = self._get_existing_plan(plan_id)
        if plan.status not in {PlanStatus.READY, PlanStatus.VALIDATED}:
            raise InvalidPlanStateError(
                f"Cannot submit plan {plan.id} from status {plan.status.value}"
            )

        for job_id in plan.execution_order:
            job = self._simulation_orchestrator.get_job(job_id)
            if job.status == SimulationStatus.PENDING:
                job = self._simulation_orchestrator.queue_job(job_id)
            if job.status == SimulationStatus.QUEUED:
                self._simulation_orchestrator.start_job(job_id)

        updated = plan.model_copy(update={"status": PlanStatus.RUNNING})
        logger.info("Execution plan submitted", plan_id=plan.id)
        return self._repository.update_plan(updated)

    def cancel_plan(self, plan_id: str) -> ExecutionPlan:
        plan = self._get_existing_plan(plan_id)
        for job_id in plan.simulation_jobs:
            self._simulation_orchestrator.cancel_job(job_id)
        updated = plan.model_copy(update={"status": PlanStatus.FAILED})
        logger.info("Execution plan cancelled", plan_id=plan.id)
        return self._repository.update_plan(updated)

    def get_goal(self, goal_id: str) -> DecisionGoal:
        return self._get_existing_goal(goal_id)

    def list_goals(self) -> List[DecisionGoal]:
        return self._repository.list_goals()

    def get_plan(self, plan_id: str) -> ExecutionPlan:
        return self._get_existing_plan(plan_id)

    def list_plans(self) -> List[ExecutionPlan]:
        return self._repository.list_plans()

    def _get_existing_goal(self, goal_id: str) -> DecisionGoal:
        goal = self._repository.find_goal_by_id(goal_id)
        if goal is None:
            raise DecisionGoalNotFoundError(f"Decision goal not found: {goal_id}")
        return goal

    def _get_existing_plan(self, plan_id: str) -> ExecutionPlan:
        plan = self._repository.find_plan_by_id(plan_id)
        if plan is None:
            raise ExecutionPlanNotFoundError(f"Execution plan not found: {plan_id}")
        return plan
