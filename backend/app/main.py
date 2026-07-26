from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.ai.client import OllamaClient
from app.ai.planner import AIPlanner
from app.api.router import api_router
from app.config.settings import settings
from app.core.exception_handlers import setup_exception_handlers
from app.core.logging import setup_logging
from app.middleware.logging import LoggingMiddleware
from app.middleware.request_id import RequestIdMiddleware
from app.orchestrator.decision_engine import DecisionEngine
from app.scheduler.simulation_orchestrator import SimulationOrchestrator
from app.scheduler.task_scheduler import TaskScheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events for the FastAPI application.
    """
    # Startup setup
    setup_logging()
    yield
    # Shutdown teardown


# OpenAPI Tags metadata for professional Swagger documentation
openapi_tags = [
    {
        "name": "Health",
        "description": "System health and status endpoints.",
    },
    {
        "name": "AI",
        "description": (
            "Endpoints related to AI inference, agents, " "and LLM integrations."
        ),
    },
    {
        "name": "EnergyPlus",
        "description": (
            "Endpoints managing the EnergyPlus Digital Twin " "and simulations."
        ),
    },
    {
        "name": "Analytics",
        "description": "Data analytics, aggregations, and optimization metrics.",
    },
    {
        "name": "Dashboard",
        "description": "Frontend dashboard data providers.",
    },
    {
        "name": "Simulation",
        "description": "Control over active environment simulations.",
    },
]


def create_app() -> FastAPI:
    """
    Factory function to create and configure the FastAPI application.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        description=(
            "Autonomous AI platform that continuously monitors, reasons, "
            "and optimizes smart building energy consumption "
            "using EnergyPlus as a Digital Twin."
        ),
        version=settings.VERSION,
        openapi_tags=openapi_tags,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )
    app.state.simulation_orchestrator = SimulationOrchestrator()
    app.state.decision_engine = DecisionEngine(app.state.simulation_orchestrator)
    app.state.ollama_client = OllamaClient()
    app.state.ai_planner = AIPlanner(
        app.state.ollama_client,
        app.state.decision_engine,
    )
    app.state.task_scheduler = TaskScheduler()

    # Register Middlewares (Note: Last added runs first for response,
    # but first added runs first for request)
    # We want RequestId to be the absolute outer layer so it wraps logging as well
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Restrict this in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register Exception Handlers
    setup_exception_handlers(app)

    # Include routers
    app.include_router(api_router)

    return app


app = create_app()
