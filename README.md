# MentorAI

MentorAI is an AI-powered educational assistant that answers questions related to academics, including subjects like math, science, literature, history, and more.

Live Demo: [https://mentor-ai-two.vercel.app/](https://mentor-ai-two.vercel.app/)

## Project Structure

The project is divided into two main parts:

- **Backend**: FastAPI application that handles question processing and AI integration
- **Frontend**: Next.js application that provides the user interface

## Features

- Educational Q&A capability
- Conversation history
- Markdown support for complex formatting of educational content
- Mobile-responsive design
- Interactive Swagger API documentation
- Educational-only responses with system prompt filtering

## How It Works

MentorAI uses a carefully designed system prompt to ensure the AI only responds to educational topics:

```
You are MentorAI, an AI-powered educational assistant designed to help students with their studies.
You can only answer questions related to educational topics like math, science, history, literature, 
languages, programming, and other academic subjects.

If a user asks a question that is not related to education or learning, politely decline to answer
and remind them that you are here to help with educational topics only.

Non-educational topics include but are not limited to: personal advice, political opinions, 
entertainment recommendations, jokes, legal or medical advice, or anything not typically taught 
in an academic setting.

Always provide informative, accurate, and educational responses that help users learn.
```

This system prompt is sent with every user question to guide the AI's responses. It ensures that:

1. The AI only answers questions related to academic subjects
2. Non-educational questions are politely declined
3. Responses are informative and educational in nature
4. The application stays focused on its core purpose of educational assistance

## Prompt Engineering Approach

The system prompt is a critical component of MentorAI's design, showcasing effective prompt engineering principles:

### Prompt Design Strategy

1. **Clear Role Definition**: The prompt immediately establishes the AI's identity as an "educational assistant" to set user expectations and frame all interactions within an educational context.

2. **Explicit Boundaries**: By listing allowed topics (math, science, history, etc.) and explicitly defining forbidden categories (personal advice, entertainment, etc.), the prompt creates clear guardrails for the AI's behavior.

3. **Action Instructions**: The prompt gives clear directives on how to handle non-educational queries - "politely decline to answer" - which provides the AI with specific behavioral guidance.

4. **Quality Guidelines**: The last line "Always provide informative, accurate, and educational responses" ensures responses maintain a consistent standard of quality and relevance.

### Implementation Details

- The system prompt is stored as a constant in `backend/app/config/settings.py`
- It's injected into every API request to the Google Gemini AI service
- The consistent application of this prompt across all interactions ensures a reliable user experience
- No user prompt can override these core instructions, maintaining the educational focus

### Benefits of This Approach

- **Focused Utility**: MentorAI maintains its specialized educational purpose rather than becoming a general-purpose chatbot
- **Appropriate Content**: Users receive academically appropriate responses, making it suitable for students of all ages
- **Consistent Experience**: The AI maintains a consistent tone and approach across all interactions
- **Reduced Misuse**: The clear boundaries help prevent the service from being used for generating inappropriate content

This prompt engineering approach exemplifies how well-designed system prompts can shape AI behavior to serve specific use cases effectively while maintaining appropriate boundaries.

## Technologies Used

### Backend
- FastAPI
- Python 3.9+
- Google Generative AI (Gemini)
- Pydantic
- Uvicorn

### Frontend
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Axios

## Installation and Setup

### Prerequisites
- Node.js 18+ 
- Python 3.9+
- npm or yarn
- Git

### Backend Setup

1. Clone the repository
   ```bash
   git clone <repository-url>
   cd MentorAI
   ```

2. Set up Python virtual environment
   ```bash
   cd backend
   python -m venv venv
   
   # Activate the virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables
   ```bash
   # Copy the example .env file
   cp .env.example .env
   
   # Edit the .env file and add your Google Gemini API key
   # GOOGLE_API_KEY=your_api_key_here
   ```

5. Run the backend server
   ```bash
   python run.py
   ```
   The API will be available at http://localhost:8000

### Frontend Setup

1. Move to the frontend directory
   ```bash
   cd ../frontend
   ```

2. Install dependencies
   ```bash
   npm install
   # or
   yarn install
   ```

3. Set up environment variables
   ```bash
   # Copy the example .env file
   cp .env.example .env.local
   
   # For local development, set the API URL to your local backend
   # NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   ```

4. Run the development server
   ```bash
   npm run dev
   # or
   yarn dev
   ```
   The frontend will be available at http://localhost:3000

## Deployment

### Backend Deployment

The backend can be deployed to any platform that supports Python applications:

#### Option 1: Deploying to a VPS or dedicated server

1. Set up a server with Python installed
2. Clone the repository and set up as in the local installation
3. Consider using Gunicorn as a production WSGI server:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
   ```
4. Set up Nginx as a reverse proxy (recommended)

#### Option 2: Deploying to a PaaS like Heroku

1. Create a Procfile:
   ```
   web: gunicorn app.main:app -k uvicorn.workers.UvicornWorker
   ```
2. Add your environment variables to the platform
3. Deploy according to the platform's instructions

### Frontend Deployment

The frontend is currently deployed to Vercel at [https://mentor-ai-two.vercel.app/](https://mentor-ai-two.vercel.app/)

#### Deploying to Vercel

1. Push your code to a GitHub repository
2. Connect your repository to Vercel
3. Set the following build settings:
   - Framework Preset: Next.js
   - Build Command: `npm run build` or `next build`
   - Output Directory: `.next`
4. Add the required environment variables
5. Deploy

## API Documentation

When running locally, the API documentation is available at:
- Swagger UI: http://localhost:8000/docs

The Swagger UI provides interactive documentation where you can:
- Browse all available API endpoints
- See request and response schemas with examples
- Test API endpoints directly from the browser
- Understand API capabilities and requirements

### Key Endpoints

- `GET /health`: Health check endpoint
- `GET /`: API root with welcome message
- `POST /education/ask`: Main endpoint to ask educational questions
  - Request body: `{ "question": "string" }`
  - Response: `{ "answer": "string" }`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

If you have any questions or feedback, please open an issue in the GitHub repository. 