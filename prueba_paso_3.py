import pandas as pd
import math
from formulas import euclidean_distance, manhattan_distance, pearson_distance, cosine_distance
from cosine_similarity import cosine_similarity
from Knn import KNNCalcularDistancia

def mostrar_peliculas_vistas(df, usuario):
    """
    Muestra las películas vistas por un usuario con sus calificaciones
    """
    print(f"\n=== Películas vistas por {usuario} ===")
    peliculas_vistas = df[usuario].dropna()
    
    if len(peliculas_vistas) == 0:
        print(f"{usuario} no ha visto ninguna película")
        return peliculas_vistas
    
    for pelicula, rating in peliculas_vistas.items():
        print(f"{pelicula} - {rating}")
    
    return peliculas_vistas

def obtener_peliculas_no_vistas(df, usuario):
    """
    Obtiene las películas que un usuario NO ha visto
    """
    peliculas_no_vistas = df[usuario].isna()
    return df[peliculas_no_vistas].index.tolist()

def recomendar_peliculas_knn(df, usuario_objetivo, k=5, metrica='euclidean'):
    """
    Recomienda películas basándose en los K vecinos más cercanos
    """
    print(f"\n{'='*60}")
    print(f"RECOMENDADOR DE PELÍCULAS PARA {usuario_objetivo.upper()}")
    print(f"{'='*60}")
    
    # Verificar que el usuario existe
    if usuario_objetivo not in df.columns:
        print(f"Error: {usuario_objetivo} no está en la base de datos")
        return
    
    # Mostrar películas vistas por el usuario objetivo
    peliculas_vistas = mostrar_peliculas_vistas(df, usuario_objetivo)
    peliculas_no_vistas = obtener_peliculas_no_vistas(df, usuario_objetivo)
    
    print(f"\nPelículas NO vistas por {usuario_objetivo}: {len(peliculas_no_vistas)}")
    
    # Seleccionar función de distancia
    funciones_distancia = {
        'euclidean': euclidean_distance,
        'manhattan': manhattan_distance, 
        'pearson': pearson_distance,
        'cosine': cosine_distance
    }
    
    if metrica not in funciones_distancia:
        print(f"Métrica no válida. Opciones: {list(funciones_distancia.keys())}")
        return
    
    # Crear calculador KNN
    knn_calculator = KNNCalcularDistancia(funciones_distancia[metrica])
    
    # Obtener K vecinos más cercanos
    print(f"\n=== BUSCANDO {k} VECINOS MÁS CERCANOS (métrica: {metrica}) ===")
    vecinos_cercanos = knn_calculator.get_knn(df, usuario_objetivo, k)
    
    print("Vecinos más cercanos:")
    for i, (vecino, distancia) in enumerate(vecinos_cercanos.iterrows(), 1):
        print(f"{i}. {vecino} - Distancia: {distancia['Distancia']:.3f}")
    
    # Generar recomendaciones basadas en los vecinos
    print(f"\n=== RECOMENDACIONES BASADAS EN VECINOS ===")
    
    recomendaciones = {}
    
    for vecino, _ in vecinos_cercanos.iterrows():
        print(f"\n--- Analizando vecino: {vecino} ---")
        
        # Películas vistas por el vecino que el usuario objetivo NO ha visto
        for pelicula in peliculas_no_vistas:
            rating_vecino = df.loc[pelicula, vecino]
            
            if not pd.isna(rating_vecino):  # Si el vecino vio esta película
                if pelicula not in recomendaciones:
                    recomendaciones[pelicula] = []
                recomendaciones[pelicula].append((vecino, rating_vecino))
                print(f"  {pelicula} - {rating_vecino} (visto por {vecino})")
    
    # Mostrar recomendaciones finales
    if recomendaciones:
        print(f"\n{'='*50}")
        print("RECOMENDACIONES FINALES:")
        print(f"{'='*50}")
        
        # Ordenar por número de vecinos que la recomiendan y rating promedio
        recomendaciones_ordenadas = {}
        for pelicula, ratings in recomendaciones.items():
            num_recomendaciones = len(ratings)
            rating_promedio = sum(r[1] for r in ratings) / num_recomendaciones
            recomendaciones_ordenadas[pelicula] = {
                'rating_promedio': rating_promedio,
                'num_recomendaciones': num_recomendaciones,
                'detalles': ratings
            }
        
        # Ordenar por rating promedio descendente
        peliculas_recomendadas = sorted(
            recomendaciones_ordenadas.items(),
            key=lambda x: (x[1]['rating_promedio'], x[1]['num_recomendaciones']),
            reverse=True
        )
        
        for i, (pelicula, info) in enumerate(peliculas_recomendadas, 1):
            print(f"\n{i}. {pelicula}")
            print(f"   Rating promedio: {info['rating_promedio']:.2f}")
            print(f"   Recomendada por {info['num_recomendaciones']} vecino(s):")
            for vecino, rating in info['detalles']:
                print(f"     - {vecino}: {rating}")
    else:
        print("\nNo se encontraron recomendaciones basadas en los vecinos más cercanos.")

def main():
    """
    Función principal para probar el sistema de recomendación
    """
    # Cargar datos
    try:
        df = pd.read_csv('Pelis_short.csv', index_col=0)
        print("Datos cargados exitosamente!")
        print(f"Usuarios disponibles: {list(df.columns)}")
        print(f"Películas en la base de datos: {len(df)}")
    except FileNotFoundError:
        print("Error: No se encontró el archivo Pelis_short.csv")
        return
    
    print("\n" + "="*60)
    print("SISTEMA DE RECOMENDACIÓN DE PELÍCULAS")
    print("="*60)
    
    # Seleccionar usuario
    print(f"\nUsuarios disponibles: {', '.join(df.columns)}")
    usuario = input("\nIngresa el nombre del usuario: ").strip()
    
    if usuario not in df.columns:
        print(f"Error: {usuario} no está en la base de datos")
        return
    
    # Seleccionar número de vecinos
    try:
        k = int(input("¿Cuántos vecinos más cercanos usar? (por defecto 5): ") or "5")
    except ValueError:
        k = 5
    
    # Seleccionar métrica
    print("\nMétricas disponibles:")
    print("1. euclidean (Distancia Euclidiana)")
    print("2. manhattan (Distancia Manhattan)")
    print("3. pearson (Distancia Pearson)")
    print("4. cosine (Distancia Coseno)")
    
    metricas = ['euclidean', 'manhattan', 'pearson', 'cosine']
    try:
        opcion = int(input("Selecciona una métrica (1-4): ") or "1") - 1
        metrica = metricas[opcion] if 0 <= opcion < 4 else 'euclidean'
    except ValueError:
        metrica = 'euclidean'
    
    # Generar recomendaciones
    recomendar_peliculas_knn(df, usuario, k, metrica)
    
    # Opción para probar otro usuario
    while True:
        continuar = input("\n¿Quieres probar con otro usuario? (s/n): ").lower()
        if continuar != 's':
            break
        
        usuario = input("Ingresa el nombre del usuario: ").strip()
        if usuario in df.columns:
            recomendar_peliculas_knn(df, usuario, k, metrica)
        else:
            print(f"Error: {usuario} no está en la base de datos")

if __name__ == "__main__":
    main()