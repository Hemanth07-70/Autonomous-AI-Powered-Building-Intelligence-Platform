from fastapi import APIRouter, Request

from app.ai.client import OllamaClient
from app.ai.exceptions import (
    AIConnectionError,
    InvalidAIResponse,
    ModelUnavailableError,
    UnsupportedGoalError,
)
from app.ai.planner import AIPlanner
from app.ai.schemas import (
    AIChatRequest,
    AIChatResponse,
    AIHealthResponse,
    AIModelsResponse,
)
from app.core.exceptions import BadRequestException
from app.orchestrator.decision_models import DecisionGoal

router = APIRouter(prefix="/api/ai")


def get_ai_planner(request: Request) -> AIPlanner:
    return request.app.state.ai_planner


def get_ollama_client(request: Request) -> OllamaClient:
    return request.app.state.ollama_client


@router.post("/chat", response_model=AIChatResponse, summary="AI Chat")
async def chat(payload: AIChatRequest, request: Request) -> AIChatResponse:
    planner = get_ai_planner(request)
    try:
        response, goal = planner.chat(payload.message, building_id=payload.building_id)
        return AIChatResponse(response=response, decision_goal=goal)
    except (
        AIConnectionError,
        InvalidAIResponse,
        ModelUnavailableError,
        UnsupportedGoalError,
    ) as exc:
        raise BadRequestException(str(exc)) from exc


@router.post("/plan", response_model=DecisionGoal, summary="Create AI Decision Goal")
async def plan(payload: AIChatRequest, request: Request) -> DecisionGoal:
    planner = get_ai_planner(request)
    try:
        return planner.plan(payload.message, building_id=payload.building_id)
    except (
        AIConnectionError,
        InvalidAIResponse,
        ModelUnavailableError,
        UnsupportedGoalError,
    ) as exc:
        raise BadRequestException(str(exc)) from exc


@router.get("/models", response_model=AIModelsResponse, summary="List AI Models")
async def models(request: Request) -> AIModelsResponse:
    client = get_ollama_client(request)
    try:
        return AIModelsResponse(
            models=client.list_models(),
            selected_model=client.model,
        )
    except AIConnectionError as exc:
        raise BadRequestException(str(exc)) from exc


@router.get("/health", response_model=AIHealthResponse, summary="AI Health Check")
async def health(request: Request) -> AIHealthResponse:
    client = get_ollama_client(request)
    return AIHealthResponse(
        available=client.health_check(),
        model=client.model,
    )
