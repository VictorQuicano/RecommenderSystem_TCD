"use client";

import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useGlobalStore } from "@/store/store";
import { useState } from "react";
import { fetchDistance } from "@/services/fetch_distance";
import { UserCombobox } from "./UserComobox";

export function UserSelectorPair() {
  const users = useGlobalStore((state) => state.users);
  const distanceType = useGlobalStore((state) => state.distance);

  const [user1, setUser1] = useState<string>("");
  const [user2, setUser2] = useState<string>("");
  const [result, setResult] = useState<number | null>(null);

  const handleCalculate = async () => {
    if (user1 && user2 && user1 !== user2) {
      const res = await fetchDistance(user1, user2, distanceType);
      setResult(res);
    }
  };

  return (
    <Card className="w-1/4 mx-auto font-sans shadow-md rounded-2xl">
      <CardHeader>
        <CardTitle className="text-xl">📏 Distancia entre Usuarios</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-3">
          <UserCombobox
            users={users}
            selectedUser={user1}
            onChange={setUser1}
            label="Usuario 1"
          />

          <UserCombobox
            users={users}
            selectedUser={user2}
            onChange={setUser2}
            label="Usuario 2"
          />

          <Button
            onClick={handleCalculate}
            disabled={!user1 || !user2 || user1 === user2}
            className="w-full"
          >
            Calcular distancia
          </Button>
        </div>

        {result !== null && (
          <div className="mt-2 text-base">
            ✅ Distancia entre <strong>{user1}</strong> y <strong>{user2}</strong>:{" "}
            <span className="font-semibold text-blue-600">{result.toFixed(4)}</span>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
