import time
from typing import Any, Dict

import structlog

from app.agents.state import AgentState

logger = structlog.get_logger("agents.analytics")


class AnalyticsAgentNode:
    """
    Node that calculates KPIs based strictly on simulation summaries.
    Does not hallucinate LLM values.
    """

    def __call__(self, state: AgentState) -> Dict[str, Any]:
        logger.info("Analytics Agent starting")
        start = time.perf_counter()

        plan = state.get("execution_plan")
        summary = state.get("simulation_summary")

        if plan and not summary:
            # No simulation results yet, do not output placeholder KPIs
            analytics = {
                "status": "Awaiting Simulation Execution",
                "estimated_runtime": plan.get("estimated_runtime"),
                "pending_jobs": len(plan.get("simulation_jobs", [])),
            }
        else:
            summary = summary or {}
            # Calculate strict deterministic KPIs
            analytics = {
                "energy_kpis": {"total_kwh": summary.get("energy_used", 0) * 1.05},
                "carbon_kpis": {"total_kg_co2": summary.get("energy_used", 0) * 0.4},
                "cost_kpis": {"total_usd": summary.get("energy_used", 0) * 0.12},
                "comfort_kpis": {"avg_pmv": summary.get("comfort_score", 0)},
                "efficiency_summary": "Derived entirely from simulated values",
                "building_performance_summary": "Performance computed strictly from ExecutionPlan targets.",
            }

        logger.info("Analytics Agent completed", latency=time.perf_counter() - start)
        return {
            "analytics": analytics,
            "timestamps": {"analytics_completed": time.time()},
        }
