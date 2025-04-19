"""
Routes for educational services.
"""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.models.schemas import QuestionRequest, AnswerResponse
from app.services.ai_service import AIService, ModelConnectionError, ModelResponseError, AIServiceError

# Initialize router
router = APIRouter(
    prefix="/education", 
    tags=["education"],
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"description": "AI service unavailable"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Invalid input data"}
    }
)

@router.post(
    "/ask", 
    response_model=AnswerResponse,
    status_code=status.HTTP_200_OK,
    summary="Ask an educational question",
    description="Send an educational question to the AI and receive an informative answer.",
    responses={
        status.HTTP_200_OK: {
            "description": "Successful response",
            "content": {
                "application/json": {
                    "example": {
                        "answer": "Photosynthesis is the process by which green plants and some other organisms convert light energy into chemical energy. During photosynthesis, plants capture light energy and use it to convert water, carbon dioxide, and minerals into oxygen and energy-rich organic compounds."
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid question format",
            "content": {
                "application/json": {
                    "example": {"detail": "Question must be phrased as a question or educational request"}
                }
            }
        },
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "AI service unavailable",
            "content": {
                "application/json": {
                    "example": {"detail": "AI service is currently unavailable. Please try again later."}
                }
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error processing the request",
            "content": {
                "application/json": {
                    "example": {"detail": "Failed to process request: Service unavailable"}
                }
            }
        }
    }
)
async def ask_question(request: QuestionRequest):
    """
    Process an educational question and return an answer.
    
    This endpoint only responds to educational topics like math, science, history, 
    literature, languages, programming, and other academic subjects.
    
    Args:
        request: The question request object containing the educational question
        
    Returns:
        AnswerResponse: The AI's response to the educational question
        
    Raises:
        HTTPException: If there is an error processing the request
    """
    try:
        # Log the question (in a production environment, use a proper logging system)
        print(f"Processing question: {request.question}")
        
        # Get answer from AI service
        answer = await AIService.get_answer(request.question)
        
        # Return the response
        return AnswerResponse(answer=answer)
    
    except ValueError as e:
        # Input validation errors (already handled by Pydantic but as a fallback)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except ModelConnectionError as e:
        # Connection issues with the AI model
        # Log the error (in a production environment, use a proper logging system)
        print(f"AI service connection error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI service is currently unavailable. Please try again later."
        )
    
    except ModelResponseError as e:
        # Issues with the AI model's response
        print(f"AI model response error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error with AI model response: {str(e)}"
        )
    
    except AIServiceError as e:
        # General AI service errors
        print(f"AI service error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI service error: {str(e)}"
        )
    
    except Exception as e:
        # Unexpected errors
        print(f"Unexpected error processing request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Failed to process request: {str(e)}"
        ) 