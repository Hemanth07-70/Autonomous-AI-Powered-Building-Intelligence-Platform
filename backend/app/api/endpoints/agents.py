from fastapi import APIRouter, HTTPException, Request

from app.agents.graph import build_graph
from app.agents.schemas import AgentHealthResponse, AgentRunRequest, AgentRunResponse
from app.agents.state import AgentState

router = APIRouter(prefix="/api/agents")


def get_graph(request: Request):
    # Depending on how dependencies are injected, we could build it once or per request
    # Here we assume the app state has ai_planner and decision_engine
    planner = request.app.state.ai_planner
    engine = getattr(request.app.state, "decision_engine", None)
    return build_graph(planner, engine)


@router.post(
    "/run", response_model=AgentRunResponse, summary="Run Autonomous Agent Graph"
)
def run_graph(payload: AgentRunRequest, request: Request) -> AgentRunResponse:
    graph = get_graph(request)

    initial_state = AgentState(
        user_request=payload.message,
        conversation_history=[],
        decision_goal=None,
        execution_plan=None,
        simulation_summary=None,
        analytics=None,
        diagnostics=None,
        recommendations=None,
        errors=[],
        metadata={},
        timestamps={},
    )

    try:
        # LangGraph runs synchronously by default in this setup,
        # but could use ainvoke for async. We will use invoke here.
        final_state = graph.invoke(initial_state)

        return AgentRunResponse(
            decision_goal=final_state.get("decision_goal"),
            execution_plan=final_state.get("execution_plan"),
            analytics=final_state.get("analytics"),
            diagnostics=final_state.get("diagnostics"),
            recommendations=final_state.get("recommendations", []),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", response_model=AgentHealthResponse, summary="Agent Graph Health")
async def health() -> AgentHealthResponse:
    return AgentHealthResponse(
        langgraph=True,
        agents=["planner", "analytics", "diagnostics", "recommendation", "supervisor"],
        version="1.0.0",
    )
