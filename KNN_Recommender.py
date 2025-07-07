# -*- coding: utf-8 -*-
"""
Módulo: recomendacion.py

Implementa la etapa de recomendaciones basadas en vecinos más cercanos (Punto 3).
Define un umbral de rating mínimo y K vecinos para sugerir películas que el usuario objetivo
no haya visto, pero sí han sido valoradas por sus vecinos.

Funciones principales:
- generar_recomendaciones: retorna DataFrame con recomendaciones y datos de soporte.
"""
import pandas as pd

class RecomendadorKNN:
    def __init__(self, knn_calculador, umbral_rating=4.0):
        """
        Inicializa el recomendador.
        :param knn_calculador: instancia de KNNCalcularDistancia
        :param umbral_rating: valor mínimo para considerar que un vecino "ha gustado" la película
        """
        self.knn = knn_calculador
        self.umbral = umbral_rating

    def generar_recomendaciones(self, df_ratings, usuario_objetivo, k=5):
        """
        Genera recomendaciones de películas para un usuario.

        Pseudocódigo:
        1. Obtener los K vecinos más cercanos al usuario objetivo usando self.knn.get_knn.
        2. Inicializar lista de recomendaciones vacía.
        3. Para cada vecino en la lista de vecinos:
           a. Identificar películas calificadas por el vecino con rating >= umbral.
           b. Filtrar aquellas películas que el usuario objetivo NO haya visto (NaN en df_ratings).
           c. Para cada película candidata:
              - Registrar: usuario_vecino, película, rating_vecino.
        4. Construir un DataFrame con todas las recomendaciones encontradas.
        5. Opcional: ordenar o agregar métricas adicionales (por ejemplo, contar cuántos vecinos recomiendan cada película).
        6. Devolver el DataFrame final.
        """
        # 1. Obtener vecinos más cercanos
        df_vecinos = self.knn.get_knn(df_ratings, usuario_objetivo, k)
        vecinos = df_vecinos.index.tolist()
        # 2. & 3. Explorar cada vecino y sus películas favoritas
        recomendaciones = []
        serie_objetivo = df_ratings[usuario_objetivo]
        for vecino in vecinos:
            serie_vecino = df_ratings[vecino]
            # a. películas con rating >= umbral
            peliculas_gustadas = serie_vecino[serie_vecino >= self.umbral].index
            # b. filtrar las que objetivo no vio
            peliculas_candidatas = [p for p in peliculas_gustadas if pd.isna(serie_objetivo[p])]
            # c. registrar cada recomendación
            for pelicula in peliculas_candidatas:
                recomendaciones.append({
                    'usuario_vecino': vecino,
                    'pelicula': pelicula,
                    'rating_vecino': serie_vecino[pelicula]
                })

        # 4. Construir DataFrame
        df_recomendaciones = pd.DataFrame(recomendaciones)

        # 5. (Opcional) Agregar conteo de recomendaciones por película
        if not df_recomendaciones.empty:
            conteo = df_recomendaciones.groupby('pelicula').size().rename('veces_recomendada')
            df_recomendaciones = df_recomendaciones.merge(
                conteo, left_on='pelicula', right_index=True
            )

        # 6. Devolver resultados ordenados por veces_recomendada y rating_vecino
        if 'veces_recomendada' in df_recomendaciones:
            return df_recomendaciones.sort_values(
                by=['veces_recomendada', 'rating_vecino'], ascending=False
            )
        return df_recomendaciones

# Ejemplo de uso (no ejecutar al import):
# from knn import KNNCalcularDistancia
# from distancias import pearson_distance
# knn_calc = KNNCalcularDistancia(pearson_distance)
# recomendador = RecomendadorKNN(knn_calc, umbral_rating=4.5)
# df_rec = recomendador.generar_recomendaciones(df_imdb, usuario_id, k=5)
# print(df_rec)
