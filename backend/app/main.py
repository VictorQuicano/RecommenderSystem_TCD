"""
Main FastAPI application module.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import data
from app.core.config import Config


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    config = Config()
    
    app = FastAPI(
        title="Recommender System API",
        description="API for movie recommendation system with KNN and distance metrics",
        version="2.0.0"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ORIGINS,
        allow_credentials=config.CORS_CREDENTIALS,
        allow_methods=config.CORS_METHODS,
        allow_headers=config.CORS_HEADERS,
    )
    
    # Include routers
    app.include_router(data.router, tags=["data"])
    
    return app


# Create the app instance
app = create_app()
