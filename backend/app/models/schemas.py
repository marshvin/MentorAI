"""
Pydantic models for request and response validation.
"""

from pydantic import BaseModel, Field

class QuestionRequest(BaseModel):
    """Request model for asking a question."""
    question: str = Field(
        ..., 
        description="The educational question to be answered",
        example="What is photosynthesis and how does it work?"
    )

class AnswerResponse(BaseModel):
    """Response model for an answered question."""
    answer: str = Field(
        ..., 
        description="The AI-generated answer to the educational question",
        example="Photosynthesis is the process by which green plants, algae, and some bacteria convert light energy into chemical energy. During photosynthesis, these organisms capture sunlight and use it to convert water and carbon dioxide into oxygen and energy-rich sugars..."
    ) 