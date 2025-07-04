// src/services/fetch_matrix.ts
import { useGlobalStore } from "@/store/store";

export async function fetch_matrix() {
  const dataset = useGlobalStore.getState().dataset;

  try {
    const res = await fetch(`http://localhost:5000/matrix?dataset=${encodeURIComponent(dataset)}`);
    const data = await res.json();

    if (
      data &&
      Array.isArray(data.columns) &&
      Array.isArray(data.data)
    ) {
      return data;
    } else {
      throw new Error("Formato inválido");
    }
  } catch (err) {
    console.warn("❌ Error al obtener matriz:", err);
    return {
      columns: [],
      data: [],
    };
  }
}
