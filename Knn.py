import pandas as pd
import math

class KNNCalcularDistancia:
    def __init__(self, distance_function):
        """
        Inicializa el calculador de KNN con una función de distancia.
        
        Parámetros:
        distance_function -- función de distancia a utilizar (euclidean, manhattan, pearson, cosine)
        """
        self.distance_function = distance_function
    
    def calculate_distances(self, df, target_column):
        """
        Calcula las distancias entre la columna objetivo y todas las demás columnas.
        
        Parámetros:
        df -- DataFrame de pandas
        target_column -- nombre de la columna objetivo (string)
        
        Retorna:
        Serie de pandas con las distancias ordenadas
        """
        if target_column not in df.columns:
            raise ValueError(f"La columna '{target_column}' no existe en el DataFrame")
            
        distances = {}
        target_series = df[target_column]
        
        for column in df.columns:
            if column == target_column:
                continue
                
            distance = self.distance_function(target_series.values, df[column].values)
            distances[column] = distance
        
        return pd.Series(distances).sort_values()
    
    def get_knn(self, df, target_column, k=5):
        """
        Obtiene los K vecinos más cercanos para la columna objetivo.
        
        Parámetros:
        df -- DataFrame de pandas
        target_column -- nombre de la columna objetivo (string)
        k -- número de vecinos a retornar (int)
        
        Retorna:
        DataFrame con los k vecinos más cercanos y sus distancias
        """
        distances = self.calculate_distances(df, target_column)
        return distances.head(k).to_frame(name='Distancia')