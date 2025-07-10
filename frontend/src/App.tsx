import { useState } from "react";
import { SystemInfo } from "./components/SystemInfo";
import { KNNRecommender } from "./components/KNNRecommender";
import { KNNNeighbors } from "./components/KNNNeighbors";
import { MovieLensRecommender } from "./components/MovieLensRecommender";
import { MovieLensNeighbors } from "./components/MovieLensNeighbors";
import { MovieSearch } from "./components/MovieSearch";
import { NewUserForm } from "./components/NewUserForm";

function App() {
  const [activeTab, setActiveTab] = useState<string>("system-info");

  const tabs = [
    { id: "system-info", label: "📊 Info del Sistema", component: SystemInfo },
    { id: "knn-recommender", label: "🤖 Recomendador KNN", component: KNNRecommender },
    { id: "knn-neighbors", label: "👥 Vecinos KNN", component: KNNNeighbors },
    { id: "movielens-recommender", label: "🎬 MovieLens Recomendador", component: MovieLensRecommender },
    { id: "movielens-neighbors", label: "👥 MovieLens Vecinos", component: MovieLensNeighbors },
    { id: "movie-search", label: "🔍 Buscar Películas", component: MovieSearch },
    { id: "new-user", label: "➕ Nuevo Usuario", component: NewUserForm },
  ];

  const ActiveComponent = tabs.find(tab => tab.id === activeTab)?.component || SystemInfo;

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-7xl mx-auto px-4 py-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Sistema de Recomendación de Películas</h1>
        
        {/* Pestañas */}
        <div className="flex flex-wrap gap-2 mb-6">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                activeTab === tab.id
                  ? "bg-blue-600 text-white"
                  : "bg-white text-gray-700 hover:bg-gray-50 border border-gray-200"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Contenido activo */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <ActiveComponent />
        </div>
      </div>
    </div>
  );
}

export default App;
