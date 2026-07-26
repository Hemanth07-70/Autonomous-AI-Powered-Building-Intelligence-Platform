from fastapi import APIRouter

from app.api.endpoints import agents, ai, decision, health, simulations

api_router = APIRouter()

# Include endpoint routers here
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(simulations.router, tags=["Simulation"])
api_router.include_router(decision.router, tags=["Decision"])
api_router.include_router(ai.router, tags=["AI"])
api_router.include_router(agents.router, tags=["Agents"])
