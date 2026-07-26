import operator
from typing import Any, Dict, List, Optional, TypedDict

from typing_extensions import Annotated


def dict_update(left: Dict, right: Dict) -> Dict:
    res = left.copy()
    res.update(right)
    return res


class AgentState(TypedDict):
    """
    LangGraph typed state for the Autonomous Building Intelligence graph.
    """

    user_request: str
    conversation_history: Annotated[List[Dict[str, str]], operator.add]
    decision_goal: Optional[Dict[str, Any]]
    execution_plan: Optional[Dict[str, Any]]
    simulation_summary: Optional[Dict[str, Any]]
    analytics: Optional[Dict[str, Any]]
    diagnostics: Optional[Dict[str, Any]]
    recommendations: Optional[List[Dict[str, Any]]]
    errors: Annotated[List[str], operator.add]
    metadata: Dict[str, Any]
    timestamps: Annotated[Dict[str, float], dict_update]
