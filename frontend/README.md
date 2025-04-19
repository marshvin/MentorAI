# MentorAI Frontend

MentorAI is an AI-powered educational assistant that helps answer educational questions.

## Getting Started

1. Copy the environment variables:
   ```bash
   cp .env.example .env.local
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## API Structure

The application follows a clean API layer pattern:

- `src/api/config.ts` - API client configuration with environment variables
- `src/api/education.ts` - Educational service API endpoints
- `src/api/index.ts` - API exports for easy importing

This structure allows for:
- Clear separation of API logic from UI components
- Type-safe API requests and responses
- Centralized error handling
- Easy configuration through environment variables

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| NEXT_PUBLIC_API_BASE_URL | Base URL for the backend API | http://localhost:8000 |

## Features

- Ask educational questions and get AI-powered answers
- Markdown formatting for AI responses
- Conversation history with persistence
- Mobile-responsive design 