# MentorAI

An AI-powered educational assistant that helps users ask and get answers to study-related questions.

## Features

- Clean, modern UI with Next.js and Tailwind CSS
- FastAPI backend for handling requests
- Google Gemini AI integration for educational responses
- Educational-only responses with system prompt filtering
- Conversation history stored in local storage
- Responsive design

## Project Structure

```
MentorAI/
├── frontend/           # Next.js frontend
│   ├── src/
│   │   ├── app/        # Next.js app directory
│   │   ├── components/ # React components
│   └── ... (Next.js config files)
└── backend/            # FastAPI backend
    ├── main.py         # Main FastAPI application
    ├── requirements.txt # Python dependencies
    └── .env.example    # Example environment file
```

## Prerequisites

- Node.js (v16+)
- Python (v3.8+)
- Google Gemini API key

## Setup and Installation

### Frontend Setup

1. Install dependencies:
   ```
   cd frontend
   npm install
   ```

2. Start the development server:
   ```
   npm run dev
   ```

3. The frontend will be available at `http://localhost:3000`

### Backend Setup

1. Create a virtual environment (optional but recommended):
   ```
   cd backend
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your Google Gemini API key:
   - Rename `.env.example` to `.env`
   - Get a Gemini API key from https://makersuite.google.com/app/apikey
   - Add your key to the `.env` file

5. Start the backend server:
   ```
   python main.py
   ```

6. The API will be available at `http://localhost:8000`

## Usage

1. Start both the frontend and backend servers
2. Open your browser to `http://localhost:3000`
3. Ask educational questions in the input field
4. Receive answers from the AI assistant

## API Endpoints

- `GET /` - Health check endpoint
- `POST /ask` - Send a question and receive an AI-generated answer

## License

MIT 