from pathlib import Path
import pandas as pd
import numpy as np
from fastapi import Depends

# Obtener la ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

def load_clean_csv(relative_path):
    # Construir ruta absoluta
    abs_path = BASE_DIR / relative_path
    df = pd.read_csv(abs_path, index_col=0)
    if df.columns[0].startswith("Unnamed") or df.columns[0] == "":
        df.rename(columns={df.columns[0]: "movie"}, inplace=True)
    return df

# Datasets compartidos
dataframes = {
    "Movie_Ratings.csv": load_clean_csv("data/Movie_Ratings.csv"),
    "Pelis_short.csv": load_clean_csv("data/Pelis_short.csv"),
}

def get_dataframe(dataset: str):
    df = dataframes.get(dataset)
    if df is None:
        raise ValueError("Dataset no encontrado")
    return df