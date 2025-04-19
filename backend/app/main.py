"""
Main FastAPI application initialization.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.api import api_router
from app.config.settings import (
    API_TITLE,
    API_DESCRIPTION,
    API_VERSION,
    API_DOCS_URL,
    API_REDOC_URL,
    CORS_ORIGINS,
    CORS_ALLOW_CREDENTIALS,
    CORS_ALLOW_METHODS,
    CORS_ALLOW_HEADERS
)

# Define tags metadata for Swagger UI
tags_metadata = [
    {
        "name": "education",
        "description": "Educational question answering endpoints",
    },
    {
        "name": "health",
        "description": "Health check endpoints for monitoring service status",
    },
]

def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: The configured FastAPI application
    """
    # Initialize FastAPI app with metadata
    application = FastAPI(
        title=API_TITLE,
        description=API_DESCRIPTION,
        version=API_VERSION,
        docs_url=API_DOCS_URL,
        redoc_url=API_REDOC_URL,
        openapi_tags=tags_metadata
    )
    
    # Setup CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=CORS_ALLOW_CREDENTIALS,
        allow_methods=CORS_ALLOW_METHODS,
        allow_headers=CORS_ALLOW_HEADERS,
    )
    
    # Include API router
    application.include_router(api_router)
    
    return application

# Create the application instance
app = create_application() 