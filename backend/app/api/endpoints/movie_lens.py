from fastapi import APIRouter, Depends, Query, Body
import time
from fastapi.responses import JSONResponse
from app.api.dependencies import get_recommender
from app.modules.movies import MovieRecommendationSystem

import pandas as pd
from typing import Dict

router = APIRouter(prefix="/movie_lens", tags=["movie_lens"])

def formato_humano(mb):
    if mb < 0:
        return "Valor inválido"
    
    if mb < 1:
        kb = mb * 1024
        return f"{kb:.2f} KB"
    elif mb >= 1024:
        gb = mb / 1024
        return f"{gb:.2f} GB"
    else:
        return f"{mb:.2f} MB"

@router.get("/info", summary="Obtiene información detallada del sistema de recomendación")
async def get_system_info(
    recommender: MovieRecommendationSystem = Depends(get_recommender)
):
    """
    Obtiene información completa sobre el sistema de recomendación:
    - Métricas disponibles
    - Estadísticas del dataset
    - Uso de memoria y disco
    - Eficiencia del sistema
    """
    try:
        raw_info = recommender.info()
        
        # Formatear para hacerlo más legible
        formatted_info = {
            "general": {
                "metricas_disponibles": raw_info['metrics'],
                "tiempos_entrenamiento": {
                    metric: f"{time:.2f} segundos" 
                    for metric, time in raw_info['training_times'].items()
                }
            },
            "dataset": {
                "total_usuarios": raw_info['dataset_info']['num_users'],
                "total_peliculas": raw_info['dataset_info']['num_movies'],
                "total_valoraciones": f"{raw_info['dataset_info']['num_ratings']:,}",
                "espacios_vacios": f"{raw_info['dataset_info']['sparsity']*100:.1f}%",
                "compresion_datos": f"{raw_info['efficiency_metrics']['ratings_compression_ratio']:.1f}x"
            },
            "memoria": {
                "total_uso_memoria": formato_humano(raw_info['memory_usage_mb']['total_system_mb']),
                "desglose": {
                    "matriz_ratings": formato_humano(raw_info['memory_usage_mb']['ratings_csr_mb']),
                    "mapeo_usuarios": formato_humano(raw_info['memory_usage_mb']['user_mapper_mb']),
                    "mapeo_peliculas": formato_humano(raw_info['memory_usage_mb']['movie_mapper_mb']),
                    "datos_peliculas": formato_humano(raw_info['memory_usage_mb']['df_movies_mb']),
                    "modelos_knn": formato_humano(raw_info['memory_usage_mb']['total_models_mb'])
                }
            },
            "almacenamiento": {
                "total_disco": formato_humano(raw_info['disk_usage_mb']['total_disk_mb']),
                "desglose": {
                    "matriz_ratings": formato_humano(raw_info['disk_usage_mb']['ratings_csr_npz_mb']),
                    "mapeos": formato_humano(raw_info['disk_usage_mb']['mappers_pkl_mb']),
                    "datos_peliculas": formato_humano(raw_info['disk_usage_mb']['movies_bayesian_csv_mb'])
                }
            },
            "rendimiento": {
                "ratio_memoria_disco": f"{raw_info['efficiency_metrics']['memory_to_disk_ratio']:.1f}x",
                "overhead_modelos": f"{raw_info['efficiency_metrics']['models_overhead_ratio']*100:.1f}%"
            }
        }
        
        return JSONResponse(content=formatted_info)
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error al obtener información del sistema: {str(e)}"}
        )

@router.get("/vecinos", summary="Obtiene los usuarios más similares a un usuario dado")
async def get_similar_users(
    user_id: int = Query(..., description="ID del usuario a buscar"),
    metric: str = Query("cosine", description="Métrica de distancia", enum=["cosine", "euclidean", "manhattan"]),
    k: int = Query(5, description="Número de vecinos a retornar"),
    recommender: MovieRecommendationSystem = Depends(get_recommender)
):
    """
    Obtiene los k usuarios más similares al usuario especificado, usando la métrica seleccionada.
    Excluye al propio usuario de los resultados y retorna un vecino adicional para compensar.
    """
    try:
        start_time = time.time()
        
        # Obtenemos k+1 vecinos porque luego excluiremos al usuario mismo
        distancias, indices = recommender.obtener_vecinos(user_id, metric, k+1)
        
        # Filtrar para excluir al usuario mismo (si está en los resultados)
        vecinos_filtrados = []
        for i, (vecino_id, distancia) in enumerate(zip(indices, distancias)):
            if vecino_id != user_id:
                vecinos_filtrados.append({
                    "user_id": int(vecino_id),
                    "proximidad": float(distancia)
                })
                
                # Si ya tenemos los k vecinos que necesitamos, salir
                if len(vecinos_filtrados) == k:
                    break
        
        processing_time = (time.time() - start_time) * 1000  # Convertir a ms
        
        return {
            "time_ms": round(processing_time, 2),
            "vecinos": vecinos_filtrados
        }
        
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error interno: {str(e)}"}
        )
    
