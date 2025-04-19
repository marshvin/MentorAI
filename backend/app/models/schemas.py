"""
Pydantic models for request and response validation.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional

class QuestionRequest(BaseModel):
    """Request model for asking a question."""
    question: str = Field(
        ..., 
        description="The educational question to be answered",
        example="What is photosynthesis and how does it work?",
        min_length=3,
        max_length=500
    )
    
    @validator('question')
    def validate_question_content(cls, v):
        # Check if question is not just whitespace
        if v.strip() == "":
            raise ValueError("Question cannot be empty or just whitespace")
        
        # Check if question actually ends with a question mark or is a command/request
        if not (v.strip().endswith('?') or 'explain' in v.lower() or 'how' in v.lower() or 
                'what' in v.lower() or 'why' in v.lower() or 'where' in v.lower() or 
                'when' in v.lower() or 'who' in v.lower() or 'which' in v.lower() or
                'describe' in v.lower() or 'define' in v.lower() or 'tell me' in v.lower()):
            raise ValueError("Input should be a question or educational request")
        
        return v

class AnswerResponse(BaseModel):
    """Response model for an answered question."""
    answer: str = Field(
        ..., 
        description="The AI-generated answer to the educational question",
        example="Photosynthesis is the process by which green plants, algae, and some bacteria convert light energy into chemical energy. During photosynthesis, these organisms capture sunlight and use it to convert water and carbon dioxide into oxygen and energy-rich sugars..."
    ) 
    error: Optional[str] = Field(
        None,
        description="Error message in case of processing issues"
    ) 