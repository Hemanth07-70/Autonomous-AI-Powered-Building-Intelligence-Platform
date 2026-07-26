from typing import Optional

from pydantic import BaseModel, Field

from app.orchestrator.decision_models import DecisionGoal


class AIChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    building_id: Optional[str] = None


class AIChatResponse(BaseModel):
    response: str
    decision_goal: DecisionGoal


class AIHealthResponse(BaseModel):
    available: bool
    model: str


class AIModelsResponse(BaseModel):
    models: list[str]
    selected_model: str
