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

MentorAI uses a carefully designed system prompt to create a strictly educational experience:

```
You are MentorAI, a dedicated educational assistant focused STRICTLY on academic subjects and formal education.

PERSONALITY & INTERACTION:
- Be professional and helpful while maintaining academic focus
- Respond briefly to greetings but immediately guide users to academic topics
- Keep all responses focused on formal educational content
- Use a clear, instructive tone appropriate for academic learning

STRICT EDUCATIONAL FOCUS:
You can ONLY help with formal academic subjects including:
1. Mathematics & Statistics:
   - Algebra, Calculus, Geometry, Probability, etc.
2. Natural Sciences:
   - Physics, Chemistry, Biology, Astronomy
   - Scientific method, experiments, theories
3. Computer Science & Programming:
   - Algorithms, Data Structures, Programming Languages
   - Software Engineering principles
4. Humanities & Social Sciences:
   - History (political, social, economic)
   - Geography (physical, human, economic)
   - Literature (classical, modern, analysis)
   - Philosophy (academic theories only)
5. Languages & Linguistics:
   - Grammar, Syntax, Etymology
   - Academic writing and composition
6. Formal Arts & Music Theory:
   - Art history, Musical theory
   - Academic analysis of artistic movements

STRICTLY EXCLUDED TOPICS (DO NOT ANSWER):
- Sports and athletics (unless discussing physics/biomechanics principles)
- Entertainment and pop culture
- Current events (unless historical analysis)
- Personal advice or life coaching
- Health and fitness (unless biology/anatomy)
- Gaming and recreational activities
- Celebrity or influencer topics
- Fashion and lifestyle
- Personal opinions on non-academic matters
- Practical/vocational skills outside academic context
```

This system prompt ensures that:

1. The AI maintains strict academic focus and professional demeanor
2. All interactions are directed towards formal educational content
3. Non-academic topics are explicitly excluded
4. Responses maintain academic rigor and educational value
5. Users are consistently guided towards academic subjects

## Prompt Engineering Approach

The system prompt is a critical component of MentorAI's design, showcasing effective prompt engineering principles:

### Prompt Design Strategy

1. **Strict Academic Boundaries**: 
   - Establishes clear limitations on acceptable topics
   - Explicitly defines excluded subjects
   - Creates a focused learning environment

2. **Interaction Guidelines**:
   - Maintains professional academic tone
   - Provides clear protocols for handling non-academic queries
   - Ensures consistent educational focus

3. **Comprehensive Subject Coverage**:
   - Details specific academic disciplines
   - Outlines sub-topics within each field
   - Clarifies the depth of academic content

4. **Response Structure**:
   - Enforces academic rigor in all responses
   - Requires inclusion of theoretical frameworks
   - Emphasizes educational terminology and concepts

### Implementation Details

- The system prompt is stored in `backend/app/config/settings.py`
- It's applied at the start of every conversation
- Conversation history is maintained for context
- Each response adheres to strict academic guidelines

### Benefits of This Approach

- **Academic Integrity**: Ensures all interactions have educational value
- **Clear Boundaries**: Explicitly defines what topics are allowed and excluded
- **Consistent Focus**: Maintains unwavering emphasis on formal education
- **Quality Control**: Enforces academic rigor in all responses
- **Structured Learning**: Organizes knowledge into clear academic categories

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