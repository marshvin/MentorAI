"""
Main API router that includes all route modules.
"""

from fastapi import APIRouter, status
from pydantic import BaseModel
from app.routes import education, health

class RootResponse(BaseModel):
    """Response model for the root endpoint."""
    message: str

# Initialize main API router
api_router = APIRouter()

# Include all routers
api_router.include_router(health.router)
api_router.include_router(education.router)

# Root endpoint
@api_router.get(
    "/", 
    response_model=RootResponse,
    summary="API Root",
    description="Root endpoint providing basic API information.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Welcome message",
            "content": {
                "application/json": {
                    "example": {"message": "Welcome to MentorAI API. Visit /health for status."}
                }
            }
        }
    }
)
async def root():
    """
    Root endpoint that provides basic information about the API.
    
    Returns:
        RootResponse: A welcome message with basic API information
    """
    return RootResponse(message="Welcome to MentorAI API. Visit /health for status.") 