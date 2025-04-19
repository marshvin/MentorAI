import { apiClient } from './config';
import { educationApi } from './education';

// Export everything from the API modules
export { apiClient, educationApi };

// Re-export types
export type { QuestionRequest, AnswerResponse } from './education'; 