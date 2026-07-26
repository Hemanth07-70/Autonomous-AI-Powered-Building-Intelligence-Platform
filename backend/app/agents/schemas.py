from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Recommendation(BaseModel):
    title: str
    description: str
    priority: int = Field(..., ge=1, le=10)
    expected_impact: str
    confidence: float = Field(..., ge=0.0, le=1.0)


class AgentRunRequest(BaseModel):
    message: str


class AgentRunResponse(BaseModel):
    decision_goal: Optional[Dict[str, Any]] = None
    execution_plan: Optional[Dict[str, Any]] = None
    analytics: Optional[Dict[str, Any]] = None
    diagnostics: Optional[Dict[str, Any]] = None
    recommendations: List[Recommendation] = Field(default_factory=list)


class AgentHealthResponse(BaseModel):
    langgraph: bool
    agents: List[str]
    version: str
