"use client";

import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useGlobalStore } from "@/store/store";
import { fetchKNN } from "@/services/fetch_knn";
import { useState } from "react";
import { UserCombobox } from "./UserComobox";

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
    <Card className="w-1/4 mx-auto font-sans shadow-md rounded-2xl">
      <CardHeader>
        <CardTitle className="text-xl">🔍 Ejecutar KNN</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Select de usuario */}
        <div className="space-y-1">
          <UserCombobox
            users={users}
            selectedUser={selectedUser}
            onChange={setSelectedUser}
          />
        </div>

        {/* Input numérico para k */}
        <div className="space-y-1">
          <label className="text-sm font-medium">Número de vecinos (k)</label>
          <Input
            type="number"
            min={1}
            max={users.length - 1}
            value={k}
            onChange={(e) => setK(Number(e.target.value))}
            placeholder="Número de vecinos"
          />
        </div>

        {/* Botón */}
        <Button onClick={handleRunKNN} disabled={!selectedUser} className="w-full">
          Ejecutar KNN
        </Button>

        {results.length > 0 && (
          <div className="space-y-2">
            <h3 className="text-lg font-medium">Resultados:</h3>
            <ScrollArea className="max-h-80 overflow-auto rounded-md border">
              <table className="w-full text-sm text-left table-auto">
                <thead className="bg-gray-100 dark:bg-gray-800">
                  <tr>
                    <th className="px-4 py-2 border-b font-semibold">Vecino</th>
                    <th className="px-4 py-2 border-b font-semibold">Distancia</th>
                  </tr>
                </thead>
                <tbody>
                  {results.map((r, i) => (
                    <tr
                      key={i}
                      className={i % 2 === 0 ? "bg-white dark:bg-gray-950" : "bg-gray-50 dark:bg-gray-900"}
                    >
                      <td className="px-4 py-2 border-b">{r.neighbor}</td>
                      <td className="px-4 py-2 border-b text-blue-600">{r.distance.toFixed(4)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </ScrollArea>
          </div>
        )}

      </CardContent>
    </Card>
  );
}
