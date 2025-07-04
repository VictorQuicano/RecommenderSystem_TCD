"""
Factory for creating distance calculator instances.
"""
from typing import Dict
from app.core.interfaces import IDistanceCalculator
from app.core.distance_calculators import (
    EuclideanDistanceCalculator,
    ManhattanDistanceCalculator,
    CosineDistanceCalculator,
    PearsonDistanceCalculator
)


class DistanceCalculatorFactory:
    """Factory for creating distance calculator instances."""
    
    def __init__(self):
        self._calculators: Dict[str, IDistanceCalculator] = {
            "euclidean": EuclideanDistanceCalculator(),
            "manhattan": ManhattanDistanceCalculator(),
            "cosine": CosineDistanceCalculator(),
            "pearson": PearsonDistanceCalculator(),
        }
    
    def get_calculator(self, metric: str) -> IDistanceCalculator:
        """Get distance calculator by metric name."""
        calculator = self._calculators.get(metric.lower())
        if calculator is None:
            raise ValueError(f"Unknown distance metric: {metric}")
        return calculator
    
    def get_available_metrics(self) -> list[str]:
        """Get list of available distance metrics."""
        return list(self._calculators.keys())
