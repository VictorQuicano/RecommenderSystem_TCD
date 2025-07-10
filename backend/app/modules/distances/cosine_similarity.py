import math
from typing import List

def cosine_similarity(values1: List[float], values2: List[float]) -> float:
    """
    Calcula la similitud del coseno entre dos vectores
    Formula: cos(x,y) = (x·y) / (||x|| × ||y||)
    """
    filtered_values1 = []
    filtered_values2 = []
    
    for v1, v2 in zip(values1, values2):
        if (v1 is not None and v2 is not None and 
            not (math.isnan(v1) if isinstance(v1, float) else False) and 
            not (math.isnan(v2) if isinstance(v2, float) else False)):
            filtered_values1.append(v1)
            filtered_values2.append(v2)
    
    if len(filtered_values1) == 0:
        return 0.0
    
    dot_product = 0
    for v1, v2 in zip(filtered_values1, filtered_values2):
        dot_product += v1 * v2
    
    magnitude1 = 0
    for v1 in filtered_values1:
        magnitude1 += v1 * v1
    magnitude1 = math.sqrt(magnitude1)
    
    magnitude2 = 0
    for v2 in filtered_values2:
        magnitude2 += v2 * v2
    magnitude2 = math.sqrt(magnitude2)
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    cosine_sim = dot_product / (magnitude1 * magnitude2)
    
    return cosine_sim