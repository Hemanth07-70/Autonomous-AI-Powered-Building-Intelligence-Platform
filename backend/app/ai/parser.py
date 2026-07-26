import json
from typing import Any

import structlog
from pydantic import ValidationError

from app.ai.exceptions import InvalidAIResponse, UnsupportedGoalError
from app.orchestrator.decision_models import DecisionGoalCreate
from app.shared.enums import GoalType

logger = structlog.get_logger("ai.parser")


def parse_decision_goal(raw_response: str) -> DecisionGoalCreate:
    try:
        payload = json.loads(_extract_json(raw_response))
    except json.JSONDecodeError as exc:
        logger.warning("AI parser rejected malformed JSON", error=str(exc))
        raise InvalidAIResponse("AI response was not valid JSON") from exc

    if not isinstance(payload, dict):
        raise InvalidAIResponse("AI response JSON must be an object")

    _validate_goal_type(payload.get("goal_type"))
    try:
        parsed = DecisionGoalCreate.model_validate(payload)
    except ValidationError as exc:
        logger.warning("AI parser rejected invalid schema", errors=exc.errors())
        raise InvalidAIResponse(
            "AI response did not match DecisionGoal schema"
        ) from exc

    logger.info(
        "AI parser produced DecisionGoal",
        goal_type=parsed.goal_type.value,
        building_id=parsed.building_id,
    )
    return parsed


def _validate_goal_type(goal_type: Any) -> None:
    try:
        GoalType(goal_type)
    except ValueError as exc:
        raise UnsupportedGoalError(f"Unsupported goal type: {goal_type}") from exc


def _extract_json(raw_response: str) -> str:
    stripped = raw_response.strip()
    if stripped.startswith("{") and stripped.endswith("}"):
        return stripped

    start = stripped.find("{")
    end = stripped.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return stripped
    return stripped[start : end + 1]
