"""
Service for interacting with the Google Gemini AI model.
"""

import google.generativeai as genai
import time
import re
from app.config.settings import GOOGLE_API_KEY, AI_MODEL, SYSTEM_PROMPT
from typing import Dict, Any, Optional, Tuple, Union

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
    
    # List of educational topics
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
    
    # Non-educational response message
    NON_EDUCATIONAL_MESSAGE = "I'm sorry, but I'm designed to help with educational questions. I can assist with topics like math, science, history, literature, languages, programming, and other academic subjects. Could you please ask me something related to education or academics?"
    
    @classmethod
    def is_educational_query(cls, query: str) -> bool:
        """
        Check if a query is educational in nature.
        
        Args:
            query: The query to check
            
        Returns:
            True if the query is educational, False otherwise
        """
        query_lower = query.lower()
        
        # Check if any educational topic is in the query
        for topic in cls.EDUCATIONAL_TOPICS:
            if topic in query_lower:
                return True
                
        # Check for educational patterns
        educational_patterns = [
            r'what\s+is',
            r'how\s+to',
            r'why\s+do',
            r'explain\s+',
            r'define\s+',
            r'describe\s+',
            r'meaning\s+of',
            r'difference\s+between',
            r'tell\s+me\s+about',
            r'who\s+was',
            r'when\s+did',
            r'where\s+is',
            r'calculate',
            r'solve',
            r'\bguide\b',
            r'\bdefinition\b',
            r'\bconcept\b',
            r'\bprocess\b',
            r'\bmethod\b',
            r'\bexample\b',
            r'\btheory\b',
            r'\bsteps\b',
            r'\bcauses\b',
            r'\beffects\b',
            r'\bopinion\b',
            r'\bevaluation\b',
            r'\breview\b',
            r'\banalysis\b',
            r'\bformula\b',
            r'\bequation\b',
            r'\bproblem\b',
            r'\bsolution\b',
            r'\bcourse\b',
            r'\blearn\b',
            r'\bstudy\b',
            r'\bunderstand\b',
            r'\bresearch\b',
            r'\bexplanation\b',
            r'\btutorial\b',
            r'\bhelp\b'
        ]
        
        for pattern in educational_patterns:
            if re.search(pattern, query_lower):
                return True
                
        # If we've reached this point, the query might not be educational
        return False
    
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
            
        # Check if the question is educational in nature
        if not AIService.is_educational_query(sanitized_question):
            # Return polite message instead of raising an error
            return AIService.NON_EDUCATIONAL_MESSAGE
            
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