"""
Service for managing conversation histories.
"""

import uuid
from typing import Dict, List, Optional
from app.models.schemas import ConversationHistory, Message

class ConversationService:
    """Service for managing conversation histories."""
    
    # In-memory store of conversation histories (in a production app, this would be a database)
    _conversations: Dict[str, ConversationHistory] = {}
    
    @classmethod
    def create_conversation(cls) -> ConversationHistory:
        """
        Create a new conversation.
        
        Returns:
            A new ConversationHistory object
        """
        conversation = ConversationHistory()
        cls._conversations[conversation.id] = conversation
        return conversation
    
    @classmethod
    def get_conversation(cls, conversation_id: str) -> Optional[ConversationHistory]:
        """
        Get a conversation by ID.
        
        Args:
            conversation_id: The ID of the conversation to get
            
        Returns:
            The conversation if found, None otherwise
        """
        return cls._conversations.get(conversation_id)
    
    @classmethod
    def add_message(cls, conversation_id: str, role: str, content: str) -> None:
        """
        Add a message to a conversation.
        
        Args:
            conversation_id: The ID of the conversation to add the message to
            role: The role of the message sender ('user' or 'model')
            content: The content of the message
            
        Raises:
            ValueError: If the conversation ID is not found
        """
        conversation = cls.get_conversation(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation with ID {conversation_id} not found")
        
        conversation.messages.append(Message(role=role, content=content))
    
    @classmethod
    def get_messages(cls, conversation_id: str) -> List[Message]:
        """
        Get all messages in a conversation.
        
        Args:
            conversation_id: The ID of the conversation to get messages from
            
        Returns:
            A list of messages in the conversation
            
        Raises:
            ValueError: If the conversation ID is not found
        """
        conversation = cls.get_conversation(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation with ID {conversation_id} not found")
        
        return conversation.messages
    
    @classmethod
    def format_history_for_gemini(cls, conversation_id: str) -> List[Dict]:
        """
        Format conversation history for the Gemini API.
        
        Args:
            conversation_id: The ID of the conversation to format
            
        Returns:
            A list of message dictionaries in Gemini's format
            
        Raises:
            ValueError: If the conversation ID is not found
        """
        messages = cls.get_messages(conversation_id)
        
        # Format messages for Gemini
        return [
            {"role": message.role, "parts": [message.content]}
            for message in messages
        ] 