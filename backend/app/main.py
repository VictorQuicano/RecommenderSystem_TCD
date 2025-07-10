from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import matrix, compare, knn, recommender

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers
app.include_router(matrix.router)
app.include_router(compare.router)
app.include_router(knn.router)
app.include_router(recommender.router)

@app.get("/")
async def root():
    return {"message": "KNN Movie Recommender API"}
"""
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from fastapi.responses import JSONResponse
from distances.euclidean_distance import euclidean_distance
from distances.manhattan_formulas import manhattan_distance
from distances.cosine_similarity import cosine_similarity
from distances.pearson import similitud_pearson
from knn.Knn import *
from typing import List
import pandas as pd

app = FastAPI()

# Permitir CORS para que puedas consumirlo desde localhost:5173 (vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir a ["http://localhost:5173"] si quieres
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import numpy as np  # ⬅️ Asegúrate de importar esto
# Carga los datasets al iniciar
def load_clean_csv(path):
    df = pd.read_csv(path, index_col=0)
    # Si la primera columna no tiene nombre, asígnale uno
    if df.columns[0].startswith("Unnamed") or df.columns[0] == "":
        df.rename(columns={df.columns[0]: "movie"}, inplace=True)

    return df


dataframes = {
    "Movie_Ratings.csv": load_clean_csv("../Movie_Ratings.csv"),
    "Pelis_short.csv": load_clean_csv("../Pelis_short.csv"),
}

@app.get("/matrix")
async def get_matrix(dataset: str = Query(...)):
    try:
        df = dataframes.get(dataset)
        if df is None:
            return JSONResponse(status_code=404, content={"error": "Dataset no encontrado"})

        # Asegurar que la primera columna sea el nombre de las películas
        if df.columns[0].lower().startswith("unnamed") or df.columns[0] == "":
            df.rename(columns={df.columns[0]: "movie"}, inplace=True)

        # Guardar los nombres de películas
        movies = df["movie"].tolist()

        # Limpiar las columnas numéricas
        df_clean = df.drop(columns=["movie"])
        df_clean = df_clean.apply(pd.to_numeric, errors="coerce")
        df_clean = df_clean.replace([np.nan, np.inf, -np.inf], None)

        # Preparar respuesta
        matrix_data = {
            "columns": df_clean.columns.tolist(),
            "movies": movies,  # etiquetas para las filas
            "data": df_clean.values.tolist()
        }

        return matrix_data

    except Exception as e:
        print("❌ Error en /matrix:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/")
async def get_column_names(dataset: str = Query(...)) -> List[str]:
    if dataset not in dataframes:
        return []

    df = dataframes[dataset]
    columns = df.columns.tolist()

    # Filtra columnas no deseadas como "Unnamed: 0"
    filtered = [col for col in columns if not col.lower().startswith("unnamed")]

    return filtered

@app.get("/")
async def get_column_names(dataset: str = Query(...)) -> List[str]:
    if dataset not in dataframes:
        return []

    df = dataframes[dataset]
    columns = df.columns.tolist()

    # Filtra columnas no deseadas como "Unnamed: 0"
    filtered = [col for col in columns if not col.lower().startswith("unnamed")]

    return filtered
  
  

@app.get("/compare")
async def compare_users(
    u1: str = Query(...),
    u2: str = Query(...),
    metric: str = Query(...),
    dataset: str = Query("Movie_Ratings.csv")
):
    try:
        df = dataframes[dataset]
        if u1 not in df.columns or u2 not in df.columns:
            return { "distance": None }

        series1 = df[u1]
        series2 = df[u2]
        mask = series1.notna() & series2.notna()

        v1 = series1[mask].tolist()
        v2 = series2[mask].tolist()
        
        dis = 0
        if metric == "euclidean":
          dis = euclidean_distance(v1, v2)
        elif metric == "manhattan":
          dis = manhattan_distance(v1, v2)
        elif metric == "pearson":
          dis = similitud_pearson(v1, v2)
        elif metric == "cosine":
          dis = cosine_similarity(v1, v2)
          
        dis = round(dis, 4)
        return dis

    except Exception as e:
        print("❌ Error en /compare:", e)
        return { "distance": None }
      
      
@app.get("/knn")
async def knn_neighbors(
    user: str = Query(...),
    k: int = Query(...),
    dataset: str = Query("Movie_Ratings.csv"),
    distance: str = Query("euclidean")
):
    try:
        df = dataframes.get(dataset)
        if df is None or user not in df.columns:
            return JSONResponse(status_code=400, content={"error": "Datos inválidos"})

        # Ejecutar el cálculo de KNN
        vecinos = find_knn_for_column(df, user, distance_type=distance, k=k)
        print(vecinos)
        # Formatear el resultado
        resultado = []
        for vecino in vecinos:
            resultado.append({
                "neighbor": vecino["neighbor"],
                "distance": round(vecino["distance"], 4)
            })

        return resultado

    except Exception as e:
        print("❌ Error en /knn:", e)
        return JSONResponse(status_code=500, content={"error": "Error interno"})
    
@app.get("/recommender")
async def recommender(
    user: str = Query(...),
    k: int = Query(...),
    dataset: str = Query("Movie_Ratings.csv"),
    distance: str = Query("euclidean"),
    umbral: float = Query(...)
):
    try:
        df = dataframes.get(dataset)

        if df is None or user not in df.columns:
            return JSONResponse(status_code=400, content={"error": "Datos inválidos"})
        
        recommendations = recommend_for_column(df, user, k,distance,umbral)
        return recommendations 
        

    except Exception as e:
        print("❌ Error en /recommender:", e)
        return JSONResponse(status_code=500, content={"error": "Error interno"})
"""
