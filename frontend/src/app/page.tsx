'use client';

import React, { useState, useEffect } from 'react';
import { BeatLoader } from 'react-spinners';
import ChatMessage from '@/components/ChatMessage';
import ChatInput from '@/components/ChatInput';
import Sidebar from '@/components/Sidebar';
import { educationApi } from '@/api';
import { 
  Conversation, 
  Message,
  loadConversations, 
  saveConversation,
  createNewConversation,
  deleteConversation
} from '@/utils/conversationUtils';

export default function Home() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversation, setActiveConversation] = useState<Conversation | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  // Load conversations from localStorage on initial load
  useEffect(() => {
    const savedConversations = loadConversations();
    setConversations(savedConversations);
    
    // Set active conversation to the most recent one or create a new one
    if (savedConversations.length > 0) {
      setActiveConversation(savedConversations[0]);
    } else {
      handleNewChat();
    }
  }, []);

  const handleNewChat = () => {
    const newConversation = createNewConversation();
    setActiveConversation(newConversation);
    setConversations(prev => [newConversation, ...prev]);
  };

  const handleSelectConversation = (id: string) => {
    const selected = conversations.find(c => c.id === id);
    if (selected) {
      setActiveConversation(selected);
    }
  };

  const handleSendMessage = async (text: string) => {
    if (!text.trim() || !activeConversation) return;

    // Create a copy of the active conversation
    const updatedConversation = { ...activeConversation };
    
    // Add user message
    const newUserMessage: Message = { isUser: true, text };
    updatedConversation.messages = [...updatedConversation.messages, newUserMessage];
    
    // If this is the first message, update the title
    if (updatedConversation.messages.length === 1) {
      updatedConversation.title = text.length > 30 
        ? text.substring(0, 27) + '...' 
        : text;
    }
    
    // Update state
    setActiveConversation(updatedConversation);
    setConversations(saveConversation(updatedConversation, conversations));
    setIsLoading(true);
    setError('');

    try {
      // Call backend API using our API module
      const response = await educationApi.askQuestion(text);

      // Add AI response
      const newAIMessage: Message = {
        isUser: false,
        text: response.answer
      };
      
      // Update with AI message
      const finalConversation = { 
        ...updatedConversation,
        messages: [...updatedConversation.messages, newAIMessage]
      };
      
      setActiveConversation(finalConversation);
      setConversations(saveConversation(finalConversation, conversations));
    } catch (err) {
      console.error('Error calling API:', err);
      setError('Failed to get a response. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = () => {
    if (!activeConversation) return;
    
    // Create a new conversation to replace the active one
    const newConversation = createNewConversation();
    setActiveConversation(newConversation);
    
    // Update the conversations list
    const updated = conversations.filter(c => c.id !== activeConversation.id);
    setConversations([newConversation, ...updated]);
  };

  const handleDeleteConversation = (id: string) => {
    // Check if we're deleting the active conversation
    const isActive = activeConversation?.id === id;
    
    // Update conversations list
    const updatedConversations = deleteConversation(id, conversations);
    setConversations(updatedConversations);
    
    // If we deleted the active conversation, set a new active conversation
    if (isActive) {
      if (updatedConversations.length > 0) {
        setActiveConversation(updatedConversations[0]);
      } else {
        // If no conversations left, create a new one
        handleNewChat();
      }
    }
  };

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <>
      {/* Mobile sidebar toggle */}
      <button 
        className="fixed top-4 left-4 md:hidden z-20 p-2 bg-primary text-white rounded-md"
        onClick={toggleSidebar}
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
      </button>
      
      {/* Sidebar */}
      <div className={`md:relative fixed inset-y-0 left-0 z-10 transform transition-transform duration-300 ease-in-out ${
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
      } md:translate-x-0`}>
        <Sidebar 
          conversations={conversations}
          activeConversationId={activeConversation?.id || null}
          onSelectConversation={handleSelectConversation}
          onDeleteConversation={handleDeleteConversation}
          onNewChat={handleNewChat}
        />
      </div>
      
      {/* Chat area */}
      <div className="flex-1 flex flex-col h-screen overflow-hidden">
        <header className="bg-white border-b p-4 flex items-center">
          <h1 className="text-xl font-bold text-primary">EduBuddy</h1>
          <p className="text-gray-600 ml-4">Your AI-powered educational assistant</p>
        </header>
        
        <div className="flex-1 overflow-y-auto p-4">
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-xl shadow-md p-4 mb-4">
              {activeConversation && activeConversation.messages.length === 0 ? (
                <div className="text-center py-10">
                  <h2 className="text-xl font-semibold text-gray-700 mb-2">Welcome to EduBuddy!</h2>
                  <p className="text-gray-500 mb-4">
                    Ask me any educational question to get started. I'm here to help with subjects like
                    math, science, history, literature, and more.
                  </p>
                  <p className="text-sm text-gray-400">
                    Example: "Explain the process of photosynthesis" or "What are the key themes in Macbeth?"
                  </p>
                </div>
              ) : (
                <div className="mb-4">
                  <div className="flex justify-between items-center mb-4">
                    <h2 className="text-lg font-semibold">
                      {activeConversation?.title || 'Conversation'}
                    </h2>
                    <button
                      onClick={handleClearChat}
                      className="text-sm text-gray-500 hover:text-red-500"
                    >
                      Clear chat
                    </button>
                  </div>
                  <div className="space-y-4 max-h-[60vh] overflow-y-auto p-2">
                    {activeConversation?.messages.map((msg, idx) => (
                      <ChatMessage key={idx} message={msg} />
                    ))}
                  </div>
                </div>
              )}

              {error && <div className="text-red-500 text-sm mb-4">{error}</div>}

              {isLoading && (
                <div className="flex justify-center my-4">
                  <BeatLoader color="#4f46e5" size={10} />
                </div>
              )}

              <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
            </div>
          </div>
        </div>
      </div>
      
      {/* Overlay for mobile */}
      {isSidebarOpen && (
        <div 
          className="md:hidden fixed inset-0 bg-black bg-opacity-50 z-0"
          onClick={() => setIsSidebarOpen(false)}
        ></div>
      )}
    </>
  );
} 