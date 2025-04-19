# MentorAI

MentorAI is an AI-powered educational assistant that answers questions related to academics, including subjects like math, science, literature, history, and more.

![MentorAI Screenshot](https://mentor-ai-two.vercel.app/screenshot.png)

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
- ReDoc: http://localhost:8000/redoc

### Key Endpoints

- `GET /health`: Health check endpoint
- `GET /`: API root with welcome message
- `POST /education/ask`: Main endpoint to ask educational questions
  - Request body: `{ "question": "string" }`
  - Response: `{ "answer": "string" }`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

If you have any questions or feedback, please open an issue in the GitHub repository. 