from fastapi import APIRouter, Query, Depends
from app.modules.distances.euclidean_distance import euclidean_distance
from app.modules.distances.manhattan_formulas import manhattan_distance
from app.modules.distances.cosine_similarity import cosine_similarity
from app.modules.distances.pearson import similitud_pearson
from app.api.dependencies import get_dataframe
import pandas as pd

router = APIRouter(prefix="/compare", tags=["compare"])

@router.get("/")
async def compare_users(
    u1: str = Query(...),
    u2: str = Query(...),
    metric: str = Query(...),
    dataset: str = Query("Movie_Ratings.csv"),
    df: pd.DataFrame = Depends(get_dataframe)
):
    try:
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