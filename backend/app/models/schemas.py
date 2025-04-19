"""
Pydantic models for request and response validation.
"""

from pydantic import BaseModel

class QuestionRequest(BaseModel):
    """Request model for asking a question."""
    question: str

class AnswerResponse(BaseModel):
    """Response model for an answered question."""
    answer: str 