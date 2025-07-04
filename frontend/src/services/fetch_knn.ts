import { useGlobalStore } from "@/store/store"; // ajusta la ruta según tu estructura

export async function fetchKNN(user: string, k: number): Promise<any[]> {
  const { dataset, distance } = useGlobalStore.getState(); // obtenemos directamente los valores

  try {
    const response = await fetch(
      `http://localhost:5000/knn?user=${encodeURIComponent(user)}&k=${k}&dataset=${encodeURIComponent(
        dataset
      )}&distance=${encodeURIComponent(distance)}`
    );

    const data = await response.json();

    // Validamos el formato
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
    return [
      { neighbor: "Heather", distance: 2.3 },
      { neighbor: "Bryan", distance: 4.1 },
    ];
  }
}
