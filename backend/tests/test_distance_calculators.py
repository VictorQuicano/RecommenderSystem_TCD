"""
Unit tests for distance calculators.
"""
import unittest
import math
from app.core.distance_calculators import (
    EuclideanDistanceCalculator,
    ManhattanDistanceCalculator,
    CosineDistanceCalculator,
    PearsonDistanceCalculator
)


class TestDistanceCalculators(unittest.TestCase):
    """Test cases for distance calculators."""
    
    def setUp(self):
        """Set up test data."""
        self.vector1 = [1.0, 2.0, 3.0, 4.0]
        self.vector2 = [2.0, 3.0, 4.0, 5.0]
        self.vector_with_nan = [1.0, float('nan'), 3.0, 4.0]
    
    def test_euclidean_distance(self):
        """Test Euclidean distance calculation."""
        calculator = EuclideanDistanceCalculator()
        result = calculator.calculate(self.vector1, self.vector2)
        expected = math.sqrt(4)  # sqrt((2-1)^2 + (3-2)^2 + (4-3)^2 + (5-4)^2)
        self.assertAlmostEqual(result, expected, places=4)
    
    def test_manhattan_distance(self):
        """Test Manhattan distance calculation."""
        calculator = ManhattanDistanceCalculator()
        result = calculator.calculate(self.vector1, self.vector2)
        expected = 4.0  # |2-1| + |3-2| + |4-3| + |5-4|
        self.assertAlmostEqual(result, expected, places=4)
    
    def test_cosine_similarity(self):
        """Test Cosine similarity calculation."""
        calculator = CosineDistanceCalculator()
        result = calculator.calculate(self.vector1, self.vector2)
        # Calculate expected manually
        dot_product = 1*2 + 2*3 + 3*4 + 4*5  # 2 + 6 + 12 + 20 = 40
        norm1 = math.sqrt(1 + 4 + 9 + 16)  # sqrt(30)
        norm2 = math.sqrt(4 + 9 + 16 + 25)  # sqrt(54)
        expected = dot_product / (norm1 * norm2)
        self.assertAlmostEqual(result, expected, places=4)
    
    def test_pearson_correlation(self):
        """Test Pearson correlation calculation."""
        calculator = PearsonDistanceCalculator()
        result = calculator.calculate(self.vector1, self.vector2)
        # For perfectly correlated vectors like [1,2,3,4] and [2,3,4,5], 
        # correlation should be 1.0
        self.assertAlmostEqual(result, 1.0, places=4)
    
    def test_distance_with_nan_values(self):
        """Test distance calculation with NaN values."""
        calculator = EuclideanDistanceCalculator()
        result = calculator.calculate(self.vector_with_nan, self.vector2)
        # Should ignore NaN values and calculate on valid pairs only
        # Valid pairs: (1,2), (3,4), (4,5)
        expected = math.sqrt((2-1)**2 + (4-3)**2 + (5-4)**2)  # sqrt(1+1+1) = sqrt(3)
        self.assertAlmostEqual(result, expected, places=4)


if __name__ == '__main__':
    unittest.main()
