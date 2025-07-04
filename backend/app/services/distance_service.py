"""
Distance service implementation.
"""
import pandas as pd
from typing import List
from app.core.interfaces import IDistanceService
from app.core.distance_factory import DistanceCalculatorFactory


class DistanceService(IDistanceService):
    """Service for distance calculations between users."""
    
    def __init__(self, distance_factory: DistanceCalculatorFactory):
        self._distance_factory = distance_factory
    
    def calculate_distance(self, dataset: pd.DataFrame, user1: str, 
                          user2: str, metric: str) -> float:
        """Calculate distance between two users."""
        if user1 not in dataset.columns or user2 not in dataset.columns:
            raise ValueError(f"One or both users not found in dataset")
        
        calculator = self._distance_factory.get_calculator(metric)
        
        # Get series for both users
        series1 = dataset[user1]
        series2 = dataset[user2]
        
        # Create mask for valid (non-null) values
        mask = series1.notna() & series2.notna()
        
        # Extract valid values
        v1 = series1[mask].tolist()
        v2 = series2[mask].tolist()
        
        if not v1 or not v2:
            return float('inf')
        
        try:
            distance = calculator.calculate(v1, v2)
            return round(distance, 4)
        except Exception:
            return float('inf')
    
    def get_available_metrics(self) -> List[str]:
        """Get list of available distance metrics."""
        return self._distance_factory.get_available_metrics()
