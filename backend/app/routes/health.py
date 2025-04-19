"""
Health check routes for the application.
"""

from fastapi import APIRouter

# Initialize router
router = APIRouter(prefix="/health", tags=["health"])

@router.get("")
async def health_check():
    """
    Simple health check endpoint to verify that the API is running.
    
    Returns:
        dict: A status message
    """
    return {"status": "online", "message": "MentorAI API is running"} 