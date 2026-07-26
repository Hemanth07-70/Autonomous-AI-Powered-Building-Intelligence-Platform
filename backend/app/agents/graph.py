from typing import Any

from langgraph.graph import END, START, StateGraph

from app.agents.analytics_agent import AnalyticsAgentNode
from app.agents.diagnostics_agent import DiagnosticsAgentNode
from app.agents.planner_agent import PlannerAgentNode
from app.agents.recommendation_agent import RecommendationAgentNode
from app.agents.state import AgentState
from app.ai.planner import AIPlanner


def build_graph(ai_planner: AIPlanner, decision_engine: Any) -> StateGraph:
    """Builds and compiles the Autonomous Building Intelligence graph."""

    workflow = StateGraph(AgentState)

    # Initialize nodes
    planner_node = PlannerAgentNode(
        ai_planner=ai_planner, decision_engine=decision_engine
    )
    analytics_node = AnalyticsAgentNode()
    diagnostics_node = DiagnosticsAgentNode()
    recommendation_node = RecommendationAgentNode()

    # Add nodes to graph
    workflow.add_node("planner", planner_node)
    workflow.add_node("analytics", analytics_node)
    workflow.add_node("diagnostics", diagnostics_node)
    workflow.add_node("recommendation", recommendation_node)

    # Define edges
    workflow.add_edge(START, "planner")

    # After planner, run analytics and diagnostics in parallel
    workflow.add_edge("planner", "analytics")
    workflow.add_edge("planner", "diagnostics")

    # Both must complete before recommendation
    workflow.add_edge("analytics", "recommendation")
    workflow.add_edge("diagnostics", "recommendation")

    workflow.add_edge("recommendation", END)

    return workflow.compile()
