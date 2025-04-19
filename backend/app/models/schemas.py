"""
Pydantic models for request and response validation.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
import uuid

class QuestionRequest(BaseModel):
    """Request model for asking a question."""
    question: str = Field(
        ..., 
        description="The educational question to be answered",
        example="What is photosynthesis and how does it work?",
        min_length=1,
        max_length=1000
    )
    conversation_id: Optional[str] = Field(
        None,
        description="Optional conversation ID to maintain context between messages"
    )
    
    @validator('question')
    def validate_question_content(cls, v):
        # Only check if the question is not just whitespace
        if v.strip() == "":
            raise ValueError("Question cannot be empty or just whitespace")
        
        # No further validation on question format to allow statements like "PHOTOSYNTHESIS PROCESS"
        return v

class Message(BaseModel):
    """Model for a single message in a conversation."""
    role: str = Field(..., description="Role of the message sender (user or model)")
    content: str = Field(..., description="Content of the message")

class ConversationHistory(BaseModel):
    """Model for conversation history."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique conversation ID")
    messages: List[Message] = Field(default_factory=list, description="List of messages in the conversation")

class AnswerResponse(BaseModel):
    """Response model for an answered question."""
    answer: str = Field(
        ..., 
        description="The AI-generated answer to the educational question",
        example="Photosynthesis is the process by which green plants, algae, and some bacteria convert light energy into chemical energy. During photosynthesis, these organisms capture sunlight and use it to convert water and carbon dioxide into oxygen and energy-rich sugars..."
    ) 
    conversation_id: str = Field(
        ...,
        description="Conversation ID to use for future messages in this conversation"
    )
    error: Optional[str] = Field(
        None,
        description="Error message in case of processing issues"
    ) 