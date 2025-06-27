import math

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

def pearson_distance(a, b):
    """Distancia Pearson (1 - correlación)"""
    valid_a = []
    valid_b = []
    
    for ai, bi in zip(a, b):
        if ai is None or math.isnan(ai) or bi is None or math.isnan(bi):
            continue
        valid_a.append(ai)
        valid_b.append(bi)
    
    n = len(valid_a)
    if n < 2:
        return float('nan')
    
    mean_a = sum(valid_a) / n
    mean_b = sum(valid_b) / n
    
    covariance = 0.0
    var_a = 0.0
    var_b = 0.0
    
    for ai, bi in zip(valid_a, valid_b):
        diff_a = ai - mean_a
        diff_b = bi - mean_b
        covariance += diff_a * diff_b
        var_a += diff_a ** 2
        var_b += diff_b ** 2
    
    if var_a == 0 or var_b == 0:
        return float('nan')
    
    correlation = covariance / math.sqrt(var_a * var_b)
    return 1 - correlation

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