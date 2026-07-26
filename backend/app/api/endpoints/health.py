from fastapi import APIRouter

from app.config.settings import settings

router = APIRouter()


@router.get("/", summary="Root Endpoint", response_model=dict)
async def root():
    """
    Root endpoint returning basic application information.
    """
    return {
        "application": settings.APP_NAME,
        "status": "running",
        "version": settings.VERSION,
    }


@router.get("/health", summary="Health Check", response_model=dict)
async def health_check():
    """
    Health check endpoint for Kubernetes/Docker probes.
    """
    return {"status": "healthy"}
