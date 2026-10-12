import { useEffect, useState } from "react";
import { HashRouter, Route, Routes, useLocation } from "react-router-dom";
import { useProgress } from "./lib/progress";
import { Sidebar } from "./components/Sidebar";
import { MapPage } from "./pages/MapPage";
import { PhasePage } from "./pages/PhasePage";
import { GuidePage } from "./pages/GuidePage";
import { ProblemPage } from "./pages/ProblemPage";
import { ProfilePage } from "./pages/ProfilePage";
import { SettingsPage } from "./pages/SettingsPage";
import { BasecampPage } from "./pages/BasecampPage";
import { LessonPage } from "./pages/LessonPage";
import { PlacementPage } from "./pages/PlacementPage";

function Shell() {
  const loc = useLocation();
  const flush = loc.pathname.startsWith("/problem/") || (/^\/basecamp\/[a-z]+-\d+$/.test(loc.pathname));
  return (
      <div className={`app ${flush ? "compact" : ""}`}>
        <Sidebar />
        <main className={`app-main ${flush ? "flush" : ""}`} key={flush ? "ws" : loc.pathname}>
          <Routes>
            <Route path="/" element={<MapPage />} />
            <Route path="/phase/:id" element={<PhasePage />} />
            <Route path="/phase/:id/guide" element={<GuidePage />} />
            <Route path="/problem/:id" element={<ProblemPage />} />
            <Route path="/basecamp" element={<BasecampPage />} />
            <Route path="/basecamp/placement" element={<PlacementPage />} />
            <Route path="/basecamp/:unitId" element={<LessonPage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/settings" element={<SettingsPage />} />
            <Route path="*" element={<MapPage />} />
          </Routes>
        </main>
      </div>
  );
}

function useHydrated() {
  const [ok, setOk] = useState(() => useProgress.persist.hasHydrated());
  useEffect(() => {
    if (ok) return;
    const off = useProgress.persist.onFinishHydration(() => setOk(true));
    if (useProgress.persist.hasHydrated()) setOk(true);
    return off;
  }, [ok]);
  return ok;
}

export default function App() {
  // Progress loads asynchronously from SQLite; wait so locked pages don't redirect early.
  if (!useHydrated()) return <div className="app-loading" />;
  return (
    <HashRouter>
      <Shell />
    </HashRouter>
  );
}
