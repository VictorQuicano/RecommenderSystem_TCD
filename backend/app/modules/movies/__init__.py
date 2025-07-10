from .MovieLens import MovieRecommendationSystem

# Instancia única que se inicializará al importar el módulo
recommendation_system = None

def initialize_system(data_path: str):
    global recommendation_system
    recommendation_system = MovieRecommendationSystem(data_path)
    return recommendation_system

def get_recommendation_system():
    if recommendation_system is None:
        raise RuntimeError("El sistema de recomendación no ha sido inicializado")
    return recommendation_system

__all__ = ['MovieRecommendationSystem', 'initialize_system', 'get_recommendation_system']