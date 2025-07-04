import { useEffect, useState } from "react";
import { fetch_matrix } from "@/services/fetch_matrix";
import { useGlobalStore } from "@/store/store";
import { Card, CardContent } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";

type MatrixResponse = {
  columns: string[];
  data: (number | null)[][];
  movies: string[]; // Agregado: nombres de películas
};

export function MatrixTable() {
  const [matrix, setMatrix] = useState<MatrixResponse>({
    columns: [],
    data: [],
    movies: [],
  });

  const dataset = useGlobalStore((state) => state.dataset);

  useEffect(() => {
    async function loadMatrix() {
      const res = await fetch_matrix();
      setMatrix(res);
    }

    loadMatrix();
  }, [dataset]);

  if (matrix.columns.length === 0 || matrix.data.length === 0) {
    return <p className="text-muted-foreground mt-4">Cargando matriz...</p>;
  }

  return (
    <Card className="mt-6">
      <CardContent>
        <h2 className="text-lg font-semibold mb-4">
          Matriz del dataset "{dataset.replace(".csv", "")}"
        </h2>

        <ScrollArea className="max-h-[400px] overflow-auto border rounded-lg">
          <table className="min-w-full text-sm text-left">
            <thead className="bg-gray-100 sticky top-0 z-10">
              <tr>
                <th className="border px-3 py-2">Película</th>
                {matrix.columns.map((col, idx) => (
                  <th key={idx} className="border px-3 py-2">
                    {col}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {matrix.data.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  <td className="border px-3 py-2 font-semibold whitespace-nowrap">
                    {matrix.movies[rowIndex] ?? `#${rowIndex + 1}`}
                  </td>
                  {row.map((val, colIdx) => (
                    <td key={colIdx} className="border px-3 py-2 text-center">
                      {val !== null ? val.toFixed(2) : "-"}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}
