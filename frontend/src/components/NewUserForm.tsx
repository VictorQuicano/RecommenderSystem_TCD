import { useState } from "react";
import { apiService } from "../services/api";

interface NewUserResponse {
  user_id: number;
  tiempos_entrenamiento: Array<{
    metrica: string;
    tiempo_ms: number;
  }>;
}

export function NewUserForm() {
  const [ratings, setRatings] = useState<Record<string, number>>({});
  const [movieId, setMovieId] = useState('');
  const [rating, setRating] = useState(5);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<NewUserResponse | null>(null);

  const handleAddRating = () => {
    if (!movieId.trim()) {
      setError('Por favor, ingresa un ID de película');
      return;
    }

    if (ratings[movieId]) {
      setError('Ya has valorado esta película');
      return;
    }

    setRatings(prev => ({
      ...prev,
      [movieId]: rating
    }));
    setMovieId('');
    setRating(5);
    setError(null);
  };

  const handleRemoveRating = (movieIdToRemove: string) => {
    setRatings(prev => {
      const newRatings = { ...prev };
      delete newRatings[movieIdToRemove];
      return newRatings;
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (Object.keys(ratings).length === 0) {
      setError('Por favor, agrega al menos una valoración');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const data = await apiService.addNewUser(ratings);
      setResult(data);
      setRatings({});
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al agregar usuario');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setRatings({});
    setMovieId('');
    setRating(5);
    setError(null);
    setResult(null);
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">➕ Agregar Nuevo Usuario</h2>
      
      <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
        <p className="text-sm text-blue-700">
          💡 Agrega valoraciones de películas para crear un nuevo usuario. 
          Necesitas proporcionar el ID de la película y tu valoración (1-5).
        </p>
      </div>

      {/* Formulario para agregar valoraciones */}
      <div className="bg-gray-50 border border-gray-200 rounded-md p-4">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">Agregar Valoración</h3>
        
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              ID de la película
            </label>
            <input
              type="number"
              value={movieId}
              onChange={(e) => setMovieId(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Ej: 1, 32, 589..."
              min="1"
            />
          </div>

          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Valoración (1-5)
            </label>
            <select
              value={rating}
              onChange={(e) => setRating(parseFloat(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value={1}>1 - Muy malo</option>
              <option value={1.5}>1.5</option>
              <option value={2}>2 - Malo</option>
              <option value={2.5}>2.5</option>
              <option value={3}>3 - Regular</option>
              <option value={3.5}>3.5</option>
              <option value={4}>4 - Bueno</option>
              <option value={4.5}>4.5</option>
              <option value={5}>5 - Excelente</option>
            </select>
          </div>

          <div className="flex items-end">
            <button
              type="button"
              onClick={handleAddRating}
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
            >
              Agregar
            </button>
          </div>
        </div>
      </div>

      {/* Lista de valoraciones agregadas */}
      {Object.keys(ratings).length > 0 && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4">
          <h3 className="text-lg font-semibold text-yellow-900 mb-3">
            Valoraciones agregadas ({Object.keys(ratings).length})
          </h3>
          
          <div className="space-y-2">
            {Object.entries(ratings).map(([movieId, rating]) => (
              <div key={movieId} className="flex justify-between items-center bg-white p-3 rounded shadow-sm">
                <div>
                  <span className="font-medium text-gray-900">Película ID: {movieId}</span>
                  <span className="ml-4 text-yellow-600 font-bold">
                    ⭐ {rating}
                  </span>
                </div>
                <button
                  onClick={() => handleRemoveRating(movieId)}
                  className="text-red-600 hover:text-red-800 text-sm"
                >
                  ❌ Eliminar
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <div className="text-red-700">❌ {error}</div>
        </div>
      )}

      {/* Botones de acción */}
      <div className="flex space-x-2">
        <button
          onClick={handleSubmit}
          disabled={loading || Object.keys(ratings).length === 0}
          className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? 'Agregando usuario...' : 'Agregar Usuario'}
        </button>
        
        <button
          type="button"
          onClick={handleClear}
          className="px-6 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600 transition-colors"
        >
          Limpiar Todo
        </button>
      </div>

      {/* Resultado */}
      {result && (
        <div className="bg-green-50 border border-green-200 rounded-md p-4">
          <h3 className="text-lg font-semibold text-green-900 mb-3">
            ✅ Usuario agregado exitosamente
          </h3>
          
          <div className="space-y-3">
            <div className="bg-white p-3 rounded shadow-sm">
              <span className="font-medium text-gray-900">ID del nuevo usuario: </span>
              <span className="text-green-600 font-bold text-lg">{result.user_id}</span>
            </div>

            <div className="bg-white p-3 rounded shadow-sm">
              <span className="font-medium text-gray-900 block mb-2">Tiempos de entrenamiento:</span>
              <div className="space-y-1">
                {result.tiempos_entrenamiento.map((tiempo, index) => (
                  <div key={index} className="text-sm">
                    <span className="font-medium">{tiempo.metrica}:</span>
                    <span className="ml-2">{tiempo.tiempo_ms.toFixed(2)} ms</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
