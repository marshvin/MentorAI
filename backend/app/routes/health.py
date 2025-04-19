"""
Health check routes for the API.
"""

from fastapi import APIRouter, status
from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str


# Initialize router
router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Checks if the API is up and running.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "API is healthy",
            "content": {
                "application/json": {
                    "example": {"status": "ok"}
                }
            }
        }
    }
)
async def health_check():
    """
    Performs a health check on the API.
    
    Returns:
        HealthResponse: A simple status response indicating the API is healthy
    """
    return HealthResponse(status="ok") 