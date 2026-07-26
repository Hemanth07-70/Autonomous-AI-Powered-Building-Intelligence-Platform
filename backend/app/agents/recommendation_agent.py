import time
from typing import Any, Dict

import structlog

from app.agents.state import AgentState

logger = structlog.get_logger("agents.recommendation")


class RecommendationAgentNode:
    """
    Terminal node that synthesizes data into actionable recommendations.
    """

    def __call__(self, state: AgentState) -> Dict[str, Any]:
        logger.info("Recommendation Agent starting")
        start = time.perf_counter()

        # Normally this would be passed to an LLM, but for this mock setup
        # we will generate deterministic recommendations based on diagnostics.
        diagnostics = state.get("diagnostics") or {}
        plan = state.get("execution_plan")

        recommendations = []
        if plan and diagnostics.get("status") == "Pending Analytics":
            recommendations.append(
                {
                    "title": "Execute Simulation Plan",
                    "description": f"Execute the {len(plan.get('simulation_jobs', []))} queued simulation jobs.",
                    "priority": 10,
                    "expected_impact": "Generates data required for recommendations.",
                    "confidence": 1.0,
                }
            )
            logger.info("Recommendation Agent completed", latency=time.perf_counter() - start)
            return {
                "recommendations": recommendations,
                "timestamps": {"recommendation_completed": time.time()},
            }
        if diagnostics.get("hvac_inefficiencies"):
            recommendations.append(
                {
                    "title": "Optimize HVAC Pre-Cooling",
                    "description": "Shift pre-cooling schedule to off-peak hours.",
                    "priority": 8,
                    "expected_impact": "12% reduction in peak demand cost.",
                    "confidence": 0.85,
                }
            )

        if diagnostics.get("occupancy_anomalies"):
            recommendations.append(
                {
                    "title": "Adjust Unoccupied Conditioning",
                    "description": "Increase deadband for Zone 2 and Zone 3 during 1 AM - 5 AM.",
                    "priority": 9,
                    "expected_impact": "5% overall energy reduction.",
                    "confidence": 0.95,
                }
            )

        if not recommendations:
            recommendations.append(
                {
                    "title": "Maintain Current Baselines",
                    "description": "System is operating optimally.",
                    "priority": 1,
                    "expected_impact": "None",
                    "confidence": 0.99,
                }
            )

        logger.info(
            "Recommendation Agent completed", latency=time.perf_counter() - start
        )
        return {
            "recommendations": recommendations,
            "timestamps": {"recommendation_completed": time.time()},
        }
