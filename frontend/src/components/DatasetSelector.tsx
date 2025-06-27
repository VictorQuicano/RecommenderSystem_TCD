import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import { useGlobalStore } from "@/store/store";

const datasets = [
  { label: "Movie_Ratings", value: "Movie_Ratings.csv" },
  { label: "Pelis_short", value: "Pelis_short.csv" },
];

export function DatasetSelector() {
  const dataset = useGlobalStore((state) => state.dataset);
  const setDataset = useGlobalStore((state) => state.setDataset);

  return (
    <div className="w-full max-w-sm mt-4">
      <label className="block mb-2 text-sm font-medium text-gray-700">
        Selecciona el dataset
      </label>
      <Select value={dataset} onValueChange={setDataset}>
        <SelectTrigger className="w-full">
          <SelectValue placeholder="Selecciona un dataset">
            {datasets.find((d) => d.value === dataset)?.label}
          </SelectValue>
        </SelectTrigger>
        <SelectContent>
          {datasets.map((dataset) => (
            <SelectItem key={dataset.value} value={dataset.value}>
              {dataset.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}
