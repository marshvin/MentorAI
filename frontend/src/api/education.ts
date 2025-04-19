import { apiClient } from './config';
import { AxiosError } from 'axios';

// Define types
export interface QuestionRequest {
  question: string;
}

export interface AnswerResponse {
  answer: string;
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
   * @returns Promise with the AI's answer
   * @throws ApiError with status code and error details
   */
  askQuestion: async (question: string): Promise<AnswerResponse> => {
    try {
      // Validate input on frontend before sending to backend
      if (!question || question.trim().length === 0) {
        throw new ApiError(
          'Question cannot be empty', 
          400, 
          'Please enter a valid question'
        );
      }
      
      // Send request to backend
      const response = await apiClient.post<AnswerResponse>('/education/ask', {
        question,
      });
      
      return response.data;
    } catch (error) {
      // Handle axios errors
      if (error instanceof AxiosError) {
        const status = error.response?.status || 500;
        const detail = error.response?.data?.detail || 'Unknown error occurred';
        
        // Handle different error types
        if (status === 400) {
          throw new ApiError('Invalid question format', status, detail);
        } else if (status === 422) {
          throw new ApiError('Invalid input data', status, detail);
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