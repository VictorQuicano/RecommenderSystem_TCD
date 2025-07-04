"""
Concrete implementations of distance calculators.
"""
import math
from typing import List
from app.core.interfaces import IDistanceCalculator


class EuclideanDistanceCalculator(IDistanceCalculator):
    """Euclidean distance implementation."""
    
    def calculate(self, vector1: List[float], vector2: List[float]) -> float:
        """Calculate Euclidean distance between two vectors."""
        squared_sum = 0
        for v1, v2 in zip(vector1, vector2):
            if not math.isnan(v1) and not math.isnan(v2):
                diff = v1 - v2
                squared_sum += diff * diff
        return math.sqrt(squared_sum)
    
    @property
    def name(self) -> str:
        return "euclidean"


class ManhattanDistanceCalculator(IDistanceCalculator):
    """Manhattan distance implementation."""
    
    def calculate(self, vector1: List[float], vector2: List[float]) -> float:
        """Calculate Manhattan distance between two vectors."""
        total_distance = 0
        for v1, v2 in zip(vector1, vector2):
            if not math.isnan(v1) and not math.isnan(v2):
                total_distance += abs(v1 - v2)
        return total_distance
    
    @property
    def name(self) -> str:
        return "manhattan"


class CosineDistanceCalculator(IDistanceCalculator):
    """Cosine similarity implementation."""
    
    def calculate(self, vector1: List[float], vector2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        dot_product = 0
        norm1 = 0
        norm2 = 0
        
        for v1, v2 in zip(vector1, vector2):
            if not math.isnan(v1) and not math.isnan(v2):
                dot_product += v1 * v2
                norm1 += v1 * v1
                norm2 += v2 * v2
        
        if norm1 == 0 or norm2 == 0:
            return 0
        
        return dot_product / (math.sqrt(norm1) * math.sqrt(norm2))
    
    @property
    def name(self) -> str:
        return "cosine"


class PearsonDistanceCalculator(IDistanceCalculator):
    """Pearson correlation coefficient implementation."""
    
    def calculate(self, vector1: List[float], vector2: List[float]) -> float:
        """Calculate Pearson correlation coefficient between two vectors."""
        # Filter out NaN values
        valid_pairs = [(v1, v2) for v1, v2 in zip(vector1, vector2) 
                      if not math.isnan(v1) and not math.isnan(v2)]
        
        if len(valid_pairs) < 2:
            return 0
        
        v1_values, v2_values = zip(*valid_pairs)
        n = len(v1_values)
        
        # Calculate means
        mean1 = sum(v1_values) / n
        mean2 = sum(v2_values) / n
        
        # Calculate numerator and denominators
        numerator = sum((v1 - mean1) * (v2 - mean2) for v1, v2 in valid_pairs)
        sum_sq1 = sum((v1 - mean1) ** 2 for v1 in v1_values)
        sum_sq2 = sum((v2 - mean2) ** 2 for v2 in v2_values)
        
        denominator = math.sqrt(sum_sq1 * sum_sq2)
        
        if denominator == 0:
            return 0
        
        return numerator / denominator
    
    @property
    def name(self) -> str:
        return "pearson"
