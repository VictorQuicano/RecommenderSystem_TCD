import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import { useGlobalStore } from "@/store/store";
import { useEffect, useState } from "react";
import { fetchDistance } from "@/services/fetch_distance";

export function UserSelectorPair() {
  const users = useGlobalStore((state) => state.users);
  const distanceType = useGlobalStore((state) => state.distance);
  const datasetName = useGlobalStore((state) => state.dataset);

  const [user1, setUser1] = useState<string>("");
  const [user2, setUser2] = useState<string>("");
  const [result, setResult] = useState<number | null>(null);

  useEffect(() => {
    const runComparison = async () => {
      if (user1 && user2 && user1 !== user2) {
        console.log(`🔍 Comparando "${user1}" y "${user2}" usando "${distanceType}"`);
        const res = await fetchDistance(user1, user2, distanceType);
        setResult(res);
      }
    };

    runComparison();
  }, [user1, user2, distanceType]);

  return (
    <div className="space-y-4 mt-6">
      <h2 className="text-lg font-semibold">Calcular Distancia entre Usuarios</h2>

      <div className="flex gap-4 max-w-md">
        <Select value={user1} onValueChange={setUser1}>
          <SelectTrigger className="w-full">
            <SelectValue placeholder="Usuario 1" />
          </SelectTrigger>
          <SelectContent>
            {users.map((name, idx) => (
              <SelectItem key={idx} value={name}>
                {name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        <Select value={user2} onValueChange={setUser2}>
          <SelectTrigger className="w-full">
            <SelectValue placeholder="Usuario 2" />
          </SelectTrigger>
          <SelectContent>
            {users.map((name, idx) => (
              <SelectItem key={idx} value={name}>
                {name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {result !== null && (
        <div className="mt-4 text-green-600 font-medium">
          ✅ Distancia entre <strong>{user1}</strong> y <strong>{user2}</strong>: {result}
        </div>
      )}
    </div>
  );
}
