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
    
    # Greeting patterns
    GREETING_PATTERNS = [
        r'^hi\b',
        r'^hello\b',
        r'^hey\b',
        r'^greetings\b',
        r'^good\s+(morning|afternoon|evening)\b',
        r'^howdy\b',
        r'^hola\b',
        r'^bonjour\b'
    ]
    
    @classmethod
    def is_greeting(cls, query: str) -> bool:
        """Check if the query is a greeting."""
        query_lower = query.lower()
        return any(re.search(pattern, query_lower) for pattern in cls.GREETING_PATTERNS)
    
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
        
        # Always allow greetings in new conversations
        if cls.is_greeting(query):
            return True
        
        # Check if any educational topic is in the query
        for topic in cls.EDUCATIONAL_TOPICS:
            if topic in query_lower:
                return True
        
        # Check for follow-up patterns that might not contain educational keywords
        follow_up_patterns = [
            r'tell\s+me\s+more',
            r'explain\s+more',
            r'elaborate',
            r'go\s+on',
            r'continue',
            r'what\s+else',
            r'can\s+you\s+explain\s+that',
            r'please\s+continue',
            r'more\s+details',
            r'explain\s+further',
            r'elaborate\s+on\s+that',
            r'why\s+is\s+that',
            r'how\s+does\s+that\s+work',
            r'give\s+me\s+an\s+example',
            r'examples\s+please',
            r'more\s+info'
        ]
        
        for pattern in follow_up_patterns:
            if re.search(pattern, query_lower):
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
            
        # Check if the question is educational in nature (only for new conversations or non-follow-ups)
        if len(ConversationService.get_messages(conversation_id)) == 0:
            # For new conversations, allow greetings
            if AIService.is_greeting(sanitized_question):
                greeting_response = "Hello! I'm MentorAI, your educational assistant. I can help you with subjects like math, science, history, literature, and more. What would you like to learn about?"
                ConversationService.add_message(conversation_id, "user", sanitized_question)
                ConversationService.add_message(conversation_id, "model", greeting_response)
                return greeting_response, conversation_id
            elif not AIService.is_educational_query(sanitized_question):
                # Add the non-educational question and response to the conversation history
                ConversationService.add_message(conversation_id, "user", sanitized_question)
                ConversationService.add_message(conversation_id, "model", AIService.NON_EDUCATIONAL_MESSAGE)
                return AIService.NON_EDUCATIONAL_MESSAGE, conversation_id
        
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
                
                # Create chat session with history
                chat = model.start_chat(history=[])
                
                # Add system instructions if this is a new conversation
                if len(ConversationService.get_messages(conversation_id)) <= 1:
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