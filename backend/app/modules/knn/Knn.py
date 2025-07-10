import pandas as pd
import math
import numpy as np

from app.modules.distances.euclidean_distance import euclidean_distance
from app.modules.distances.manhattan_formulas import manhattan_distance
from app.modules.distances.cosine_similarity import cosine_similarity
from app.modules.distances.pearson import similitud_pearson

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
    
    def recommend(self, df: pd.DataFrame, target_column:str, neighbor:int=5, umbral:float=3.5)->list[dict]:
        # Paso 1: obtener KNN
        knn_df = self.get_knn(df, target_column, neighbor)

        neighbor_cols = [d['neighbor'] for d in knn_df]

        # Paso 2: identificar los índices donde el usuario no ha calificado (NaN)
        indices_nan = df[df[target_column].isna()].index

        recommendations = []

        for idx in indices_nan:
        # Calificaciones de neighbor en ese ítem
            neighbor_values = df.loc[idx, neighbor_cols]
            neighbor_values = neighbor_values.dropna()  # quitar NaNs

            if neighbor_values.empty:
                continue  # ningún neighbor calificó esta película

            promedio = neighbor_values.mean()

            if promedio >= umbral:
                # Construimos el dict del formato requerido
                recomendacion = {
                    'movie': idx,
                    'score': round(promedio, 3),
                    'neighbor': sorted(
                        [
                            {'name': neighbor, 'score': round(df.loc[idx, neighbor], 3)}
                            for neighbor in neighbor_values.index
                        ],
                        key=lambda x: x['score'],
                        reverse=True
                    )
                }
                recommendations.append(recomendacion)

        # Ordenar recommendations por score descendente
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations

distance_functions = {
    'euclidean': euclidean_distance,
    'manhattan': manhattan_distance,
    'pearson': similitud_pearson,
    'cosine': cosine_similarity
}

def validateFunction(distance_type:str = 'euclidian'):
    if distance_type not in distance_functions:
        raise ValueError(f"Tipo de distancia no válido. Opciones: {list(distance_functions.keys())}")

def find_knn_for_column(df: pd.DataFrame, target_column: str, distance_type='euclidean', k=5) -> list[dict]:

    validateFunction(distance_type)

    #df = df.apply(pd.to_numeric, errors='coerce')  # Convierte todo a numérico

    knn_calculator = KNNCalcularDistancia(distance_functions[distance_type])
    return knn_calculator.get_knn(df, target_column, k)

def recommend_for_column(df: pd.DataFrame, target_column:str, neighbor:int=5,distance_type='euclidean', umbral:float=3.5) -> list[dict]:

    validateFunction(distance_type)

    df = df.apply(pd.to_numeric, errors='coerce')  # Convierte todo a numérico
    print(df)

    knn_calculator = KNNCalcularDistancia(distance_functions[distance_type])
    return knn_calculator.recommend(df,target_column,neighbor, umbral)
