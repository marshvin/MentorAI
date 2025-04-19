"""
Service for interacting with the Google Gemini AI model.
"""

import google.generativeai as genai
import time
import re
from app.config.settings import GOOGLE_API_KEY, AI_MODEL, SYSTEM_PROMPT
from app.services.conversation_service import ConversationService
from typing import Dict, Any, Optional, Tuple, Union, List

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
    
    # List of educational topics for detecting non-educational queries
    EDUCATIONAL_TOPICS = [
        'math', 'mathematics', 'algebra', 'geometry', 'calculus', 'statistics', 'trigonometry',
        'science', 'biology', 'chemistry', 'physics', 'astronomy', 'geology', 'ecology',
        'history', 'geography', 'social studies', 'civics', 'economics', 'politics',
        'literature', 'grammar', 'writing', 'reading', 'language', 'english', 'spanish', 'french',
        'programming', 'computer', 'coding', 'algorithm', 'data structure',
        'art', 'music', 'philosophy', 'psychology', 'sociology', 'anthropology',
        'education', 'learning', 'study', 'research', 'academic', 'school', 'college', 'university',
        'theory', 'concept', 'principle', 'law', 'formula', 'equation', 'theorem',
        'cell', 'molecule', 'atom', 'element', 'compound', 'reaction',
        'photosynthesis', 'respiration', 'evolution', 'genetics', 'dna', 'ecosystem',
        'planet', 'solar system', 'universe', 'gravity', 'force', 'energy', 'matter',
        'world war', 'civilization', 'empire', 'revolution', 'democracy', 'monarchy',
        'novel', 'poem', 'essay', 'author', 'literary', 'shakespeare', 'dickens',
        'verb', 'noun', 'adjective', 'adverb', 'pronoun', 'preposition', 'conjunction',
        'python', 'java', 'javascript', 'html', 'css', 'sql', 'database',
        'renaissance', 'reformation', 'enlightenment', 'industrial revolution',
        'climate', 'weather', 'environment', 'pollution', 'sustainability',
        'health', 'nutrition', 'exercise', 'disease', 'medicine', 'vaccine',
        'engineering', 'architecture', 'design', 'technology', 'innovation',
        'proof', 'evidence', 'experiment', 'observation', 'hypothesis'
    ]
    
    @staticmethod
    async def get_answer(question: str, conversation_id: Optional[str] = None, max_retries: int = 2) -> Tuple[str, str]:
        """
        Get an answer to a question from the AI model.
        
        Args:
            question: The question to ask the AI
            conversation_id: Optional ID of an existing conversation
            max_retries: Maximum number of retry attempts if model fails
            
        Returns:
            A tuple containing (AI's response as a string, conversation ID)
            
        Raises:
            ModelConnectionError: If there is an error connecting to the AI service
            ModelResponseError: If there is an error with the model's response
            AIServiceError: For other AI service related errors
        """
        # Sanitize input
        sanitized_question = question.strip()
        if not sanitized_question:
            raise ValueError("Question cannot be empty")
        
        # Get or create conversation
        if conversation_id:
            try:
                # Validate that conversation exists
                conversation = ConversationService.get_conversation(conversation_id)
                if not conversation:
                    # If conversation doesn't exist, create a new one
                    conversation = ConversationService.create_conversation()
                    conversation_id = conversation.id
            except ValueError:
                # If conversation doesn't exist, create a new one
                conversation = ConversationService.create_conversation()
                conversation_id = conversation.id
        else:
            # Create a new conversation
            conversation = ConversationService.create_conversation()
            conversation_id = conversation.id
        
        # Add user message to history
        ConversationService.add_message(conversation_id, "user", sanitized_question)
            
        retry_count = 0
        last_error = None
        
        while retry_count <= max_retries:
            try:
                # Initialize the Gemini model
                model = genai.GenerativeModel(AI_MODEL)
                
                # Get formatted conversation history
                history = ConversationService.format_history_for_gemini(conversation_id)
                
                # Create chat session
                chat = model.start_chat(history=[])
                
                # Always send system prompt first for consistent behavior
                chat.send_message(SYSTEM_PROMPT)
                
                # Send all messages in history
                for message in history:
                    chat.send_message(message["parts"][0])
                
                # Send the user's question and get response
                response = chat.send_message(sanitized_question)
                
                # Validate response
                if not response or not response.text or len(response.text.strip()) == 0:
                    raise ModelResponseError("Received empty response from AI model")
                
                # Add the AI's response to the conversation history
                ConversationService.add_message(conversation_id, "model", response.text)
                
                # Return the AI's response and conversation ID
                return response.text, conversation_id
                
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