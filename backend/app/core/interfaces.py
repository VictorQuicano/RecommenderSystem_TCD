"""
Core interfaces and abstractions for the recommender system.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import pandas as pd


class IDistanceCalculator(ABC):
    """Interface for distance calculation strategies."""
    
    @abstractmethod
    def calculate(self, vector1: List[float], vector2: List[float]) -> float:
        """Calculate distance between two vectors."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the distance metric."""
        pass


class IDataRepository(ABC):
    """Interface for data access operations."""
    
    @abstractmethod
    def get_dataset(self, name: str) -> pd.DataFrame:
        """Get dataset by name."""
        pass
    
    @abstractmethod
    def get_available_datasets(self) -> List[str]:
        """Get list of available dataset names."""
        pass
    
    @abstractmethod
    def get_user_columns(self, dataset_name: str) -> List[str]:
        """Get user column names from dataset."""
        pass


class IKnnService(ABC):
    """Interface for KNN service operations."""
    
    @abstractmethod
    def find_neighbors(self, dataset: pd.DataFrame, target_user: str, 
                      distance_metric: str, k: int) -> List[Dict[str, Any]]:
        """Find k nearest neighbors for a target user."""
        pass


class IDistanceService(ABC):
    """Interface for distance service operations."""
    
    @abstractmethod
    def calculate_distance(self, dataset: pd.DataFrame, user1: str, 
                          user2: str, metric: str) -> float:
        """Calculate distance between two users."""
        pass
    
    @abstractmethod
    def get_available_metrics(self) -> List[str]:
        """Get list of available distance metrics."""
        pass


class IMatrixService(ABC):
    """Interface for matrix service operations."""
    
    @abstractmethod
    def get_matrix_data(self, dataset: pd.DataFrame) -> Dict[str, Any]:
        """Get matrix representation of dataset."""
        pass
