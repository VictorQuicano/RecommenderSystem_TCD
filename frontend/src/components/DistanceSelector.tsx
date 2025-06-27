import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import { useGlobalStore } from "@/store/store";

export function DistanceSelector() {
  const distance = useGlobalStore((state) => state.distance);
  const setDistance = useGlobalStore((state) => state.setDistance);

  return (
    <div className="w-full max-w-sm">
      <label className="block mb-2 text-sm font-medium text-gray-700">
        Tipo de distancia
      </label>
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
    </div>
  );
}
