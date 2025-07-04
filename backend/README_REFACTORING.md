# Backend Refactorizado - Documentación

## ✨ Resumen de la Refactorización

El backend ha sido completamente refactorizado aplicando los principios SOLID y mejores prácticas de desarrollo. La funcionalidad original se mantiene intacta, pero ahora el código es más mantenible, testeable y extensible.

## 🏗️ Arquitectura SOLID Implementada

### 1. Single Responsibility Principle (SRP)
- **DistanceCalculators**: Cada calculadora tiene una sola responsabilidad
- **Services**: Cada servicio maneja un dominio específico
- **Repository**: Solo maneja acceso a datos

### 2. Open/Closed Principle (OCP)
- **DistanceCalculatorFactory**: Permite agregar nuevas métricas sin modificar código existente
- **Interfaces**: Permiten nuevas implementaciones sin cambiar dependientes

### 3. Liskov Substitution Principle (LSP)
- Todas las implementaciones de `IDistanceCalculator` son intercambiables
- Los servicios pueden usar cualquier implementación de sus dependencias

### 4. Interface Segregation Principle (ISP)
- Interfaces específicas para cada responsabilidad:
  - `IDistanceCalculator`, `IDataRepository`, `IKnnService`, etc.

### 5. Dependency Inversion Principle (DIP)
- El código depende de abstracciones (interfaces), no de concreciones
- Inyección de dependencias a través del `Container`

## 📁 Nueva Estructura

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Configuración de FastAPI
│   ├── core/
│   │   ├── __init__.py
│   │   ├── interfaces.py          # Interfaces/Abstracciones
│   │   ├── config.py              # Configuración
│   │   ├── distance_calculators.py # Implementaciones de distancias
│   │   ├── distance_factory.py    # Factory para calculadoras
│   │   └── container.py           # Contenedor de DI
│   ├── models/
│   │   ├── __init__.py
│   │   └── enums.py               # Enumeraciones
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── data_repository.py     # Acceso a datos
│   ├── services/
│   │   ├── __init__.py
│   │   ├── distance_service.py    # Servicio de distancias
│   │   ├── knn_service.py         # Servicio KNN
│   │   └── matrix_service.py      # Servicio de matrices
│   └── api/
│       ├── __init__.py
│       └── routes/
│           ├── __init__.py
│           └── data.py            # Rutas de la API
├── tests/
│   ├── __init__.py
│   ├── test_distance_calculators.py
│   ├── test_services.py
│   └── test_api.py
├── main.py                        # Punto de entrada
├── test_setup.py                  # Script de verificación
└── requirements.txt
```

## 🚀 Cómo Ejecutar

### 1. Activar el entorno virtual
```bash
# Desde el directorio raíz del proyecto
cd backend
```

### 2. Ejecutar el servidor
```bash
uvicorn main:app --reload
```

El servidor estará disponible en: http://127.0.0.1:8000

## 🔗 Endpoints Disponibles

La API mantiene **exactamente la misma funcionalidad** que antes:

### Obtener usuarios de un dataset
```
GET /?dataset=Movie_Ratings.csv
```

### Obtener matriz de datos
```
GET /matrix?dataset=Movie_Ratings.csv
```

### Comparar dos usuarios
```
GET /compare?u1=Heather&u2=Thomas&metric=euclidean&dataset=Movie_Ratings.csv
```

### Obtener vecinos más cercanos (KNN)
```
GET /knn?user=Heather&k=5&dataset=Movie_Ratings.csv&distance=euclidean
```

### Nuevos endpoints adicionales
```
GET /datasets          # Lista de datasets disponibles
GET /metrics           # Lista de métricas disponibles
```

## 🧪 Ejecutar Pruebas

```bash
# Verificación básica del sistema
python test_setup.py

# Pruebas unitarias
python -m unittest tests.test_distance_calculators -v
python -m unittest tests.test_services -v
```

## 📊 Documentación Interactiva

Visita http://127.0.0.1:8000/docs para ver la documentación interactiva de Swagger UI.

## 🔧 Extensibilidad

### Agregar nueva métrica de distancia

1. Crear nueva clase que implemente `IDistanceCalculator`:
```python
class MyNewDistanceCalculator(IDistanceCalculator):
    def calculate(self, vector1: List[float], vector2: List[float]) -> float:
        # Tu implementación aquí
        pass
    
    @property
    def name(self) -> str:
        return "mynew"
```

2. Registrarla en `DistanceCalculatorFactory`:
```python
self._calculators["mynew"] = MyNewDistanceCalculator()
```

### Agregar nuevo servicio

1. Definir interface en `interfaces.py`
2. Implementar el servicio
3. Registrarlo en el `Container`
4. Usarlo en las rutas de la API

## ✅ Beneficios de la Refactorización

- **Mantenibilidad**: Código más organizado y fácil de modificar
- **Testabilidad**: Cada componente es fácilmente testeable
- **Extensibilidad**: Fácil agregar nuevas funcionalidades
- **Reutilización**: Componentes reutilizables
- **Separación de responsabilidades**: Cada clase tiene un propósito específico
- **Inyección de dependencias**: Mejor acoplamiento y testabilidad
- **Configuración centralizada**: Fácil modificar configuraciones

## 🔍 Migración desde el código anterior

No se requiere migración del frontend. Todos los endpoints mantienen **exactamente la misma interfaz** que antes. El frontend seguirá funcionando sin cambios.

La única diferencia es que ahora el código del backend es mucho más limpio, organizado y fácil de mantener.
