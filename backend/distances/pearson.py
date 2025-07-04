import math
from typing import List

def similitud_pearson(lista1: List[float], lista2: List[float]) -> float:
    """
    Calcula la similitud de Pearson entre dos listas de valores numéricos.
    """

    # Filtrar valores donde ambos no sean None o NaN
    v1_filtrados = []
    v2_filtrados = []

    for v1, v2 in zip(lista1, lista2):
        if v1 is not None and v2 is not None:
            if isinstance(v1, float) and math.isnan(v1): continue
            if isinstance(v2, float) and math.isnan(v2): continue
            v1_filtrados.append(v1)
            v2_filtrados.append(v2)

    if len(v1_filtrados) < 2:
        return 0.0

    # Calcular medias
    media1 = sum(v1_filtrados) / len(v1_filtrados)
    media2 = sum(v2_filtrados) / len(v2_filtrados)

    # Numerador y denominador
    numerador = sum((a - media1) * (b - media2) for a, b in zip(v1_filtrados, v2_filtrados))
    denom1 = math.sqrt(sum((a - media1) ** 2 for a in v1_filtrados))
    denom2 = math.sqrt(sum((b - media2) ** 2 for b in v2_filtrados))

    if denom1 == 0 or denom2 == 0:
        return 0.0
    
    return numerador / (denom1 * denom2)
