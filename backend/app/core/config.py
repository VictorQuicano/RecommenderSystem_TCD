"""
Configuration settings for the application.
"""
from typing import Dict
import os


class Config:
    """Application configuration class."""
    
    # CORS settings
    CORS_ORIGINS = ["*"]  # In production, restrict to specific origins
    CORS_CREDENTIALS = True
    CORS_METHODS = ["*"]
    CORS_HEADERS = ["*"]
    
    # Data paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    DATA_DIR = BASE_DIR
    
    # Available datasets
    DATASETS = {
        "Movie_Ratings.csv": os.path.join(DATA_DIR, "Movie_Ratings.csv"),
        "Pelis_short.csv": os.path.join(DATA_DIR, "Pelis_short.csv"),
    }
    
    # Distance metrics configuration
    DISTANCE_METRICS = ["euclidean", "manhattan", "pearson", "cosine"]
    
    # API settings
    DEFAULT_DATASET = "Movie_Ratings.csv"
    MAX_K_NEIGHBORS = 50
    DEFAULT_K = 5
