import { apiClient } from './config';
import { AxiosError } from 'axios';

// Define types
export interface QuestionRequest {
  question: string;
  conversation_id?: string;
}

export interface AnswerResponse {
  answer: string;
  conversation_id: string;
  error?: string;
}

export interface ApiErrorResponse {
  detail: string;
  status?: number;
}

export class ApiError extends Error {
  status: number;
  detail: string;

  constructor(message: string, status: number, detail?: string) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.detail = detail || message;
  }
}

// API endpoints for educational services
export const educationApi = {
  /**
   * Ask a question to the AI educational assistant
   * @param question The question text
   * @param conversationId Optional conversation ID for context
   * @returns Promise with the AI's answer and conversation ID
   * @throws ApiError with status code and error details
   */
  askQuestion: async (question: string, conversationId?: string): Promise<AnswerResponse> => {
    try {
      // Basic validation - only check if empty or too long
      if (!question || question.trim().length === 0) {
        throw new ApiError(
          'Question cannot be empty', 
          400, 
          'Please enter a question'
        );
      }
      
      if (question.length > 1000) {
        throw new ApiError(
          'Question too long',
          400,
          'Please enter a question shorter than 1000 characters'
        );
      }
      
      // Prepare request data
      const requestData: QuestionRequest = {
        question
      };
      
      // Add conversation_id if it exists
      if (conversationId) {
        requestData.conversation_id = conversationId;
      }
      
      // Send request to backend
      const response = await apiClient.post<AnswerResponse>('/education/ask', requestData);
      
      return response.data;
    } catch (error) {
      // Handle axios errors
      if (error instanceof AxiosError) {
        const status = error.response?.status || 500;
        const detail = error.response?.data?.detail || 'Unknown error occurred';
        
        // Handle different error types
        if (status === 400) {
          throw new ApiError('Invalid question', status, detail);
        } else if (status === 422) {
          throw new ApiError('Invalid input format', status, detail);
        } else if (status === 503) {
          throw new ApiError('AI service unavailable', status, detail);
        } else {
          throw new ApiError('Error processing request', status, detail);
        }
      }
      
      // Rethrow if not an axios error
      throw error instanceof ApiError 
        ? error 
        : new ApiError('Unknown error occurred', 500, 'An unexpected error occurred');
    }
  },
}; 