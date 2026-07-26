from typing import List

from fastapi import APIRouter, Request, status

from app.core.exceptions import BadRequestException, NotFoundException
from app.orchestrator.decision_engine import (
    DecisionEngine,
    DecisionGoalNotFoundError,
    ExecutionPlanNotFoundError,
    InvalidDecisionGoalError,
    InvalidPlanStateError,
)
from app.orchestrator.decision_models import (
    DecisionGoal,
    DecisionGoalCreate,
    ExecutionPlan,
)

router = APIRouter(prefix="/api/decision")


def get_decision_engine(request: Request) -> DecisionEngine:
    return request.app.state.decision_engine


@router.post(
    "/goals",
    status_code=status.HTTP_201_CREATED,
    response_model=DecisionGoal,
    summary="Create Decision Goal",
)
async def create_goal(payload: DecisionGoalCreate, request: Request) -> DecisionGoal:
    decision_engine = get_decision_engine(request)
    try:
        return decision_engine.create_goal(
            goal_type=payload.goal_type,
            priority=payload.priority,
            building_id=payload.building_id,
            constraints=payload.constraints,
            parameters=payload.parameters,
        )
    except InvalidDecisionGoalError as exc:
        raise BadRequestException(str(exc)) from exc


@router.get(
    "/goals",
    response_model=List[DecisionGoal],
    summary="List Decision Goals",
)
async def list_goals(request: Request) -> List[DecisionGoal]:
    decision_engine = get_decision_engine(request)
    return decision_engine.list_goals()


@router.get(
    "/goals/{goal_id}",
    response_model=DecisionGoal,
    summary="Get Decision Goal",
)
async def get_goal(goal_id: str, request: Request) -> DecisionGoal:
    decision_engine = get_decision_engine(request)
    try:
        return decision_engine.get_goal(goal_id)
    except DecisionGoalNotFoundError as exc:
        raise NotFoundException(str(exc)) from exc


@router.post(
    "/goals/{goal_id}/plan",
    response_model=ExecutionPlan,
    summary="Generate Execution Plan",
)
async def generate_plan(goal_id: str, request: Request) -> ExecutionPlan:
    decision_engine = get_decision_engine(request)
    try:
        return decision_engine.build_execution_plan(goal_id)
    except DecisionGoalNotFoundError as exc:
        raise NotFoundException(str(exc)) from exc
    except InvalidDecisionGoalError as exc:
        raise BadRequestException(str(exc)) from exc


@router.get(
    "/plans/{plan_id}",
    response_model=ExecutionPlan,
    summary="Get Execution Plan",
)
async def get_plan(plan_id: str, request: Request) -> ExecutionPlan:
    decision_engine = get_decision_engine(request)
    try:
        return decision_engine.get_plan(plan_id)
    except ExecutionPlanNotFoundError as exc:
        raise NotFoundException(str(exc)) from exc
    except InvalidPlanStateError as exc:
        raise BadRequestException(str(exc)) from exc
