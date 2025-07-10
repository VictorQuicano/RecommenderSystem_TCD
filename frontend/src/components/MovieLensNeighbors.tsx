import { useState } from "react";
import { apiService } from "../services/api";

interface Neighbor {
  user_id: number;
  proximidad: number;
}

interface NeighborsResponse {
  time_ms: number;
  vecinos: Neighbor[];
}

export function MovieLensNeighbors() {
  const [formData, setFormData] = useState({
    user_id: 1,
    metric: 'cosine',
    k: 5
  });
  const [neighbors, setNeighbors] = useState<Neighbor[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [responseTime, setResponseTime] = useState<number | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.user_id <= 0) {
      setError('Por favor, ingresa un ID de usuario válido');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const data: NeighborsResponse = await apiService.getMovieLensNeighbors({
        user_id: formData.user_id,
        metric: formData.metric,
        k: formData.k
      });
      setNeighbors(data.vecinos || []);
      setResponseTime(data.time_ms || null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al obtener vecinos');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: ['user_id', 'k'].includes(name) ? 
        (value === '' ? 0 : parseInt(value) || 0) : 
        value
    }));
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">👥 Vecinos MovieLens</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              ID del Usuario
            </label>
            <input
              type="number"
              name="user_id"
              value={formData.user_id}
              onChange={handleInputChange}
              min="1"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="ID del usuario"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Número de vecinos (k)
            </label>
            <input
              type="number"
              name="k"
              value={formData.k}
              onChange={handleInputChange}
              min="1"
              max="50"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Métrica de distancia
            </label>
            <select
              name="metric"
              value={formData.metric}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="cosine">Cosine</option>
              <option value="euclidean">Euclidean</option>
              <option value="manhattan">Manhattan</option>
            </select>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full md:w-auto px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? 'Obteniendo vecinos...' : 'Obtener Vecinos'}
        </button>
      </form>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <div className="text-red-700">❌ {error}</div>
        </div>
      )}

      {neighbors.length > 0 && (
        <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
          <div className="flex justify-between items-center mb-3">
            <h3 className="text-lg font-semibold text-blue-900">
              👥 Vecinos más cercanos al Usuario {formData.user_id}
            </h3>
            {responseTime && (
              <span className="text-sm text-gray-600 bg-white px-2 py-1 rounded">
                ⏱️ {responseTime.toFixed(2)}ms
              </span>
            )}
          </div>
          <div className="space-y-2">
            {neighbors.map((neighbor, index) => (
              <div key={index} className="flex justify-between items-center bg-white p-3 rounded shadow-sm">
                <div className="flex items-center space-x-3">
                  <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-1 rounded-full">
                    #{index + 1}
                  </span>
                  <span className="font-medium text-gray-900">Usuario {neighbor.user_id}</span>
                </div>
                <span className="text-blue-600 font-bold">
                  Proximidad: {neighbor.proximidad.toFixed(4)}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
