import pickle
import time
import numpy as np
import pandas as pd
from scipy.sparse import load_npz, vstack, csr_matrix
from sklearn.neighbors import NearestNeighbors


class MovieRecommendationSystem:
    """
    Sistema de recomendación de películas basado en filtrado colaborativo
    usando diferentes métricas de distancia con K-Nearest Neighbors.
    """
    
    def __init__(self, path="./data/processed"):
        """
        Inicializa el sistema de recomendación cargando datos y entrenando modelos.
        
        Args:
            path (str): Ruta a los archivos de datos procesados
        """
        self.path = path
        self.metrics = ['cosine', 'euclidean', 'manhattan']
        self.models = {}
        self.training_times = {}
        
        # Cargar datos
        self._load_data()
        
        # Entrenar modelos con diferentes métricas
        self._train_models()
    
    def _load_data(self):
        """Carga la matriz de ratings, mapeos y DataFrame de películas."""
        # Cargar matriz CSR
        self.ratings_csr = load_npz(f"{self.path}/ratings_csr.npz")
        
        # Cargar mapeos
        with open(f"{self.path}/mappers.pkl", "rb") as f:
            data = pickle.load(f)
            self.user_mapper = data["user_mapper"]
            self.movie_mapper = data["movie_mapper"]
            self.reverse_movie_mapper = data["reverse_movie_mapper"]
        
        # Cargar DataFrame de películas
        self.df_movies = pd.read_csv(f"{self.path}/movies_bayesian.csv")
    
    def _train_models(self):
        """Entrena modelos KNN con diferentes métricas."""
        for metric in self.metrics:
            start_time = time.time()
            
            model = NearestNeighbors(
                metric=metric,
                algorithm='brute',
                n_neighbors=5,
                n_jobs=-1
            )
            model.fit(self.ratings_csr)
            
            end_time = time.time()
            training_time = end_time - start_time
            
            self.models[metric] = model
            self.training_times[metric] = training_time
    
    def info(self):
        """
        Retorna información sobre el sistema: métricas, tiempos de entrenamiento y tamaños de datos.
        
        Returns:
            dict: Información del sistema
        """
        info_dict = {
            'metrics': self.metrics,
            'training_times': self.training_times.copy(),
            'dataset_info': {
                'num_users': self.ratings_csr.shape[0],
                'num_movies': self.ratings_csr.shape[1],
                'num_ratings': self.ratings_csr.nnz,
                'sparsity': 1 - (self.ratings_csr.nnz / (self.ratings_csr.shape[0] * self.ratings_csr.shape[1]))
            },
            'models_info': {
                metric: {
                    'n_neighbors': model.n_neighbors,
                    'algorithm': model.algorithm,
                    'metric': model.metric
                } for metric, model in self.models.items()
            }
        }
        return info_dict
    
    def obtener_vecinos(self, user_id, metric='cosine', k=5):
        """
        Obtiene los k vecinos más similares a un usuario usando la métrica especificada.
        
        Args:
            user_id (int): ID del usuario (índice en la matriz)
            metric (str): Métrica a usar ('cosine', 'euclidean', 'manhattan')
            k (int): Número de vecinos a retornar
            
        Returns:
            tuple: (distancias, indices) de los vecinos más similares
        """
        if metric not in self.models:
            raise ValueError(f"Métrica '{metric}' no disponible. Opciones: {self.metrics}")
        
        model = self.models[metric]
        # Temporalmente cambiar n_neighbors si es necesario
        if k != model.n_neighbors:
            temp_model = NearestNeighbors(
                metric=metric,
                algorithm='brute',
                n_neighbors=k,
                n_jobs=-1
            )
            temp_model.fit(self.ratings_csr)
            distancias, indices = temp_model.kneighbors(self.ratings_csr[user_id])
        else:
            distancias, indices = model.kneighbors(self.ratings_csr[user_id])
        
        return distancias[0], indices[0]
    
    def agregar_o_actualizar_usuario(self, nuevas_valoraciones, user_id=None):
        """
        Agrega un nuevo usuario o actualiza uno existente y reentrena todos los modelos.
        
        Args:
            nuevas_valoraciones (dict): {movieId: rating}
            user_id (int, optional): ID del usuario a actualizar. None para nuevo usuario.
            
        Returns:
            tuple: (updated_ratings_csr, user_id, training_times_dict)
        """
        num_peliculas = self.ratings_csr.shape[1]
        nueva_fila = np.zeros(num_peliculas)
        
        # Crear vector de ratings
        for mid, rating in nuevas_valoraciones.items():
            if mid in self.movie_mapper:
                col_idx = self.movie_mapper[mid]
                nueva_fila[col_idx] = rating
        
        nueva_fila_sparse = csr_matrix(nueva_fila)
        
        # Actualizar matriz
        if user_id is None:
            # Crear nuevo usuario
            self.ratings_csr = vstack([self.ratings_csr, nueva_fila_sparse])
            user_id = self.ratings_csr.shape[0] - 1
        else:
            # Actualizar usuario existente
            self.ratings_csr[user_id] = nueva_fila_sparse
        
        # Reentrenar todos los modelos y medir tiempos
        new_training_times = {}
        for metric in self.metrics:
            start_time = time.time()
            
            model = NearestNeighbors(
                metric=metric,
                algorithm='brute',
                n_neighbors=5,
                n_jobs=-1
            )
            model.fit(self.ratings_csr)
            
            end_time = time.time()
            training_time = end_time - start_time
            
            self.models[metric] = model
            new_training_times[metric] = training_time
        
        self.training_times = new_training_times
        
        return self.ratings_csr, user_id, new_training_times
    
    def recomendar_peliculas(self, user_id, metric='cosine', top_k=5, top_n=10):
        """
        Recomienda películas basándose en usuarios similares usando la métrica especificada.
        
        Args:
            user_id (int): ID del usuario
            metric (str): Métrica a usar para encontrar vecinos
            top_k (int): Número de vecinos a considerar
            top_n (int): Número de recomendaciones a retornar
            
        Returns:
            list: Lista de tuplas (movie_id, title, bayesian_rating)
        """
        # Obtener vecinos
        distancias, vecinos = self.obtener_vecinos(user_id, metric, top_k)
        vecinos = [v for v in vecinos if v != user_id]
        
        # Obtener películas vistas por el usuario
        user_ratings = self.ratings_csr[user_id].toarray().flatten()
        peliculas_vistas = set(np.where(user_ratings > 0)[0])
        
        # Sumar ratings de vecinos por película
        scores = {}
        for vecino_id in vecinos:
            vecino_ratings = self.ratings_csr[vecino_id].toarray().flatten()
            for idx, rating in enumerate(vecino_ratings):
                if rating > 0 and idx not in peliculas_vistas:
                    scores[idx] = scores.get(idx, []) + [rating]
        
        # Obtener promedio de cada película recomendada
        scores_avg = [(idx, np.mean(ratings)) for idx, ratings in scores.items()]
        
        # Ordenar según bayesian_rating
        def get_bayesian(idx):
            movie_id = self.reverse_movie_mapper[idx]
            row = self.df_movies[self.df_movies["movieId"] == movie_id]
            return row["bayesian_rating"].values[0] if not row.empty and "bayesian_rating" in row.columns else 0
        
        scores_avg.sort(key=lambda x: get_bayesian(x[0]), reverse=True)
        
        # Traducir a títulos
        recomendaciones = []
        for idx, _ in scores_avg[:top_n]:
            movie_id = self.reverse_movie_mapper[idx]
            row = self.df_movies[self.df_movies["movieId"] == movie_id]
            if not row.empty:
                row = row.iloc[0]
                bayesian_rating = row.get("bayesian_rating", np.nan)
                recomendaciones.append((movie_id, row["title"], bayesian_rating))
        
        return recomendaciones
    
    def recomendar_por_genero(self, user_id, genero_objetivo, metric='cosine', top_k=5, top_n=10):
        """
        Recomienda películas de un género específico basándose en usuarios similares.
        
        Args:
            user_id (int): ID del usuario
            genero_objetivo (str): Género objetivo (ej: 'Action', 'Comedy')
            metric (str): Métrica a usar para encontrar vecinos
            top_k (int): Número de vecinos a considerar
            top_n (int): Número de recomendaciones a retornar
            
        Returns:
            list: Lista de tuplas (movie_id, title, genres, bayesian_rating)
        """
        # Obtener vecinos
        distancias, vecinos = self.obtener_vecinos(user_id, metric, top_k)
        vecinos = [v for v in vecinos if v != user_id]
        
        # Películas vistas por el usuario
        user_ratings = self.ratings_csr[user_id].toarray().flatten()
        peliculas_vistas = set(np.where(user_ratings > 0)[0])
        
        # Obtener películas candidatas de vecinos que no haya visto
        scores = {}
        for vecino_id in vecinos:
            vecino_ratings = self.ratings_csr[vecino_id].toarray().flatten()
            for idx, rating in enumerate(vecino_ratings):
                if rating > 0 and idx not in peliculas_vistas:
                    movie_id = self.reverse_movie_mapper[idx]
                    row = self.df_movies[self.df_movies["movieId"] == movie_id]
                    if not row.empty and genero_objetivo in row["genres"].values[0].split('|'):
                        scores[idx] = scores.get(idx, []) + [rating]
        
        if not scores:
            return []
        
        # Promedio por película
        scores_avg = [(idx, np.mean(ratings)) for idx, ratings in scores.items()]
        
        # Ordenar por bayesian_rating
        def get_bayesian(idx):
            movie_id = self.reverse_movie_mapper[idx]
            row = self.df_movies[self.df_movies["movieId"] == movie_id]
            return row["bayesian_rating"].values[0] if not row.empty and "bayesian_rating" in row.columns else 0
        
        scores_avg.sort(key=lambda x: get_bayesian(x[0]), reverse=True)
        
        # Retornar recomendaciones
        recomendaciones = []
        for idx, _ in scores_avg[:top_n]:
            movie_id = self.reverse_movie_mapper[idx]
            row = self.df_movies[self.df_movies["movieId"] == movie_id]
            if not row.empty:
                row = row.iloc[0]
                bayesian_rating = row.get("bayesian_rating", np.nan)
                recomendaciones.append((movie_id, row["title"], row["genres"], bayesian_rating))
        
        return recomendaciones

