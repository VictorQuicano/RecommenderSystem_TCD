"""
KNN service implementation.
"""
import pandas as pd
import math
from typing import List, Dict, Any
from app.core.interfaces import IKnnService
from app.core.distance_factory import DistanceCalculatorFactory


class KnnService(IKnnService):
    """Service for K-Nearest Neighbors operations."""
    
    def __init__(self, distance_factory: DistanceCalculatorFactory):
        self._distance_factory = distance_factory
    
    def find_neighbors(self, dataset: pd.DataFrame, target_user: str, 
                      distance_metric: str, k: int) -> List[Dict[str, Any]]:
        """Find k nearest neighbors for a target user."""
        if target_user not in dataset.columns:
            raise ValueError(f"User '{target_user}' not found in dataset")
        
        calculator = self._distance_factory.get_calculator(distance_metric)
        distances = self._calculate_all_distances(dataset, target_user, calculator)
        
        # Sort distances and get top k
        sorted_distances = sorted(distances.items(), key=lambda x: x[1])
        
        # Filter out infinite distances and take top k
        valid_neighbors = [
            {"neighbor": name, "distance": round(dist, 4)}
            for name, dist in sorted_distances
            if not math.isinf(dist)
        ]
        
        return valid_neighbors[:k]
    
    def _calculate_all_distances(self, dataset: pd.DataFrame, target_user: str, calculator) -> Dict[str, float]:
        """Calculate distances from target user to all other users."""
        distances = {}
        target_series = pd.to_numeric(dataset[target_user], errors='coerce')
        
        for column in dataset.columns:
            if column == target_user or column.lower() in ["movie", "unnamed"]:
                continue
            
            other_series = pd.to_numeric(dataset[column], errors='coerce')
            
            # Get valid pairs (both not null)
            valid_pairs = [
                (x, y)
                for x, y in zip(target_series, other_series)
                if pd.notna(x) and pd.notna(y)
            ]
            
            if not valid_pairs:
                distances[column] = float('inf')
                continue
            
            values1, values2 = zip(*valid_pairs)
            
            try:
                distance = calculator.calculate(list(values1), list(values2))
                distances[column] = distance
            except Exception:
                distances[column] = float('inf')
        
        return distances
