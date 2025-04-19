"""
Service for interacting with the Google Gemini AI model.
"""

import google.generativeai as genai
from app.config.settings import GOOGLE_API_KEY, AI_MODEL, SYSTEM_PROMPT

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

class AIService:
    """Service for handling AI interactions with Google Gemini."""
    
    @staticmethod
    async def get_answer(question: str) -> str:
        """
        Get an answer to a question from the AI model.
        
        Args:
            question: The question to ask the AI
            
        Returns:
            The AI's response as a string
            
        Raises:
            Exception: If there is an error communicating with the AI service
        """
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
            response = chat.send_message(question)
            
            # Return the AI's response
            return response.text
            
        except Exception as e:
            # Re-raise the exception with additional context
            raise Exception(f"Error getting answer from AI service: {str(e)}") 