import pickle
import time
import os
import sys
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
    
    def _get_object_size_mb(self, obj):
        """Calcula el tamaño en MB de un objeto en memoria."""
        return sys.getsizeof(obj) / (1024 * 1024)
    
    def _get_file_size_mb(self, filepath):
        """Calcula el tamaño en MB de un archivo en disco."""
        try:
            return os.path.getsize(filepath) / (1024 * 1024)
        except FileNotFoundError:
            return 0
    
    def _get_deep_size_mb(self, obj):
        """Calcula el tamaño aproximado en MB incluyendo objetos anidados."""
        size = sys.getsizeof(obj)
        
        if isinstance(obj, dict):
            size += sum(sys.getsizeof(k) + sys.getsizeof(v) for k, v in obj.items())
        elif isinstance(obj, (list, tuple)):
            size += sum(sys.getsizeof(item) for item in obj)
        elif hasattr(obj, '__dict__'):
            size += sum(sys.getsizeof(k) + sys.getsizeof(v) for k, v in obj.__dict__.items())
        
        return size / (1024 * 1024)
    
    def info(self):
        """
        Retorna información completa sobre el sistema: métricas, tiempos de entrenamiento,
        tamaños de datos en memoria y en disco.
        
        Returns:
            dict: Información detallada del sistema
        """
        # Información básica
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
        
        # Información de memoria RAM (en MB)
        memory_info = {
            'ratings_csr_mb': self._get_object_size_mb(self.ratings_csr),
            'user_mapper_mb': self._get_deep_size_mb(self.user_mapper),
            'movie_mapper_mb': self._get_deep_size_mb(self.movie_mapper),
            'reverse_movie_mapper_mb': self._get_deep_size_mb(self.reverse_movie_mapper),
            'df_movies_mb': self.df_movies.memory_usage(deep=True).sum() / (1024 * 1024),
            'models_mb': {
                metric: self._get_deep_size_mb(model) for metric, model in self.models.items()
            }
        }
        
        # Calcular total de RAM de modelos
        total_models_mb = sum(memory_info['models_mb'].values())
        memory_info['total_models_mb'] = total_models_mb
        
        # Calcular total de RAM del sistema
        total_system_mb = (
            memory_info['ratings_csr_mb'] + 
            memory_info['user_mapper_mb'] + 
            memory_info['movie_mapper_mb'] + 
            memory_info['reverse_movie_mapper_mb'] + 
            memory_info['df_movies_mb'] + 
            total_models_mb
        )
        memory_info['total_system_mb'] = total_system_mb
        
        # Información de archivos en disco (en MB)
        disk_info = {
            'ratings_csr_npz_mb': self._get_file_size_mb(f"{self.path}/ratings_csr.npz"),
            'mappers_pkl_mb': self._get_file_size_mb(f"{self.path}/mappers.pkl"),
            'movies_bayesian_csv_mb': self._get_file_size_mb(f"{self.path}/movies_bayesian.csv")
        }
        
        # Calcular total de archivos en disco
        total_disk_mb = sum(disk_info.values())
        disk_info['total_disk_mb'] = total_disk_mb
        
        # Estadísticas de eficiencia
        efficiency_info = {
            'memory_to_disk_ratio': total_system_mb / total_disk_mb if total_disk_mb > 0 else 0,
            'ratings_compression_ratio': memory_info['ratings_csr_mb'] / disk_info['ratings_csr_npz_mb'] if disk_info['ratings_csr_npz_mb'] > 0 else 0,
            'models_overhead_ratio': total_models_mb / memory_info['ratings_csr_mb'] if memory_info['ratings_csr_mb'] > 0 else 0
        }
        
        # Agregar toda la información al diccionario principal
        info_dict.update({
            'memory_usage_mb': memory_info,
            'disk_usage_mb': disk_info,
            'efficiency_metrics': efficiency_info
        })
        
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
        
        Returns:
            dict: {
                'time_ms': tiempo de ejecución en milisegundos,
                'recommendations': [
                    {
                        'movie_id': int,
                        'title': str,
                        'bayesian_rating': float,
                        'neighbors': [
                            {
                                'user_id': int,
                                'rating': float,
                                'distance': float
                            }
                        ]
                    }
                ]
            }
        """
        start_time = time.time()
        
        # Obtener vecinos con distancias
        distancias, vecinos = self.obtener_vecinos(user_id, metric, top_k)
        vecinos = [v for v in vecinos if v != user_id]
        
        # Obtener películas vistas por el usuario
        user_ratings = self.ratings_csr[user_id].toarray().flatten()
        peliculas_vistas = set(np.where(user_ratings > 0)[0])
        
        # Estructura para almacenar ratings por película y vecinos
        movie_data = {}
        
        for vecino_id, distancia in zip(vecinos, distancias):
            vecino_ratings = self.ratings_csr[vecino_id].toarray().flatten()
            
            for idx, rating in enumerate(vecino_ratings):
                if rating > 0 and idx not in peliculas_vistas:
                    if idx not in movie_data:
                        movie_data[idx] = {
                            'ratings': [],
                            'neighbors': []
                        }
                    
                    movie_data[idx]['ratings'].append(rating)
                    movie_data[idx]['neighbors'].append({
                        'user_id': int(vecino_id),
                        'rating': float(rating),
                        'distance': float(distancia)
                    })
        
        # Procesar recomendaciones
        recommendations = []
        for idx, data in movie_data.items():
            movie_id = self.reverse_movie_mapper[idx]
            row = self.df_movies[self.df_movies["movieId"] == movie_id]
            
            if not row.empty:
                row = row.iloc[0]
                bayesian_rating = row.get("bayesian_rating", np.nan)
                
                recommendations.append({
                    'movie_id': int(movie_id),
                    'title': row["title"],
                    'genres': row["genres"],
                    'bayesian_rating': float(bayesian_rating) if not np.isnan(bayesian_rating) else None,
                    'neighbors': data['neighbors']
                })
        
        # Ordenar por bayesian_rating
        recommendations.sort(key=lambda x: x['bayesian_rating'] if x['bayesian_rating'] is not None else 0, reverse=True)
        
        return {
            'time_ms': round((time.time() - start_time) * 1000, 2),
            'recommendations': recommendations[:top_n]
        }

    def recomendar_por_genero(self, user_id, genero_objetivo, metric='cosine', top_k=5, top_n=10):
        """
        Recomienda películas de un género específico basándose en usuarios similares.
        
        Returns:
            dict: {
                'time_ms': tiempo de ejecución en milisegundos,
                'recommendations': [
                    {
                        'movie_id': int,
                        'title': str,
                        'genres': str,
                        'bayesian_rating': float,
                        'neighbors': [
                            {
                                'user_id': int,
                                'rating': float,
                                'distance': float
                            }
                        ]
                    }
                ]
            }
        """
        start_time = time.time()
        
        # Obtener vecinos con distancias
        distancias, vecinos = self.obtener_vecinos(user_id, metric, top_k)
        vecinos = [v for v in vecinos if v != user_id]
        
        # Obtener películas vistas por el usuario
        user_ratings = self.ratings_csr[user_id].toarray().flatten()
        peliculas_vistas = set(np.where(user_ratings > 0)[0])
        
        # Estructura para almacenar datos por película
        movie_data = {}
        
        for vecino_id, distancia in zip(vecinos, distancias):
            vecino_ratings = self.ratings_csr[vecino_id].toarray().flatten()
            
            for idx, rating in enumerate(vecino_ratings):
                if rating > 0 and idx not in peliculas_vistas:
                    movie_id = self.reverse_movie_mapper[idx]
                    row = self.df_movies[self.df_movies["movieId"] == movie_id]
                    
                    if not row.empty and genero_objetivo in row["genres"].values[0].split('|'):
                        if idx not in movie_data:
                            movie_data[idx] = {
                                'ratings': [],
                                'neighbors': []
                            }
                        
                        movie_data[idx]['ratings'].append(rating)
                        movie_data[idx]['neighbors'].append({
                            'user_id': int(vecino_id),
                            'rating': float(rating),
                            'distance': float(distancia)
                        })
        
        # Procesar recomendaciones
        recommendations = []
        for idx, data in movie_data.items():
            movie_id = self.reverse_movie_mapper[idx]
            row = self.df_movies[self.df_movies["movieId"] == movie_id]
            
            if not row.empty:
                row = row.iloc[0]
                bayesian_rating = row.get("bayesian_rating", np.nan)
                
                recommendations.append({
                    'movie_id': int(movie_id),
                    'title': row["title"],
                    'genres': row["genres"],
                    'bayesian_rating': float(bayesian_rating) if not np.isnan(bayesian_rating) else None,
                    'neighbors': data['neighbors']
                })
        
        # Ordenar por bayesian_rating
        recommendations.sort(key=lambda x: x['bayesian_rating'] if x['bayesian_rating'] is not None else 0, reverse=True)
        
        return {
            'time_ms': round((time.time() - start_time) * 1000, 2),
            'recommendations': recommendations[:top_n]
        }
    
    def buscar_peliculas(self, nombre: str = None, genero: str = None, top_n: int = 10):
        """
        Busca películas por nombre y/o género.
        
        Args:
            nombre (str): Parte del título a buscar (case insensitive)
            genero (str): Género a filtrar (ej: 'Action')
            top_n (int): Máximo número de resultados a retornar
            
        Returns:
            list: Lista de diccionarios con información de películas
        """
        results = self.df_movies.copy()
        
        # Filtrar por género si se especificó
        if genero:
            results = results[results['genres'].str.contains(genero, case=False, na=False)]
        
        # Filtrar por nombre si se especificó
        if nombre:
            results = results[results['title'].str.contains(nombre, case=False, na=False)]
        
        # Ordenar por bayesian_rating (si existe)
        if 'bayesian_rating' in results.columns:
            results = results.sort_values('bayesian_rating', ascending=False)
        
        # Formatear resultados
        peliculas = []
        for _, row in results.head(top_n).iterrows():
            peliculas.append({
                'movie_id': int(row['movieId']),
                'title': row['title'],
                'genres': row['genres'],
                'bayesian_rating': float(row['bayesian_rating']) if 'bayesian_rating' in row else None
            })
        
        return peliculas
