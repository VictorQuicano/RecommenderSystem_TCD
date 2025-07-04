"""
Matrix service implementation.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any
from app.core.interfaces import IMatrixService


class MatrixService(IMatrixService):
    """Service for matrix operations."""
    
    def get_matrix_data(self, dataset: pd.DataFrame) -> Dict[str, Any]:
        """Get matrix representation of dataset."""
        # Make a copy to avoid modifying original
        df = dataset.copy()
        
        # Ensure first column is movie names
        if df.columns[0].lower().startswith("unnamed") or df.columns[0] == "":
            df.rename(columns={df.columns[0]: "movie"}, inplace=True)
        
        # Extract movie names
        movies = df["movie"].tolist() if "movie" in df.columns else []
        
        # Clean numeric data
        df_clean = df.drop(columns=["movie"]) if "movie" in df.columns else df
        df_clean = df_clean.apply(pd.to_numeric, errors="coerce")
        df_clean = df_clean.replace([np.nan, np.inf, -np.inf], None)
        
        return {
            "columns": df_clean.columns.tolist(),
            "movies": movies,
            "data": df_clean.values.tolist()
        }
