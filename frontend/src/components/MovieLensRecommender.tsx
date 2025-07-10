import { useState } from "react";
import { apiService } from "../services/api";

interface MovieRecommendation {
  movie_id: number;
  title: string;
  rating_bayes: number;
  genres?: string[];
}

// Función auxiliar para convertir la respuesta del backend
const convertBackendResponse = (backendData: any[]): MovieRecommendation[] => {
  if (!Array.isArray(backendData)) {
    return [];
  }
  
  return backendData.map(item => {
    if (Array.isArray(item)) {
      // Formato: [movie_id, title, rating_bayes] o [movie_id, title, genres, rating_bayes]
      return {
        movie_id: item[0] || 0,
        title: item[1] || 'Título desconocido',
        rating_bayes: item.length > 3 ? (item[3] || 0) : (item[2] || 0),
        genres: item.length > 3 ? item[2] : undefined
      };
    } else if (typeof item === 'object' && item !== null) {
      // Formato objeto: {movie_id, title, rating_bayes, etc.}
      return {
        movie_id: item.movie_id || 0,
        title: item.title || 'Título desconocido',
        rating_bayes: item.rating_bayes || item.bayesian_rating || 0,
        genres: item.genres
      };
    }
    
    return {
      movie_id: 0,
      title: 'Título desconocido',
      rating_bayes: 0
    };
  });
};

export function MovieLensRecommender() {
  const [formData, setFormData] = useState({
    user_id: 1,
    metric: 'cosine',
    top_k: 5,
    top_n: 10,
    genero_objetivo: ''
  });
  const [recommendations, setRecommendations] = useState<MovieRecommendation[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isGenreRecommendation, setIsGenreRecommendation] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      let data;
      if (isGenreRecommendation && formData.genero_objetivo.trim()) {
        data = await apiService.getMovieLensRecommendationsByGenre({
          user_id: formData.user_id,
          genero_objetivo: formData.genero_objetivo,
          metric: formData.metric,
          top_k: formData.top_k,
          top_n: formData.top_n
        });
      } else {
        data = await apiService.getMovieLensRecommendations({
          user_id: formData.user_id,
          metric: formData.metric,
          top_k: formData.top_k,
          top_n: formData.top_n
        });
      }
      
      // Extraer las recomendaciones del objeto de respuesta
      const recommendationsArray = data.recommendations || data;
      const convertedData = convertBackendResponse(recommendationsArray);
      
      setRecommendations(convertedData);
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
      [name]: ['user_id', 'top_k', 'top_n'].includes(name) ? 
        (value === '' ? 0 : parseInt(value) || 0) : 
        value
    }));
  };

  const commonGenres = [
    'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime',
    'Documentary', 'Drama', 'Fantasy', 'Horror', 'Musical', 'Mystery',
    'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'
  ];

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">🎬 Recomendador MovieLens</h2>
      
      <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4">
        <div className="flex items-center space-x-2 mb-2">
          <input
            type="checkbox"
            id="genreRecommendation"
            checked={isGenreRecommendation}
            onChange={(e) => setIsGenreRecommendation(e.target.checked)}
            className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
          />
          <label htmlFor="genreRecommendation" className="text-sm font-medium text-gray-700">
            Filtrar por género específico
          </label>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
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
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Métrica
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

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Vecinos (top_k)
            </label>
            <input
              type="number"
              name="top_k"
              value={formData.top_k}
              onChange={handleInputChange}
              min="1"
              max="50"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Recomendaciones (top_n)
            </label>
            <input
              type="number"
              name="top_n"
              value={formData.top_n}
              onChange={handleInputChange}
              min="1"
              max="50"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {isGenreRecommendation && (
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Género objetivo
              </label>
              <select
                name="genero_objetivo"
                value={formData.genero_objetivo}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required={isGenreRecommendation}
              >
                <option value="">Seleccionar género</option>
                {commonGenres.map(genre => (
                  <option key={genre} value={genre}>{genre}</option>
                ))}
              </select>
            </div>
          )}
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
            🎬 Recomendaciones para Usuario {formData.user_id}
            {isGenreRecommendation && formData.genero_objetivo && (
              <span className="text-sm font-normal"> (Género: {formData.genero_objetivo})</span>
            )}
          </h3>
          <div className="space-y-2">
            {recommendations.map((movie) => (
              <div key={movie.movie_id} className="flex justify-between items-center bg-white p-3 rounded shadow-sm">
                <div className="flex-1">
                  <span className="font-medium text-gray-900">{movie.title}</span>
                  <div className="text-sm text-gray-500">
                    ID: {movie.movie_id}
                    {movie.genres && <span className="ml-2">Géneros: {movie.genres}</span>}
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-green-600 font-bold">
                    {movie.rating_bayes ? movie.rating_bayes.toFixed(2) : 'N/A'}
                  </span>
                  <div className="text-sm text-gray-500">Rating Bayesiano</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
