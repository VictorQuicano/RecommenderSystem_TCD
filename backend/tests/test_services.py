"""
Unit tests for services.
"""
import unittest
import pandas as pd
from unittest.mock import Mock
from app.services.knn_service import KnnService
from app.services.distance_service import DistanceService
from app.services.matrix_service import MatrixService
from app.core.distance_factory import DistanceCalculatorFactory


class TestKnnService(unittest.TestCase):
    """Test cases for KNN service."""
    
    def setUp(self):
        """Set up test data."""
        self.distance_factory = DistanceCalculatorFactory()
        self.knn_service = KnnService(self.distance_factory)
        
        # Create sample DataFrame
        self.sample_df = pd.DataFrame({
            'movie': ['Movie1', 'Movie2', 'Movie3'],
            'User1': [5.0, 4.0, 3.0],
            'User2': [4.0, 5.0, 2.0],
            'User3': [3.0, 4.0, 5.0]
        })
    
    def test_find_neighbors_valid_user(self):
        """Test finding neighbors for valid user."""
        neighbors = self.knn_service.find_neighbors(
            self.sample_df, 'User1', 'euclidean', 2
        )
        self.assertIsInstance(neighbors, list)
        self.assertLessEqual(len(neighbors), 2)
        
        # Check structure of returned neighbors
        for neighbor in neighbors:
            self.assertIn('neighbor', neighbor)
            self.assertIn('distance', neighbor)
    
    def test_find_neighbors_invalid_user(self):
        """Test finding neighbors for invalid user."""
        with self.assertRaises(ValueError):
            self.knn_service.find_neighbors(
                self.sample_df, 'NonexistentUser', 'euclidean', 2
            )


class TestDistanceService(unittest.TestCase):
    """Test cases for distance service."""
    
    def setUp(self):
        """Set up test data."""
        self.distance_factory = DistanceCalculatorFactory()
        self.distance_service = DistanceService(self.distance_factory)
        
        # Create sample DataFrame
        self.sample_df = pd.DataFrame({
            'movie': ['Movie1', 'Movie2', 'Movie3'],
            'User1': [5.0, 4.0, 3.0],
            'User2': [4.0, 5.0, 2.0],
            'User3': [3.0, 4.0, 5.0]
        })
    
    def test_calculate_distance_valid_users(self):
        """Test calculating distance between valid users."""
        distance = self.distance_service.calculate_distance(
            self.sample_df, 'User1', 'User2', 'euclidean'
        )
        self.assertIsInstance(distance, float)
        self.assertGreaterEqual(distance, 0)
    
    def test_calculate_distance_invalid_users(self):
        """Test calculating distance with invalid users."""
        with self.assertRaises(ValueError):
            self.distance_service.calculate_distance(
                self.sample_df, 'User1', 'NonexistentUser', 'euclidean'
            )
    
    def test_get_available_metrics(self):
        """Test getting available metrics."""
        metrics = self.distance_service.get_available_metrics()
        self.assertIsInstance(metrics, list)
        expected_metrics = ["euclidean", "manhattan", "cosine", "pearson"]
        for metric in expected_metrics:
            self.assertIn(metric, metrics)


class TestMatrixService(unittest.TestCase):
    """Test cases for matrix service."""
    
    def setUp(self):
        """Set up test data."""
        self.matrix_service = MatrixService()
        
        # Create sample DataFrame
        self.sample_df = pd.DataFrame({
            'movie': ['Movie1', 'Movie2', 'Movie3'],
            'User1': [5.0, 4.0, 3.0],
            'User2': [4.0, 5.0, 2.0],
            'User3': [3.0, 4.0, 5.0]
        })
    
    def test_get_matrix_data(self):
        """Test getting matrix data."""
        matrix_data = self.matrix_service.get_matrix_data(self.sample_df)
        
        self.assertIsInstance(matrix_data, dict)
        self.assertIn('columns', matrix_data)
        self.assertIn('movies', matrix_data)
        self.assertIn('data', matrix_data)
        
        # Check structure
        self.assertIsInstance(matrix_data['columns'], list)
        self.assertIsInstance(matrix_data['movies'], list)
        self.assertIsInstance(matrix_data['data'], list)


if __name__ == '__main__':
    unittest.main()
