from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from app.modules.knn.Knn import recommend_for_column
from app.api.dependencies import get_dataframe

import pandas as pd

router = APIRouter(prefix="/movie_lens", tags=["movie_lens"])

