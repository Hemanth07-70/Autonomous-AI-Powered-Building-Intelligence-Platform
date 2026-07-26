import threading
from typing import Dict, List, Optional

from app.orchestrator.decision_models import DecisionGoal, ExecutionPlan


class DuplicateDecisionGoalError(Exception):
    pass


class DuplicateExecutionPlanError(Exception):
    pass


class DecisionRepository:
    """
    Thread-safe in-memory store for goals and generated execution plans.
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._goals: Dict[str, DecisionGoal] = {}
        self._plans: Dict[str, ExecutionPlan] = {}

    def save_goal(self, goal: DecisionGoal) -> DecisionGoal:
        with self._lock:
            if goal.id in self._goals:
                raise DuplicateDecisionGoalError(
                    f"Decision goal already exists: {goal.id}"
                )
            self._goals[goal.id] = goal
            return goal

    def find_goal_by_id(self, goal_id: str) -> Optional[DecisionGoal]:
        with self._lock:
            return self._goals.get(goal_id)

    def list_goals(self) -> List[DecisionGoal]:
        with self._lock:
            return sorted(self._goals.values(), key=lambda goal: goal.created_at)

    def save_plan(self, plan: ExecutionPlan) -> ExecutionPlan:
        with self._lock:
            if plan.id in self._plans:
                raise DuplicateExecutionPlanError(
                    f"Execution plan already exists: {plan.id}"
                )
            self._plans[plan.id] = plan
            return plan

    def update_plan(self, plan: ExecutionPlan) -> ExecutionPlan:
        with self._lock:
            self._plans[plan.id] = plan
            return plan

    def find_plan_by_id(self, plan_id: str) -> Optional[ExecutionPlan]:
        with self._lock:
            return self._plans.get(plan_id)

    def list_plans(self) -> List[ExecutionPlan]:
        with self._lock:
            return sorted(self._plans.values(), key=lambda plan: plan.created_at)
