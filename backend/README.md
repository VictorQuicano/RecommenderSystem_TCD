# 📚 Descripción EndPoints

Esta API expone diversos endpoints para sistemas de recomendación basados en películas. Incluye métodos KNN personalizados, recomendaciones por vecinos, filtrado por género, e información detallada sobre el sistema.

> **Importante:**
>
> - Los endpoints bajo `/recommender` y `/knn` utilizan el dataset **`Movie_Ratings.csv`**.
> - Los endpoints bajo `/movie_lens` utilizan **`MovieLens32.zip`**.

### ⚙️ Ejecución del Proyecto

> 📌 **Nota:** Para ejecutar el proyecto, ubícate en el directorio `backend` y luego ejecuta:

```bash
cd backend
./run.sh
```

## 🤖 Recomendador KNN

> **Ruta:** `{base_url}/recommender/`

Recomienda películas al usuario especificado utilizando el algoritmo KNN con una métrica de distancia y umbral configurables.

**Parámetros de entrada:**

- `user` (str): Nombre del usuario (columna del DataFrame).
- `k` (int): Número de vecinos a considerar.
- `dataset` (str, default: `"Movie_Ratings.csv"`): Dataset a utilizar.
- `distance` (str, default: `"euclidean"`): Métrica de distancia (`"euclidean"`, `"manhattan"`, `"cosine"`, etc.).
- `umbral` (float): Umbral mínimo de coincidencia para generar recomendaciones.

**Respuesta:**

```json
[
  {"movie": "Inception", "score": 4.75},
  ...
]
```

---

## 👥 Vecinos usando KNN

> **Ruta:** `{base_url}/knn/`

Obtiene los vecinos más cercanos a un usuario usando KNN, con la métrica de distancia especificada.

**Parámetros de entrada:**

- `user` (str): Nombre del usuario (columna del DataFrame).
- `k` (int): Número de vecinos.
- `dataset` (str, default: `"Movie_Ratings.csv"`): Dataset a utilizar.
- `distance` (str, default: `"euclidean"`): Métrica de distancia.

**Respuesta:**

```json
[
  {"neighbor": "usuario123", "distance": 0.8723},
  ...
]
```

---

## 📽️ MovieLens32 - Endpoints

Esta API proporciona funcionalidades del sistema de recomendación basado en el dataset MovieLens. Las rutas expuestas permiten consultar información del sistema, buscar películas, obtener vecinos similares, recomendaciones generales o por género, y registrar valoraciones de nuevos usuarios.

> 📌 **Prefijo base:** `{base_url}/movie_lens`

---

### 🔍 `GET /info`

**Descripción:**
Obtiene un resumen detallado del estado y rendimiento del sistema de recomendación.

**Entrada:**
Sin parámetros.

**Salida:**

```json
{
  "general": {
    "metricas_disponibles": ["cosine", "euclidean", ...],
    "tiempos_entrenamiento": {"cosine": "1.23 segundos", ...}
  },
  "dataset": {
    "total_usuarios": 610,
    "total_peliculas": 9724,
    ...
  },
  "memoria": {...},
  "almacenamiento": {...},
  "rendimiento": {...}
}
```

---

### 👥 `GET /vecinos`

**Descripción:**
Retorna los **usuarios más similares** a un usuario dado según una métrica de distancia.

**Entrada:**

- `user_id` (int): ID del usuario.
- `metric` (str): `"cosine"`, `"euclidean"` o `"manhattan"`.
- `k` (int): Número de vecinos deseados.

**Salida:**

```json
{
  "time_ms": 12.34,
  "vecinos": [
    {"user_id": 58, "proximidad": 0.873},
    ...
  ]
}
```

---

### ➕ `POST /nuevo`

**Descripción:**
Agrega un nuevo usuario (o actualiza uno existente) con sus valoraciones.

**Entrada (JSON):**

```json
{
  "1": 4.0,
  "32": 5.0,
  "589": 3.0
}
```

**Salida:**

```json
{
  "user_id": 612,
  "tiempos_entrenamiento": [
    {"metrica": "cosine", "tiempo_ms": 345.67},
    ...
  ]
}
```

---

### 🎬 `GET /recomendar`

**Descripción:**
Recomienda películas para un usuario basadas en vecinos similares.

**Entrada:**

- `user_id` (int): ID del usuario.
- `metric` (str): `"cosine"`, `"euclidean"`, `"manhattan"`.
- `top_k` (int): Número de vecinos a considerar.
- `top_n` (int): Número de películas a recomendar.

**Salida:**
Lista de películas recomendadas ordenadas por rating bayesiano.

---

### 🎞️ `GET /recomendar/genero`

**Descripción:**
Recomienda películas de un género específico para un usuario.

**Entrada:**

- `user_id` (int)
- `genero_objetivo` (str): Género a filtrar (ej. `"Action"`, `"Comedy"`).
- `metric` (str): `"cosine"`, etc.
- `top_k` (int)
- `top_n` (int)

**Salida:**
Películas recomendadas de ese género, ordenadas por popularidad ajustada.

---

### 🔎 `GET /buscar`

**Descripción:**
Busca películas por **nombre parcial** y/o **género exacto**.

**Entrada:**

- `nombre` (str, opcional): Parte del título (mín. 3 caracteres).
- `genero` (str, opcional): Género exacto (ej. `"Action"`).
- `top_n` (int): Límite de resultados (default 10).

**Salida:**

```json
{
  "count": 2,
  "results": [
    {"movie_id": 1, "title": "Toy Story (1995)", "rating_bayes": 4.32},
    ...
  ]
}
```
