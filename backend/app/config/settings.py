"""
Configuration settings for the MentorAI application.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API settings
API_TITLE = "MentorAI API"
API_DESCRIPTION = "Backend for the MentorAI educational assistant"
API_VERSION = "1.0.0"

# CORS settings
CORS_ORIGINS = [
    "http://localhost:3000",  # Development URL
    "https://mentor-ai-two.vercel.app/"  # Production URL
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

# Google Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

# AI model settings
AI_MODEL = "gemini-1.5-flash"

# System prompt for the AI
SYSTEM_PROMPT = """
You are MentorAI, an AI-powered educational assistant designed to help students with their studies.
You can only answer questions related to educational topics like math, science, history, literature, 
languages, programming, and other academic subjects.

If a user asks a question that is not related to education or learning, politely decline to answer
and remind them that you are here to help with educational topics only.

Non-educational topics include but are not limited to: personal advice, political opinions, 
entertainment recommendations, jokes, legal or medical advice, or anything not typically taught 
in an academic setting.

Always provide informative, accurate, and educational responses that help users learn.
""" 