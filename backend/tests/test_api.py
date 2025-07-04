"""
Integration tests for API endpoints.
"""
import unittest
import pandas as pd
from fastapi.testclient import TestClient
from app.main import app


class TestAPIEndpoints(unittest.TestCase):
    """Test cases for API endpoints."""
    
    def setUp(self):
        """Set up test client."""
        self.client = TestClient(app)
        
        # Create sample test data
        self.sample_data = pd.DataFrame({
            'movie': ['Movie1', 'Movie2', 'Movie3'],
            'User1': [5.0, 4.0, 3.0],
            'User2': [4.0, 5.0, 2.0],
            'User3': [3.0, 4.0, 5.0]
        })
    
    def test_get_datasets(self):
        """Test getting available datasets."""
        response = self.client.get("/datasets")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
    
    def test_get_metrics(self):
        """Test getting available metrics."""
        response = self.client.get("/metrics")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        expected_metrics = ["euclidean", "manhattan", "cosine", "pearson"]
        for metric in expected_metrics:
            self.assertIn(metric, data)
    
    def test_compare_users_invalid_dataset(self):
        """Test comparing users with invalid dataset."""
        response = self.client.get(
            "/compare?u1=User1&u2=User2&metric=euclidean&dataset=nonexistent.csv"
        )
        self.assertEqual(response.status_code, 404)
    
    def test_compare_users_invalid_metric(self):
        """Test comparing users with invalid metric."""
        response = self.client.get(
            "/compare?u1=User1&u2=User2&metric=invalid&dataset=Movie_Ratings.csv"
        )
        self.assertEqual(response.status_code, 400)
    
    def test_knn_invalid_user(self):
        """Test KNN with invalid user."""
        response = self.client.get(
            "/knn?user=NonexistentUser&k=3&dataset=Movie_Ratings.csv&distance=euclidean"
        )
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
