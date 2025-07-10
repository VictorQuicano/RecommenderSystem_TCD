from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from app.modules.knn.Knn import recommend_for_column
from app.api.dependencies import get_dataframe

import pandas as pd

router = APIRouter(prefix="/recommender", tags=["recommender"])

@router.get("/")
async def recommender(
    user: str = Query(...),
    k: int = Query(...),
    dataset: str = Query("Movie_Ratings.csv"),
    distance: str = Query("euclidean"),
    umbral: float = Query(...),
    df: pd.DataFrame = Depends(get_dataframe)
):
    try:
        if user not in df.columns:
            return JSONResponse(status_code=400, content={"error": "Datos inválidos"})
        
        recommendations = recommend_for_column(df, user, k, distance, umbral)
        return recommendations 

    except Exception as e:
        print("❌ Error en /recommender:", e)
        return JSONResponse(status_code=500, content={"error": "Error interno"})