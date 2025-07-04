// src/services/fetch_recommender.ts
import { useGlobalStore } from "@/store/store";

export type Recommendation = {
  movie: string;
  score: number;
  neighbor: { name: string; score: number }[];
};

export async function fetch_recommender(params: {
  user: string;
  k: number;
  umbral: number;
}) {
  const { dataset, distance } = useGlobalStore.getState();

  try {
    const res = await fetch("http://localhost:5000/recommender?" + new URLSearchParams({
      user: params.user,
      k: params.k.toString(),
      umbral: params.umbral.toString(),
      dataset,
      distance,
    }));

    if (!res.ok) throw new Error("Error en la solicitud");

    const data = await res.json();
    return data;
  } catch (err) {
    console.error("❌ Error al obtener recomendaciones:", err);
    return [];
  }
}
