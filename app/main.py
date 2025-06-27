from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pydantic import BaseModel
#from Knn import * 
import os

app = FastAPI()

path_df_movies = "data/Pelis_short.csv"
path_df_ratings = "data/Movie_Ratings.csv"

directorio_actual = os.getcwd()
path_movies = os.path.join(directorio_actual, path_df_movies)
path_rating = os.path.join(directorio_actual, path_df_ratings)

df_movies = pd.read_csv(path_movies, index_col=0)
df_ratings = pd.read_csv(path_rating, index_col=0)



def promedio_por_fila(df):
    # Calcula el promedio por fila
    promedios = round(df.mean(axis=1),2)
    
    # Convierte a diccionario
    resultado = promedios.to_dict()
    
    return resultado

def getDataFrameAndUsers(df_selected):
    df = pd.read_csv(df_selected, index_col=0)
    users = df.columns
    return df, users


# Estado en memoria
selected_variable = {"value": None}
def getDataFrameAndUsers(df_selected):
    df = pd.read_csv(df_selected, index_col=0)
    users = df.columns
    return df, users

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Selection(BaseModel):
    variable: str


# POST endpoint para seleccionar una variable
@app.post("/api/select")
def select_variable(selection: Selection):
    if selection.variable not in df_movies.columns and selection.variable not in df_ratings.columns:
        raise HTTPException(status_code=400, detail="Variable not found in either dataset.")
    
    selected_variable["value"] = selection.variable
    return {"selected_variable": selected_variable["value"]}

# GET endpoint para consultar la variable seleccionada
@app.get("/api/selected")
def get_selected_variable():
    return {"selected_variable": selected_variable["value"]}





@app.get("/api/hello")
def read_hello():
    return {"message": "Hello from FastAPI!"}