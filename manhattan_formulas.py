import numpy as np
import math

def manhattan_distance(a, b):
    """
    Calcula la distancia Manhattan entre dos puntos, ignorando valores inválidos.
    
    Parámetros:
    a, b -- listas de valores numéricos
    
    Retorna:
    Distancia Manhattan o None si no hay dimensiones válidas
    """
    distance = 0.0
    valid_pairs = 0
    
    for ai, bi in zip(a, b):
        if ai is None or math.isnan(ai) or bi is None or math.isnan(bi):
            continue
        distance += abs(ai - bi)
        valid_pairs += 1
    
    if valid_pairs == 0:
        return None
    return distance

def manhattan_distance_matrix(data):
    """
    Calcula la matriz de distancias Manhattan para todos los registros.
    """
    n = len(data)
    dist_matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(i+1, n):
            distance = manhattan_distance(data[i], data[j])
            dist_matrix[i][j] = distance
            dist_matrix[j][i] = distance
    
    return dist_matrix