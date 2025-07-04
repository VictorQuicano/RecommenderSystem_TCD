"use client";

import { useEffect, useState } from "react";
import { useGlobalStore } from "@/store/store";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { fetch_recommender, type Recommendation } from "@/services/fetch_recomender";
import { ScrollArea } from "@radix-ui/react-scroll-area";
import { UserCombobox } from "./UserComobox";

export function RecommenderPanel() {
  const { dataset, setDataset, distance, setDistance } = useGlobalStore();
  const users = useGlobalStore((state) => state.users);
  const [selectedUser, setSelectedUser] = useState("");
  const [k, setK] = useState(3);
  const [umbral, setUmbral] = useState(0.5);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);

  useEffect(() => {
    if (selectedUser) handleRecommend();
  }, [dataset]);

  async function handleRecommend() {
    if (!selectedUser) return;
    const data = await fetch_recommender({ user: selectedUser, k, umbral });
    setRecommendations(data);
  }

  return (
    <Card className="w-full font-sans shadow-md rounded-2xl">
      <CardHeader>
        <CardTitle className="text-xl">🎬 Recomendador de Películas</CardTitle>
      </CardHeader>
      <CardContent className="flex w-full gap-6">
        {/* CONTROLES */}
        <div className="space-y-4 w-1/4 ">
          <UserCombobox
            users={users}
            selectedUser={selectedUser}
            onChange={setSelectedUser}
          />

          <div>
            <Label className="text-sm font-medium">k (vecinos)</Label>

            <Input
              type="number"
              value={k}
              min={1}
              onChange={(e) => setK(Number(e.target.value))}
            />
          </div>

          <div>
            <Label className="text-sm font-medium">Umbral</Label>
            <Input
              type="number"
              step="0.1"
              value={umbral}
              onChange={(e) => setUmbral(Number(e.target.value))}
            />
          </div>

          <Button onClick={handleRecommend} disabled={!selectedUser} className="w-full">
            Obtener recomendaciones
          </Button>
        </div>

        {/* RESULTADOS */}
        <div className="w-full">
          {recommendations.length > 0 && (
            <div>
              <Label className="text-lg font-medium">Películas recomendadas:</Label>
              <ScrollArea className="max-h-[35em] pr-2 overflow-auto">
                <div className="space-y-4">
                  {recommendations.map((rec, idx) => {
                    const headers = rec.neighbor.map((n) => n.name);
                    const values = rec.neighbor.map((n) => n.score.toFixed(2));

                    return (
                      <div
                        key={idx}
                        className="bg-white dark:bg-gray-950 border rounded-lg p-4 shadow-sm"
                      >
                        <div className="mb-2 text-base">
                          <span className="font-semibold text-lg">{rec.movie}</span>{" "}
                          <span className="text-muted-foreground text-sm">
                            (Score estimado: <strong>{rec.score.toFixed(2)}</strong>)
                          </span>
                        </div>
                        <div className="overflow-x-auto">
                          <table className="min-w-full text-sm text-left border-collapse table-auto">
                            <thead className="bg-muted text-muted-foreground">
                              <tr>
                                {headers.map((name, i) => (
                                  <th key={i} className="p-2 border bg-gray-100 capitalize">
                                    {name}
                                  </th>
                                ))}
                              </tr>
                            </thead>
                            <tbody>
                              <tr>
                                {values.map((val, i) => (
                                  <td key={i} className="p-2 border text-center">
                                    {val}
                                  </td>
                                ))}
                              </tr>
                            </tbody>
                          </table>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </ScrollArea>
            </div>
          )}
        </div>

      </CardContent>
    </Card >
  );
}
