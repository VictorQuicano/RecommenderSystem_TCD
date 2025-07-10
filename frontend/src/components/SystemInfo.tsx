import { useState, useEffect } from "react";
import { apiService } from "../services/api";

interface SystemInfoData {
  general: {
    metricas_disponibles: string[];
    tiempos_entrenamiento: Record<string, string>;
  };
  dataset: {
    total_usuarios: number;
    total_peliculas: number;
    total_valoraciones: string;
    espacios_vacios: string;
    compresion_datos: string;
  };
  memoria: {
    total_uso_memoria: string;
    desglose: Record<string, string>;
  };
  almacenamiento: {
    total_disco: string;
    desglose: Record<string, string>;
  };
  rendimiento: {
    ratio_memoria_disco: string;
    overhead_modelos: string;
  };
}

export function SystemInfo() {
  const [systemInfo, setSystemInfo] = useState<SystemInfoData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchSystemInfo = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiService.getSystemInfo();
      setSystemInfo(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al obtener información del sistema");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSystemInfo();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <div className="text-red-600 mb-4">❌ {error}</div>
        <button
          onClick={fetchSystemInfo}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Reintentar
        </button>
      </div>
    );
  }

  if (!systemInfo) {
    return <div className="text-center py-8">No hay información disponible</div>;
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Información General */}
        <div className="bg-blue-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-blue-900 mb-3">📊 General</h3>
          <div className="space-y-2">
            <div>
              <span className="font-medium">Métricas disponibles:</span>
              <div className="flex flex-wrap gap-1 mt-1">
                {systemInfo.general.metricas_disponibles.map((metric) => (
                  <span key={metric} className="bg-blue-200 text-blue-800 px-2 py-1 rounded text-sm">
                    {metric}
                  </span>
                ))}
              </div>
            </div>
            <div>
              <span className="font-medium">Tiempos de entrenamiento:</span>
              <div className="mt-1 space-y-1">
                {Object.entries(systemInfo.general.tiempos_entrenamiento).map(([metric, time]) => (
                  <div key={metric} className="text-sm">
                    <span className="font-medium">{metric}:</span> {time}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Información del Dataset */}
        <div className="bg-green-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-green-900 mb-3">📚 Dataset</h3>
          <div className="space-y-2">
            <div>
              <span className="font-medium">Total usuarios:</span>
              <span className="ml-2 text-lg font-bold text-green-700">
                {systemInfo.dataset.total_usuarios.toLocaleString()}
              </span>
            </div>
            <div>
              <span className="font-medium">Total películas:</span>
              <span className="ml-2 text-lg font-bold text-green-700">
                {systemInfo.dataset.total_peliculas.toLocaleString()}
              </span>
            </div>
            <div>
              <span className="font-medium">Total valoraciones:</span>
              <span className="ml-2 text-lg font-bold text-green-700">
                {systemInfo.dataset.total_valoraciones}
              </span>
            </div>
            <div>
              <span className="font-medium">Espacios vacíos:</span>
              <span className="ml-2 text-green-700">
                {systemInfo.dataset.espacios_vacios}
              </span>
            </div>
            <div>
              <span className="font-medium">Compresión de datos:</span>
              <span className="ml-2 text-green-700">
                {systemInfo.dataset.compresion_datos}
              </span>
            </div>
          </div>
        </div>

        {/* Información de Memoria */}
        <div className="bg-purple-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-purple-900 mb-3">💾 Memoria</h3>
          <div className="space-y-2">
            <div>
              <span className="font-medium">Uso total:</span>
              <span className="ml-2 text-lg font-bold text-purple-700">
                {systemInfo.memoria.total_uso_memoria}
              </span>
            </div>
            <div className="mt-3">
              <span className="font-medium text-sm">Desglose:</span>
              <div className="mt-1 space-y-1">
                {Object.entries(systemInfo.memoria.desglose).map(([key, value]) => (
                  <div key={key} className="text-xs flex justify-between">
                    <span className="font-medium capitalize">
                      {key.replace(/_/g, ' ')}:
                    </span>
                    <span className="text-purple-600 font-semibold">{value}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Información adicional */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-orange-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-orange-900 mb-3">💽 Almacenamiento</h3>
          <div className="space-y-2">
            <div>
              <span className="font-medium">Uso total en disco:</span>
              <span className="ml-2 text-lg font-bold text-orange-700">
                {systemInfo.almacenamiento.total_disco}
              </span>
            </div>
            <div className="mt-3">
              <span className="font-medium text-sm">Desglose:</span>
              <div className="mt-1 space-y-1">
                {Object.entries(systemInfo.almacenamiento.desglose).map(([key, value]) => (
                  <div key={key} className="text-xs flex justify-between">
                    <span className="font-medium capitalize">
                      {key.replace(/_/g, ' ')}:
                    </span>
                    <span className="text-orange-600 font-semibold">{value}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="bg-red-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-red-900 mb-3">⚡ Rendimiento</h3>
          <div className="space-y-2">
            <div>
              <span className="font-medium">Ratio memoria/disco:</span>
              <span className="ml-2 text-red-700">
                {systemInfo.rendimiento.ratio_memoria_disco}
              </span>
            </div>
            <div>
              <span className="font-medium">Overhead de modelos:</span>
              <span className="ml-2 text-red-700">
                {systemInfo.rendimiento.overhead_modelos}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="flex justify-center">
        <button
          onClick={fetchSystemInfo}
          className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
        >
          🔄 Actualizar Información
        </button>
      </div>
    </div>
  );
}
