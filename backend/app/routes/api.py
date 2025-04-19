"""
Main API router that includes all route modules.
"""

from fastapi import APIRouter
from app.routes import education, health

# Initialize main API router
api_router = APIRouter()

# Include all routers
api_router.include_router(health.router)
api_router.include_router(education.router)

# Root endpoint
@api_router.get("/")
async def root():
    """
    Root endpoint that redirects to health check.
    
    Returns:
        dict: A redirect message
    """
    return {"message": "Welcome to MentorAI API. Visit /health for status."} 