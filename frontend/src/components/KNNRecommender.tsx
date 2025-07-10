import { useState } from "react";
import { apiService } from "../services/api";

interface Recommendation {
  movie: string;
  score: number;
}

export function KNNRecommender() {
  const [formData, setFormData] = useState({
    user: '',
    k: 5,
    dataset: 'Movie_Ratings.csv',
    distance: 'euclidean',
    umbral: 0.5
  });
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.user.trim()) {
      setError('Por favor, ingresa un nombre de usuario');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const data = await apiService.getKNNRecommendations(formData);
      setRecommendations(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al obtener recomendaciones');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'k' ? parseInt(value) : name === 'umbral' ? parseFloat(value) : value
    }));
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">🤖 Recomendador KNN</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Usuario
            </label>
            <input
              type="text"
              name="user"
              value={formData.user}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Nombre del usuario"
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
              Umbral
            </label>
            <input
              type="number"
              name="umbral"
              value={formData.umbral}
              onChange={handleInputChange}
              min="0"
              max="1"
              step="0.1"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Dataset
            </label>
            <select
              name="dataset"
              value={formData.dataset}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="Movie_Ratings.csv">Movie_Ratings.csv</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Métrica de distancia
            </label>
            <select
              name="distance"
              value={formData.distance}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="euclidean">Euclidean</option>
              <option value="manhattan">Manhattan</option>
              <option value="cosine">Cosine</option>
              <option value="pearson">Pearson</option>
            </select>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full md:w-auto px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? 'Obteniendo recomendaciones...' : 'Obtener Recomendaciones'}
        </button>
      </form>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <div className="text-red-700">❌ {error}</div>
        </div>
      )}

      {recommendations.length > 0 && (
        <div className="bg-green-50 border border-green-200 rounded-md p-4">
          <h3 className="text-lg font-semibold text-green-900 mb-3">
            🎬 Recomendaciones para {formData.user}
          </h3>
          <div className="space-y-2">
            {recommendations.map((rec, index) => (
              <div key={index} className="flex justify-between items-center bg-white p-3 rounded shadow-sm">
                <span className="font-medium text-gray-900">{rec.movie}</span>
                <span className="text-green-600 font-bold">
                  {rec.score.toFixed(2)}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
