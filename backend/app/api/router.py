from fastapi import APIRouter

from app.api.endpoints import ai, decision, health, simulations

api_router = APIRouter()

# Include endpoint routers here
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(simulations.router, tags=["Simulation"])
api_router.include_router(decision.router, tags=["Decision"])
api_router.include_router(ai.router, tags=["AI"])
