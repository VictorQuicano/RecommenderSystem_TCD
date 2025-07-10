from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from app.modules.knn.Knn import find_knn_for_column
from app.api.dependencies import get_dataframe
import pandas as pd

router = APIRouter(prefix="/knn", tags=["knn"])

@router.get("/")
async def knn_neighbors(
    user: str = Query(...),
    k: int = Query(...),
    dataset: str = Query("Movie_Ratings.csv"),
    distance: str = Query("euclidean"),
    df: pd.DataFrame = Depends(get_dataframe)
):
    try:
        if user not in df.columns:
            return JSONResponse(status_code=400, content={"error": "Datos inválidos"})

        vecinos = find_knn_for_column(df, user, distance_type=distance, k=k)
        resultado = [{
            "neighbor": vecino["neighbor"],
            "distance": round(vecino["distance"], 4)
        } for vecino in vecinos]

        return resultado

    except Exception as e:
        print("❌ Error en /knn:", e)
        return JSONResponse(status_code=500, content={"error": "Error interno"})