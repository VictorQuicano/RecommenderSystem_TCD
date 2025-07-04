"""
Enumerations for the application.
"""
from enum import Enum


class DistanceMetric(Enum):
    """Available distance metrics."""
    EUCLIDEAN = "euclidean"
    MANHATTAN = "manhattan"
    COSINE = "cosine"
    PEARSON = "pearson"


class DatasetName(Enum):
    """Available datasets."""
    MOVIE_RATINGS = "Movie_Ratings.csv"
    PELIS_SHORT = "Pelis_short.csv"
