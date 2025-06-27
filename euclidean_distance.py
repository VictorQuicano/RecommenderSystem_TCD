import math
from typing import List

#Params
#values1 = df["Heather"].tolist()
#values2 = df["Thomas"].tolist()

def euclidean_distance(values1: List[float], values2: List[float]) -> float:
    squared_sum = 0
    for v1, v2 in zip(values1, values2):
        if v1 is not None and v2 is not None:
            diff = v1 - v2
            squared_sum += diff * diff

    return math.sqrt(squared_sum)