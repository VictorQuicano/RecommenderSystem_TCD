import math
import numpy as np


def euclidean_distance(a, b):
    """Distancia Euclidiana"""
    sum_sq = 0.0
    valid_pairs = 0
    
    for ai, bi in zip(a, b):
        if ai is None or math.isnan(ai) or bi is None or math.isnan(bi):
            continue
        sum_sq += (ai - bi)**2
        valid_pairs += 1
    
    if valid_pairs == 0:
        return float('nan')
    return math.sqrt(sum_sq)

def manhattan_distance(a, b):
    """Distancia Manhattan"""
    distance = 0.0
    valid_pairs = 0
    
    for ai, bi in zip(a, b):
        if ai is None or math.isnan(ai) or bi is None or math.isnan(bi):
            continue
        distance += abs(ai - bi)
        valid_pairs += 1
    
    if valid_pairs == 0:
        return float('nan')
    return distance

def pearson_distance(serie_usuario_a, serie_usuario_b):
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
    
    coeficiente=numerador_covarianza / producto_desviaciones
    # Convertir coeficiente en distancia:
    distancia_basada_en_pearson = 1 - coeficiente
    return distancia_basada_en_pearson




def cosine_distance(a, b):
    """Distancia Coseno (1 - similitud coseno)"""
    dot_product = 0.0
    norm_a = 0.0
    norm_b = 0.0
    valid_pairs = 0
    
    for ai, bi in zip(a, b):
        if ai is None or math.isnan(ai) or bi is None or math.isnan(bi):
            continue
        dot_product += ai * bi
        norm_a += ai ** 2
        norm_b += bi ** 2
        valid_pairs += 1
    
    if valid_pairs == 0 or norm_a == 0 or norm_b == 0:
        return float('nan')
    
    norm_a = math.sqrt(norm_a)
    norm_b = math.sqrt(norm_b)
    cosine_sim = dot_product / (norm_a * norm_b)
    return 1 - cosine_sim