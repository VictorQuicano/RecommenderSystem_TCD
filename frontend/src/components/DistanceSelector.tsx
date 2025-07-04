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

export function DistanceSelector() {
  const distance = useGlobalStore((state) => state.distance);
  const setDistance = useGlobalStore((state) => state.setDistance);

  return (
    <Card className="p-6 font-sans shadow-md rounded-2xl w-full">
      <CardHeader>
        <CardTitle className="text-xl">📐 Tipo de Distancia</CardTitle>
      </CardHeader>
      <CardContent>
        <label className="block mb-2 text-sm font-medium">Distancia a utilizar</label>
        <Select value={distance} onValueChange={setDistance}>
          <SelectTrigger className="w-full">
            <SelectValue placeholder="Selecciona una distancia" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="euclidean">Euclidean</SelectItem>
            <SelectItem value="manhattan">Manhattan</SelectItem>
            <SelectItem value="pearson">Pearson</SelectItem>
            <SelectItem value="cosine">Coseno</SelectItem>
          </SelectContent>
        </Select>
      </CardContent>
    </Card>
  );
}
