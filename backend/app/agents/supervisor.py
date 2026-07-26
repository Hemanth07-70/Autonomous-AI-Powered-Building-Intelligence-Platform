from typing import Literal

import structlog

from app.agents.state import AgentState

logger = structlog.get_logger("agents.supervisor")


def supervisor_node(state: AgentState) -> Literal["planner", "end"]:
    """
    Initial entrypoint routing.
    If no goal exists, route to planner.
    """
    logger.info("Supervisor evaluating state")

    if not state.get("decision_goal"):
        return "planner"
    return "end"


def planner_router(state: AgentState) -> Literal["analytics", "diagnostics", "end"]:
    """
    After planner, we could route to analytics and diagnostics.
    With LangGraph we just continue edges, but conditional routing can be used here.
    """
    if state.get("errors"):
        return "end"
    # Actually, in a parallel graph, returning multiple edges or a fixed next node is better.
    # In graph.py we'll define a parallel branch.
    pass
