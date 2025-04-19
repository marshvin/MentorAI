import { apiClient } from './config';

// Define types
export interface QuestionRequest {
  question: string;
}

export interface AnswerResponse {
  answer: string;
}

// API endpoints for educational services
export const educationApi = {
  /**
   * Ask a question to the AI educational assistant
   * @param question The question text
   * @returns Promise with the AI's answer
   */
  askQuestion: async (question: string): Promise<AnswerResponse> => {
    const response = await apiClient.post<AnswerResponse>('/education/ask', {
      question,
    });
    return response.data;
  },
}; 