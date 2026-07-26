import time
from typing import Any, Dict

import structlog

from app.agents.state import AgentState
from app.ai.planner import AIPlanner

logger = structlog.get_logger("agents.planner")


class PlannerAgentNode:
    """
    Node that delegates to the existing AIPlanner to convert natural language
    into a deterministic DecisionGoal and an ExecutionPlan via the DecisionEngine.
    """

    def __init__(self, ai_planner: AIPlanner, decision_engine: Any):
        self.ai_planner = ai_planner
        self.decision_engine = decision_engine

    def __call__(self, state: AgentState) -> Dict[str, Any]:
        logger.info("Planner Agent starting", user_request=state["user_request"])
        start = time.perf_counter()

        try:
            # Re-use existing AI Planner logic
            goal = self.ai_planner.plan(state["user_request"])

            # The Decision Engine normally generates the plan via a separate API,
            # but we can call it directly here if we inject the decision_engine
            # For simplicity, we just trigger the plan generation
            plan = self.decision_engine.build_execution_plan(goal.id)

            logger.info("Planner Agent completed", latency=time.perf_counter() - start)

            return {
                "decision_goal": goal.model_dump(mode="json"),
                "execution_plan": plan.model_dump(mode="json") if plan else None,
                "timestamps": {"planner_completed": time.time()},
            }
        except Exception as e:
            logger.error("Planner Agent failed", error=str(e))
            return {"errors": [f"PlannerAgent failed: {str(e)}"]}
