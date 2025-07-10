import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

class ApiService {
  private api = axios.create({
    baseURL: BASE_URL,
    timeout: 30000,
  });

  // Recomendador KNN
  async getKNNRecommendations(params: {
    user: string;
    k: number;
    dataset?: string;
    distance?: string;
    umbral: number;
  }) {
    const response = await this.api.get('/recommender/', { params });
    return response.data;
  }

  // Vecinos KNN
  async getKNNNeighbors(params: {
    user: string;
    k: number;
    dataset?: string;
    distance?: string;
  }) {
    const response = await this.api.get('/knn/', { params });
    return response.data;
  }

  // MovieLens - Información del sistema
  async getSystemInfo() {
    const response = await this.api.get('/movie_lens/info');
    return response.data;
  }

  // MovieLens - Obtener vecinos
  async getMovieLensNeighbors(params: {
    user_id: number;
    metric: string;
    k: number;
  }) {
    const response = await this.api.get('/movie_lens/vecinos', { params });
    return response.data;
  }

  // MovieLens - Agregar nuevo usuario
  async addNewUser(ratings: Record<string, number>) {
    const response = await this.api.post('/movie_lens/nuevo', ratings);
    return response.data;
  }

  // MovieLens - Recomendaciones
  async getMovieLensRecommendations(params: {
    user_id: number;
    metric: string;
    top_k: number;
    top_n: number;
  }) {
    const response = await this.api.get('/movie_lens/recomendar', { params });
    return response.data;
  }

  // MovieLens - Recomendaciones por género
  async getMovieLensRecommendationsByGenre(params: {
    user_id: number;
    genero_objetivo: string;
    metric: string;
    top_k: number;
    top_n: number;
  }) {
    const response = await this.api.get('/movie_lens/recomendar/genero', { params });
    return response.data;
  }

  // MovieLens - Buscar películas
  async searchMovies(params: {
    nombre?: string;
    genero?: string;
    top_n?: number;
  }) {
    const response = await this.api.get('/movie_lens/buscar', { params });
    return response.data;
  }

  // Obtener nombres de usuarios (para el dataset Movie_Ratings.csv)
  async getUserNames(dataset: string) {
    const response = await this.api.get(`/users?dataset=${encodeURIComponent(dataset)}`);
    return response.data;
  }
}

export const apiService = new ApiService();
