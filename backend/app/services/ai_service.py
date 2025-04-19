"""
Service for interacting with the Google Gemini AI model.
"""

import google.generativeai as genai
import time
from app.config.settings import GOOGLE_API_KEY, AI_MODEL, SYSTEM_PROMPT
from typing import Dict, Any, Optional

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

class AIServiceError(Exception):
    """Base exception for AI service errors."""
    pass

class ModelConnectionError(AIServiceError):
    """Exception raised when there's an issue connecting to the AI model."""
    pass

class ModelResponseError(AIServiceError):
    """Exception raised when there's an issue with the AI model's response."""
    pass

class AIService:
    """Service for handling AI interactions with Google Gemini."""
    
    @staticmethod
    async def get_answer(question: str, max_retries: int = 2) -> str:
        """
        Get an answer to a question from the AI model.
        
        Args:
            question: The question to ask the AI
            max_retries: Maximum number of retry attempts if model fails
            
        Returns:
            The AI's response as a string
            
        Raises:
            ModelConnectionError: If there is an error connecting to the AI service
            ModelResponseError: If there is an error with the model's response
            AIServiceError: For other AI service related errors
        """
        # Sanitize input
        sanitized_question = question.strip()
        if not sanitized_question:
            raise ValueError("Question cannot be empty")
            
        retry_count = 0
        last_error = None
        
        while retry_count <= max_retries:
            try:
                # Initialize the Gemini model
                model = genai.GenerativeModel(AI_MODEL)
                
                # Create chat session with system prompt
                chat = model.start_chat(history=[
                    {"role": "user", "parts": ["Hi, I need help with my studies."]},
                    {"role": "model", "parts": ["Hello! I'm MentorAI, your AI educational assistant. I'm here to help you with your academic questions. What subject or topic are you studying?"]}
                ])
                
                # Add system instructions
                chat.send_message(SYSTEM_PROMPT)
                
                # Send the user's question
                response = chat.send_message(sanitized_question)
                
                # Validate response
                if not response or not response.text or len(response.text.strip()) == 0:
                    raise ModelResponseError("Received empty response from AI model")
                
                # Return the AI's response
                return response.text
                
            except (ConnectionError, TimeoutError) as e:
                last_error = e
                retry_count += 1
                if retry_count <= max_retries:
                    # Exponential backoff
                    wait_time = 2 ** retry_count
                    time.sleep(wait_time)
                else:
                    raise ModelConnectionError(f"Failed to connect to AI service after {max_retries} retries: {str(e)}")
                    
            except Exception as e:
                # Categorize other exceptions
                if "api_key" in str(e).lower():
                    raise AIServiceError(f"Authentication error with AI service: {str(e)}")
                elif "rate" in str(e).lower() and "limit" in str(e).lower():
                    raise AIServiceError(f"Rate limit exceeded: {str(e)}")
                else:
                    raise AIServiceError(f"Error getting answer from AI service: {str(e)}")
        
        # This should not happen due to the raise in the loop, but adding as a safeguard
        if last_error:
            raise AIServiceError(f"Failed to get answer after retries: {str(last_error)}") 