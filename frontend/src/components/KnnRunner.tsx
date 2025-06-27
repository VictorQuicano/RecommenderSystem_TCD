import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { useGlobalStore } from "@/store/store";
import { fetchKNN } from "@/services/fetch_knn";
import { useState } from "react";

export function KNNRunner() {
  const users = useGlobalStore((state) => state.users);
  const [selectedUser, setSelectedUser] = useState("");
  const [k, setK] = useState(1);
  const [results, setResults] = useState<{ neighbor: string; distance: number }[]>([]);

  const handleRunKNN = async () => {
    if (!selectedUser || k <= 0) return;
    const res = await fetchKNN(selectedUser, k);
    setResults(res);
  };

  return (
    <div className="mt-8 space-y-4 max-w-md">
      <h2 className="text-lg font-semibold">Ejecutar KNN</h2>

      {/* Select de usuario */}
      <Select value={selectedUser} onValueChange={setSelectedUser}>
        <SelectTrigger className="w-full">
          <SelectValue placeholder="Selecciona un usuario" />
        </SelectTrigger>
        <SelectContent>
          {users.map((u, idx) => (
            <SelectItem key={idx} value={u}>
              {u}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>

      {/* Input numérico para k */}
      <Input
        type="number"
        min={1}
        max={users.length - 1}
        value={k}
        onChange={(e) => setK(Number(e.target.value))}
        placeholder="Número de vecinos"
      />

      {/* Botón para ejecutar */}
      <button
        onClick={handleRunKNN}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Ejecutar KNN
      </button>

      {/* Resultados */}
      {results.length > 0 && (
        <div className="mt-4 space-y-2">
          <h3 className="font-medium">Resultados:</h3>
          <ul className="list-disc pl-6">
            {results.map((r, i) => (
              <li key={i}>
                Vecino: <strong>{r.neighbor}</strong> — Distancia:{" "}
                <span className="text-blue-600">{r.distance.toFixed(2)}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
