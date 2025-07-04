import { useEffect } from "react";
import { DistanceSelector } from "./components/DistanceSelector";
import { DatasetSelector } from "./components/DatasetSelector";
import { fetchNames } from "./services/fetch_names";
import { UserSelectorPair } from "./components/UserSelector";
import { useGlobalStore } from "./store/store";
import { KNNRunner } from "./components/KnnRunner";
import { MatrixTable } from "./components/MatrixChart";
import { RecommenderPanel } from "./components/RecommenderPanel";

function App() {
  const datasetName = useGlobalStore((state) => state.dataset);

  useEffect(() => {
    fetchNames();
  }, [datasetName]);

  return (
    <div className="p-6 space-y-4 flex flex-col max-h-screen overflow-hidden">
      <div className="flex justify-center items-center gap-5">
        <DatasetSelector />
        <DistanceSelector />
      </div>
      <div className="flex w-full justify-between gap-5 min-h-full">
        <UserSelectorPair />
        <KNNRunner />
        <RecommenderPanel />
      </div>
      {/* <MatrixTable /> */}
    </div>
  );
}

export default App;
