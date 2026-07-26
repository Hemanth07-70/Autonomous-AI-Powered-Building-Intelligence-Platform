from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import uuid4

from pydantic import BaseModel, Field

from app.shared.enums import GoalType, PlanStatus


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class DecisionGoal(BaseModel):
    """
    Deterministic building objective submitted to the Decision Engine.
    """

    id: str = Field(default_factory=lambda: str(uuid4()))
    goal_type: GoalType
    priority: int = Field(default=5, ge=1, le=10)
    building_id: str = Field(..., min_length=1)
    constraints: Dict[str, Any] = Field(default_factory=dict)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)


class DecisionGoalCreate(BaseModel):
    goal_type: GoalType
    priority: int = Field(default=5, ge=1, le=10)
    building_id: str = Field(..., min_length=1)
    constraints: Dict[str, Any] = Field(default_factory=dict)
    parameters: Dict[str, Any] = Field(default_factory=dict)


class ExecutionPlan(BaseModel):
    """
    Ordered simulation plan generated from a validated decision goal.
    """

    id: str = Field(default_factory=lambda: str(uuid4()))
    goal_id: str
    simulation_jobs: List[str] = Field(default_factory=list)
    execution_order: List[str] = Field(default_factory=list)
    status: PlanStatus = PlanStatus.CREATED
    estimated_runtime: float = Field(default=0.0, ge=0.0)
    created_at: datetime = Field(default_factory=utc_now)
