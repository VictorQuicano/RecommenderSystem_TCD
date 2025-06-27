import pandas as pd
import math

def euclidean_distance(df: pd.DataFrame, user1: str, user2: str) -> float:
    values1 = df[user1].tolist()
    values2 = df[user2].tolist()

    squared_sum = 0
    for v1, v2 in zip(values1, values2):
        if pd.notna(v1) and pd.notna(v2):
            diff = v1 - v2
            squared_sum += diff * diff

    return math.sqrt(squared_sum)