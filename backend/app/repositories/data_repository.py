"""
Data repository implementation.
"""
import pandas as pd
import numpy as np
from typing import List
from app.core.interfaces import IDataRepository
from app.core.config import Config


class DataRepository(IDataRepository):
    """Repository for handling data operations."""
    
    def __init__(self, config: Config):
        self._config = config
        self._datasets = {}
        self._load_datasets()
    
    def _load_datasets(self):
        """Load all datasets into memory."""
        for name, path in self._config.DATASETS.items():
            try:
                df = pd.read_csv(path, index_col=False)
                
                # Clean column names
                if df.columns[0].startswith("Unnamed") or df.columns[0] == "":
                    df.rename(columns={df.columns[0]: "movie"}, inplace=True)
                
                self._datasets[name] = df
            except Exception as e:
                print(f"Warning: Could not load dataset {name}: {e}")
    
    def get_dataset(self, name: str) -> pd.DataFrame:
        """Get dataset by name."""
        if name not in self._datasets:
            raise ValueError(f"Dataset '{name}' not found")
        return self._datasets[name].copy()
    
    def get_available_datasets(self) -> List[str]:
        """Get list of available dataset names."""
        return list(self._datasets.keys())
    
    def get_user_columns(self, dataset_name: str) -> List[str]:
        """Get user column names from dataset."""
        df = self.get_dataset(dataset_name)
        columns = df.columns.tolist()
        
        # Filter out non-user columns
        filtered = [col for col in columns if not col.lower().startswith("unnamed") 
                   and col.lower() != "movie"]
        
        return filtered
