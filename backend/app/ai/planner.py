import time
from typing import Optional, Any

import structlog

from app.ai.parser import parse_decision_goal
from app.ai.prompts import build_prompt
from app.orchestrator.decision_engine import DecisionEngine
from app.orchestrator.decision_models import DecisionGoal

logger = structlog.get_logger("ai.planner")


class AIPlanner:
    """
    Converts natural language requests into deterministic DecisionGoals.
    """

    def __init__(
        self,
        client: Any,
        decision_engine: DecisionEngine,
        default_building_id: str = "building-a",
    ) -> None:
        self._client = client
        self._decision_engine = decision_engine
        self._default_building_id = default_building_id

    def plan(self, message: str, building_id: Optional[str] = None) -> DecisionGoal:
        start = time.perf_counter()
        default_building_id = building_id or self._default_building_id
        prompt = build_prompt(message, default_building_id)
        logger.info(
            "AI planner received request",
            message_length=len(message),
            model=self._client.model,
            building_id=default_building_id,
        )
        self._client.ensure_model_available()
        raw_response = self._client.chat_completion(prompt)
        parsed_goal = parse_decision_goal(raw_response)
        goal = self._decision_engine.create_goal(
            goal_type=parsed_goal.goal_type,
            priority=parsed_goal.priority,
            building_id=parsed_goal.building_id,
            constraints=parsed_goal.constraints,
            parameters=parsed_goal.parameters,
        )
        logger.info(
            "AI planner generated DecisionGoal",
            goal_id=goal.id,
            goal_type=goal.goal_type.value,
            latency=time.perf_counter() - start,
        )
        return goal

    def chat(
        self, message: str, building_id: Optional[str] = None
    ) -> tuple[str, DecisionGoal]:
        goal = self.plan(message, building_id=building_id)
        response = (
            f"Created {goal.goal_type.value} decision goal for "
            f"building {goal.building_id}."
        )
        return response, goal
