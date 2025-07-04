"use client";

import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useGlobalStore } from "@/store/store";

const datasets = [
  { label: "Movie_Ratings", value: "Movie_Ratings.csv" },
  { label: "Pelis_short", value: "Pelis_short.csv" },
];

export function DatasetSelector() {
  const dataset = useGlobalStore((state) => state.dataset);
  const setDataset = useGlobalStore((state) => state.setDataset);

  return (
    <Card className="font-sans shadow-md rounded-2xl w-full">
      <CardHeader>
        <CardTitle className="text-xl">📁 Seleccionar Dataset</CardTitle>
      </CardHeader>
      <CardContent>
        <label className="block mb-2 text-sm font-medium">Dataset disponible</label>
        <Select value={dataset} onValueChange={setDataset}>
          <SelectTrigger className="w-full">
            <SelectValue placeholder="Selecciona un dataset">
              {datasets.find((d) => d.value === dataset)?.label}
            </SelectValue>
          </SelectTrigger>
          <SelectContent>
            {datasets.map((ds) => (
              <SelectItem key={ds.value} value={ds.value}>
                {ds.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </CardContent>
    </Card>
  );
}
