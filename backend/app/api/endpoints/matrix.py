from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
from app.api.dependencies import get_dataframe

router = APIRouter(prefix="/matrix", tags=["matrix"])

@router.get("/")
async def get_matrix(dataset: str = Query(...)):
    try:
        df = get_dataframe(dataset)
        
        if df.columns[0].lower().startswith("unnamed") or df.columns[0] == "":
            df.rename(columns={df.columns[0]: "movie"}, inplace=True)

        movies = df["movie"].tolist()
        df_clean = df.drop(columns=["movie"])
        df_clean = df_clean.apply(pd.to_numeric, errors="coerce")
        df_clean = df_clean.replace([np.nan, np.inf, -np.inf], None)

        matrix_data = {
            "columns": df_clean.columns.tolist(),
            "movies": movies,
            "data": df_clean.values.tolist()
        }

        return matrix_data

    except Exception as e:
        print("❌ Error en /matrix:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})