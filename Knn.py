import pandas as pd
import math
import numpy as np

class KNNCalcularDistancia:
    def __init__(self, distance_function):
        self.distance_function = distance_function

    def calculate_distances(self, df: pd.DataFrame, target_column: str) -> pd.Series:
        if target_column not in df.columns:
            raise ValueError(f"La columna '{target_column}' no existe en el DataFrame")

        distances = {}
        target_series = pd.to_numeric(df[target_column], errors='coerce')

        for column in df.columns:
            if column == target_column:
                continue

            other_series = pd.to_numeric(df[column], errors='coerce')

            # Filtrar valores válidos (ambos no nulos)
            valid_pairs = [
                (x, y)
                for x, y in zip(target_series, other_series)
                if pd.notna(x) and pd.notna(y)
            ]
            if not valid_pairs:
                distances[column] = float('inf')  # o None
                continue

            values1, values2 = zip(*valid_pairs)
            try:
                distance = self.distance_function(list(values1), list(values2))
            except Exception:
                distance = float('inf')

            distances[column] = distance

        return pd.Series(distances).sort_values()

    def get_knn(self, df: pd.DataFrame, target_column: str, k: int = 5) -> list[dict]:
        distances = self.calculate_distances(df, target_column)
        knn = distances.head(k)

        return [
            {"neighbor": name, "distance": round(dist, 4)}
            for name, dist in knn.items()
            if not math.isinf(dist)
        ]