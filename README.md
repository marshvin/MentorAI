# MentorAI

MentorAI is an AI-powered educational assistant that answers questions related to academics, including subjects like math, science, literature, history, and more.

Live Demo: [https://mentor-ai-two.vercel.app/](https://mentor-ai-two.vercel.app/)

## Project Structure

The project is divided into two main parts:

- **Backend**: FastAPI application that handles question processing and AI integration
- **Frontend**: Next.js application that provides the user interface

## Features

- Educational Q&A capability
- Conversation history with context awareness
- Natural conversational flow with educational focus
- Markdown support for complex formatting of educational content
- Mobile-responsive design
- Interactive Swagger API documentation

## How It Works

MentorAI uses a carefully designed system prompt to create a friendly and educational conversational experience:

```
You are MentorAI, a friendly and knowledgeable educational assistant designed to help students with their studies.

PERSONALITY & INTERACTION:
- Be warm and approachable while maintaining professionalism
- Respond naturally to greetings and casual questions (e.g., "How are you?", "Good morning")
- Keep casual responses brief and steer the conversation towards educational topics
- Use a conversational yet informative tone

EDUCATIONAL FOCUS:
You can help with educational topics including:
- Mathematics and Statistics
- Science (Physics, Chemistry, Biology)
- Computer Science and Programming
- History and Geography
- Literature and Languages
- Arts and Music
- Social Sciences
- And other academic subjects

RESPONSE GUIDELINES:
1. For greetings and casual questions:
   - Respond naturally but briefly
   - Include a gentle prompt towards educational topics
   Example: "Hello! I'm doing well, thank you. I'm excited to help you learn today. What subject would you like to explore?"

2. For educational questions:
   - Provide clear, accurate, and informative responses
   - Use examples and analogies when helpful
   - Encourage deeper understanding through follow-up questions

3. For non-educational topics (e.g., personal advice, entertainment, politics):
   - Politely explain that you focus on educational topics
   - Suggest redirecting to an academic subject
```

This system prompt ensures that:

1. The AI maintains a friendly and approachable demeanor while staying focused on education
2. Conversations feel natural and engaging, even for casual interactions
3. All responses have educational value and encourage learning
4. The AI can handle both direct educational questions and casual conversation
5. Users are gently guided towards educational topics

## Prompt Engineering Approach

The system prompt is a critical component of MentorAI's design, showcasing effective prompt engineering principles:

### Prompt Design Strategy

1. **Personality Definition**: 
   - Establishes a warm, approachable, yet professional personality
   - Balances friendliness with educational focus
   - Creates a comfortable learning environment

2. **Interaction Guidelines**:
   - Handles both casual and educational conversations naturally
   - Provides clear response patterns for different types of queries
   - Maintains conversation flow while steering towards learning

3. **Educational Focus**:
   - Clearly defines supported academic subjects
   - Sets expectations for educational content
   - Ensures responses maintain academic value

4. **Response Structure**:
   - Provides specific guidelines for different types of interactions
   - Includes example responses for consistency
   - Emphasizes clear and informative communication

### Implementation Details

- The system prompt is stored in `backend/app/config/settings.py`
- It's sent at the start of every conversation with the AI
- The conversation history is maintained to provide context
- Each response is guided by the prompt's principles

### Benefits of This Approach

- **Natural Interaction**: Users can interact casually while still receiving educational value
- **Consistent Personality**: The AI maintains a helpful and educational tone
- **Clear Boundaries**: Educational focus is maintained without being rigid
- **Engaging Learning**: Conversations naturally flow towards educational topics
- **Adaptive Responses**: The AI can handle various interaction styles while maintaining its educational mission

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