import { useGlobalStore } from "@/store/store";

export async function fetchNames() {
  const dataset = useGlobalStore.getState().dataset;

  try {
    const response = await fetch(`http://localhost:5000?dataset=${encodeURIComponent(dataset)}`);
    const data = await response.json();

    if (Array.isArray(data) && data.every((d) => typeof d === "string")) {
      useGlobalStore.getState().setUsers(data);
    } else {
      throw new Error("Formato inválido");
    }
  } catch (error) {
    console.warn("❌ Error al obtener nombres, usando datos por defecto:", error);
    useGlobalStore.getState().setUsers([
      "Patrick C",
      "Heather",
      "Bryan",
      "Patrick T",
      "Thomas",
      "aaron",
    ]);
  }
}
