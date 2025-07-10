import { useState } from "react";
import { apiService } from "../services/api";

interface Movie {
  movie_id: number;
  title: string;
  bayesian_rating?: number;
  genres?: string;
}

interface SearchResponse {
  count: number;
  results: Movie[];
}

export function MovieSearch() {
  const [formData, setFormData] = useState({
    nombre: '',
    genero: '',
    top_n: 10
  });
  const [searchResults, setSearchResults] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.nombre.trim() && !formData.genero.trim()) {
      setError('Por favor, ingresa un nombre de película o selecciona un género');
      return;
    }

    if (formData.nombre.trim() && formData.nombre.trim().length < 3) {
      setError('El nombre debe tener al menos 3 caracteres');
      return;
    }

    setLoading(true);
    setError(null);
    setSearchResults(null); // Limpiar resultados anteriores
    
    try {
      const params: any = { top_n: formData.top_n };
      if (formData.nombre.trim()) params.nombre = formData.nombre.trim();
      if (formData.genero.trim()) params.genero = formData.genero.trim();
      
      const data = await apiService.searchMovies(params);
      
      // Verificar que la respuesta tenga la estructura correcta
      if (!data || !data.results || !Array.isArray(data.results)) {
        throw new Error('Respuesta del servidor con formato incorrecto');
      }
      
      setSearchResults(data);
    } catch (err) {
      console.error('Error en búsqueda de películas:', err);
      setError(err instanceof Error ? err.message : 'Error al buscar películas');
      setSearchResults(null);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'top_n' ? parseInt(value) : value
    }));
    
    // Limpiar error cuando el usuario empieza a escribir
    if (error) {
      setError(null);
    }
  };

  const handleClear = () => {
    setFormData({ nombre: '', genero: '', top_n: 10 });
    setSearchResults(null);
    setError(null);
  };

  const commonGenres = [
    'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime',
    'Documentary', 'Drama', 'Fantasy', 'Horror', 'Musical', 'Mystery',
    'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'
  ];

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">🔍 Buscar Películas</h2>
      
      <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
        <p className="text-sm text-blue-700">
          💡 Puedes buscar por nombre parcial (mínimo 3 caracteres), género exacto, o ambos criterios.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Nombre de la película
            </label>
            <input
              type="text"
              name="nombre"
              value={formData.nombre}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Ej: Toy Story, Matrix..."
              minLength={3}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Género
            </label>
            <select
              name="genero"
              value={formData.genero}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Todos los géneros</option>
              {commonGenres.map(genre => (
                <option key={genre} value={genre}>{genre}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Límite de resultados
            </label>
            <input
              type="number"
              name="top_n"
              value={formData.top_n}
              onChange={handleInputChange}
              min="1"
              max="100"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        <div className="flex space-x-2">
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Buscando...' : 'Buscar'}
          </button>
          
          <button
            type="button"
            onClick={handleClear}
            className="px-6 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600 transition-colors"
          >
            Limpiar
          </button>
        </div>
      </form>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <div className="text-red-700">❌ {error}</div>
        </div>
      )}

      {searchResults && (
        <div className="bg-green-50 border border-green-200 rounded-md p-4">
          <h3 className="text-lg font-semibold text-green-900 mb-3">
            🎬 Resultados de búsqueda ({searchResults.count} encontrados)
          </h3>
          
          {searchResults.results.length === 0 ? (
            <p className="text-gray-600">No se encontraron películas con los criterios especificados.</p>
          ) : (
            <div className="space-y-2">
              {searchResults.results.map((movie) => (
                <div key={movie.movie_id} className="flex justify-between items-center bg-white p-3 rounded shadow-sm">
                  <div className="flex-1">
                    <span className="font-medium text-gray-900">{movie.title}</span>
                    <div className="text-sm text-gray-500">ID: {movie.movie_id}</div>
                    {movie.genres && (
                      <div className="text-sm text-blue-600 mt-1">
                        Géneros: {movie.genres}
                      </div>
                    )}
                  </div>
                  <div className="text-right">
                    <span className="text-green-600 font-bold">
                      {movie.bayesian_rating != null ? movie.bayesian_rating.toFixed(2) : 'N/A'}
                    </span>
                    <div className="text-sm text-gray-500">Rating Bayesiano</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
