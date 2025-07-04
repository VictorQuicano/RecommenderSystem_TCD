import { useEffect } from "react";
import { DistanceSelector } from "./components/DistanceSelector";
import { DatasetSelector } from "./components/DatasetSelector";
import { fetchNames } from "./services/fetch_names";
import { UserSelectorPair } from "./components/UserSelector";
import { useGlobalStore } from "./store/store";
import { KNNRunner } from "./components/KnnRunner";
import { MatrixTable } from "./components/MatrixChart";

function App() {
  const datasetName = useGlobalStore((state) => state.dataset);

  useEffect(() => {
    fetchNames();
  }, [datasetName]);

  return (
    <div className="p-6 space-y-4">
      <DatasetSelector />
      <DistanceSelector />
      <UserSelectorPair />
      <KNNRunner />
      <MatrixTable />
    </div>
  );
}

export default App;
