import { create } from "zustand";

type GlobalStore = {
  users: string[];
  setUsers: (names: string[]) => void;

  distance: string;
  setDistance: (dist: string) => void;

  dataset: string;
  setDataset: (ds: string) => void;
};

export const useGlobalStore = create<GlobalStore>((set) => ({
  users: [],
  setUsers: (names) => set({ users: names }),

  distance: "euclidean",
  setDistance: (dist) => set({ distance: dist }),

  dataset: "Movie_Ratings.csv",
  setDataset: (ds) =>
    set({
      dataset: ds,
      users: [], // ← Limpiar usuarios al cambiar el dataset
    }),
}));
