"""
Routes for educational services.
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import QuestionRequest, AnswerResponse
from app.services.ai_service import AIService

# Initialize router
router = APIRouter(prefix="/education", tags=["education"])

@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Process an educational question and return an answer.
    
    Args:
        request: The question request object
        
    Returns:
        AnswerResponse: The AI's response to the question
        
    Raises:
        HTTPException: If there is an error processing the request
    """
    try:
        # Get answer from AI service
        answer = await AIService.get_answer(request.question)
        
        # Return the response
        return AnswerResponse(answer=answer)
    
    except Exception as e:
        # Log the error (in a production environment, use a proper logging system)
        print(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process request: {str(e)}") 