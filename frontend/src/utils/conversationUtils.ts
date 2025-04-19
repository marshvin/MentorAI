// Conversation type definition
export interface Message {
  isUser: boolean;
  text: string;
}

export interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  backend_conversation_id?: string; // ID from the backend API
}

// Generate a unique ID
export const generateId = (): string => {
  return Math.random().toString(36).substring(2, 9);
};

// Get a title from the first message
export const getTitleFromMessage = (message: string): string => {
  // Truncate to first 30 chars if longer
  return message.length > 30 
    ? message.substring(0, 27) + '...'
    : message;
};

// Save conversations to localStorage
export const saveConversations = (conversations: Conversation[]): void => {
  localStorage.setItem('mentorAI-conversations', JSON.stringify(conversations));
};

// Load conversations from localStorage
export const loadConversations = (): Conversation[] => {
  const saved = localStorage.getItem('mentorAI-conversations');
  if (!saved) return [];
  
  try {
    // Parse the saved conversations and ensure dates are properly converted
    const parsed = JSON.parse(saved);
    return parsed.map((convo: any) => ({
      ...convo,
      createdAt: new Date(convo.createdAt)
    }));
  } catch (e) {
    console.error('Failed to parse saved conversations', e);
    return [];
  }
};

// Create a new conversation
export const createNewConversation = (firstMessage?: Message): Conversation => {
  return {
    id: generateId(),
    title: firstMessage?.text 
      ? getTitleFromMessage(firstMessage.text) 
      : 'New Conversation',
    messages: firstMessage ? [firstMessage] : [],
    createdAt: new Date()
  };
};

// Save/update a specific conversation
export const saveConversation = (
  conversation: Conversation, 
  allConversations: Conversation[]
): Conversation[] => {
  const index = allConversations.findIndex(c => c.id === conversation.id);
  
  if (index >= 0) {
    // Update existing conversation
    const updated = [...allConversations];
    updated[index] = conversation;
    saveConversations(updated);
    return updated;
  } else {
    // Add new conversation
    const updated = [conversation, ...allConversations];
    saveConversations(updated);
    return updated;
  }
};

// Delete a conversation
export const deleteConversation = (
  conversationId: string, 
  allConversations: Conversation[]
): Conversation[] => {
  const updated = allConversations.filter(c => c.id !== conversationId);
  saveConversations(updated);
  return updated;
}; 