@router.post("/nuevo", summary="Agrega un nuevo usuario o actualiza sus valoraciones")
async def agregar_usuario(
    nuevas_valoraciones: Dict[int, float] = Body(..., example={1: 4.0, 32: 5.0, 589: 3.0}),
    recommender: MovieRecommendationSystem = Depends(get_recommender)
):
    """
    Agrega un nuevo usuario con sus valoraciones o actualiza uno existente.
    Retorna el ID asignado y los tiempos de reentrenamiento por métrica.
    """
    try:
        # Procesar las valoraciones (convertir keys a int por si vienen como strings)
        ratings_processed = {int(movie_id): float(rating) for movie_id, rating in nuevas_valoraciones.items()}
        
        # Llamar a la función del sistema de recomendación
        _, user_id, training_times = recommender.agregar_o_actualizar_usuario(ratings_processed)
        
        # Formatear los tiempos de entrenamiento
        tiempos_formateados = [
            {
                "metrica": metric,
                "tiempo_ms": round(time * 1000, 2)  # Convertir a milisegundos
            }
            for metric, time in training_times.items()
        ]
        
        return {
            "user_id": int(user_id),
            "tiempos_entrenamiento": tiempos_formateados
        }
        
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error al procesar las valoraciones: {str(e)}"}
        )
    
@router.get("/recomendar", summary="Obtiene recomendaciones generales de películas")
async def recomendar_peliculas_endpoint(
    user_id: int = Query(..., description="ID del usuario"),
    metric: str = Query("cosine", description="Métrica de distancia", enum=["cosine", "euclidean", "manhattan"]),
    top_k: int = Query(5, description="Número de vecinos a considerar"),
    top_n: int = Query(10, description="Número de recomendaciones a retornar"),
    recommender: MovieRecommendationSystem = Depends(get_recommender)
):
    """
    Recomienda películas basadas en usuarios similares, ordenadas por bayesian rating.
    Incluye información de los vecinos que contribuyeron a cada recomendación.
    """
    try:
        result = recommender.recomendar_peliculas(
            user_id=user_id,
            metric=metric,
            top_k=top_k,
            top_n=top_n
        )
        return result
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error al generar recomendaciones: {str(e)}"}
        )
    
@router.get("/recomendar/genero", summary="Obtiene recomendaciones de películas filtradas por género")
async def recomendar_por_genero_endpoint(
    user_id: int = Query(..., description="ID del usuario"),
    genero_objetivo: str = Query(..., description="Género a filtrar (ej: 'Action', 'Comedy')"),
    metric: str = Query("cosine", description="Métrica de distancia", enum=["cosine", "euclidean", "manhattan"]),
    top_k: int = Query(5, description="Número de vecinos a considerar"),
    top_n: int = Query(10, description="Número de recomendaciones a retornar"),
    recommender: MovieRecommendationSystem = Depends(get_recommender)
):
    """
    Recomienda películas de un género específico basadas en usuarios similares,
    ordenadas por bayesian rating. Incluye información de los vecinos que
    contribuyeron a cada recomendación.
    """
    try:
        result = recommender.recomendar_por_genero(
            user_id=user_id,
            genero_objetivo=genero_objetivo,
            metric=metric,
            top_k=top_k,
            top_n=top_n
        )
        return result
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error al generar recomendaciones por género: {str(e)}"}
        )
    
@router.get("/buscar", summary="Busca películas por nombre y/o género")
async def buscar_peliculas_endpoint(
    nombre: str = Query(None, description="Parte del título a buscar", min_length=3),
    genero: str = Query(None, description="Género a filtrar (ej: 'Action')"),
    top_n: int = Query(10, description="Número máximo de resultados"),
    recommender: MovieRecommendationSystem = Depends(get_recommender)
):
    """
    Busca películas en el catálogo por:
    - Título (búsqueda parcial case insensitive)
    - Género (filtro exacto)
    - Ambos criterios simultáneamente
    
    Devuelve resultados ordenados por rating bayesiano (si existe).
    """
    try:
        # Validar que al menos un criterio esté presente
        if nombre is None and genero is None:
            return JSONResponse(
                status_code=400,
                content={"error": "Debe especificar al menos un criterio (nombre o género)"}
            )
        
        resultados = recommender.buscar_peliculas(
            nombre=nombre,
            genero=genero,
            top_n=top_n
        )
        
        return {
            "count": len(resultados),
            "results": resultados
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error en la búsqueda: {str(e)}"}
        )