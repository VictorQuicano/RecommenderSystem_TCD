import pandas as pd
import numpy as np

def similitud_pearson(serie_usuario_a: pd.Series, serie_usuario_b: pd.Series) -> float:
    #calificadas por ambos usuarios
    peliculas_comunes = serie_usuario_a.notna() & serie_usuario_b.notna()
    
    #vectores de ratings emparejados
    calificaciones_usuario_a = serie_usuario_a[peliculas_comunes].values
    calificaciones_usuario_b = serie_usuario_b[peliculas_comunes].values
    
    #Revisar si hay suficientes datos
    if len(calificaciones_usuario_a) < 2:
        return 0.0
    
    #Medias de cada usuario
    media_usuario_a = np.mean(calificaciones_usuario_a)
    media_usuario_b = np.mean(calificaciones_usuario_b)
    
    #Numerador: covarianza empírica
    numerador_covarianza = np.sum(
        (calificaciones_usuario_a - media_usuario_a) *
        (calificaciones_usuario_b - media_usuario_b)
    )
    
    #Denominador: producto de desviaciones estándar
    desviacion_usuario_a = np.sqrt(np.sum((calificaciones_usuario_a - media_usuario_a) ** 2))
    desviacion_usuario_b = np.sqrt(np.sum((calificaciones_usuario_b - media_usuario_b) ** 2))
    producto_desviaciones = desviacion_usuario_a * desviacion_usuario_b
    
    if producto_desviaciones == 0:
        return 0.0
    
    #Coeficiente de Pearson
    return numerador_covarianza / producto_desviaciones


if __name__ == "__main__":
    ruta_csv = 'Pelis_short.csv'
    df_peliculas = pd.read_csv(ruta_csv, index_col=0)
    
    usuario_a = 'Patrick C'
    usuario_b = 'Heather'
    coeficiente = similitud_pearson(df_peliculas[usuario_a], df_peliculas[usuario_b])
    print(f"Coeficiente de Pearson entre {usuario_a} y {usuario_b}: {coeficiente:.3f}")
