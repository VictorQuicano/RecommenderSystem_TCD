type KNNResult = {
  neighbor: string;
  distance: number;
};

export async function fetchKNN(user: string, k: number): Promise<KNNResult[]> {
  try {
    const response = await fetch(
      `http://localhost:5000/knn?user=${encodeURIComponent(user)}&k=${k}`
    );
    const data = await response.json();

    // Validamos que cada entrada tenga el formato correcto
    if (
      Array.isArray(data) &&
      data.every(
        (item) =>
          typeof item.neighbor === "string" && typeof item.distance === "number"
      )
    ) {
      return data;
    } else {
      throw new Error("Formato inválido");
    }
  } catch (err) {
    console.warn("⚠️ Error en fetchKNN, devolviendo mock:", err);
    // Retorno simulado
    return [
      { neighbor: "Heather", distance: 2.3 },
      { neighbor: "Bryan", distance: 4.1 },
    ];
  }
}
