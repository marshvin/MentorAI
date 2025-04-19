import axios from 'axios';

// Validate and format the API URL
const getValidApiUrl = () => {
  const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
  
  if (!apiUrl) {
    // Fallback to window.location in production, or localhost in development
    if (process.env.NODE_ENV === 'production') {
      // In production, use the same domain as the frontend, but with the backend port
      const protocol = window.location.protocol;
      const hostname = window.location.hostname;
      return `${protocol}//${hostname}:8000`;
    } else {
      // In development, use localhost
      return 'http://localhost:8000';
    }
  }

  try {
    // Test if the URL is valid
    new URL(apiUrl);
    return apiUrl;
  } catch (e) {
    console.error('Invalid API URL:', apiUrl);
    // Return a fallback URL
    return process.env.NODE_ENV === 'production'
      ? `${window.location.protocol}//${window.location.hostname}:8000`
      : 'http://localhost:8000';
  }
};

// Create axios instance with base URL from environment variables
export const apiClient = axios.create({
  baseURL: getValidApiUrl(),
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for dynamic baseURL in production
apiClient.interceptors.request.use((config) => {
  if (process.env.NODE_ENV === 'production') {
    // Update baseURL dynamically in case window.location changed
    config.baseURL = getValidApiUrl();
  }
  return config;
});

// Add a response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Log errors in development
    if (process.env.NODE_ENV !== 'production') {
      console.error('API Error:', error.response || error);
    }
    return Promise.reject(error);
  }
); 