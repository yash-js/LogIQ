import { HashRouter, Route, Routes, useLocation } from "react-router-dom";
import { Sidebar } from "./components/Sidebar";
import { MapPage } from "./pages/MapPage";
import { PhasePage } from "./pages/PhasePage";
import { GuidePage } from "./pages/GuidePage";
import { ProblemPage } from "./pages/ProblemPage";
import { ProfilePage } from "./pages/ProfilePage";
import { SettingsPage } from "./pages/SettingsPage";

function Shell() {
  const loc = useLocation();
  const flush = loc.pathname.startsWith("/problem/");
  return (
      <div className={`app ${flush ? "compact" : ""}`}>
        <Sidebar />
        <main className={`app-main ${flush ? "flush" : ""}`} key={flush ? "ws" : loc.pathname}>
          <Routes>
            <Route path="/" element={<MapPage />} />
            <Route path="/phase/:id" element={<PhasePage />} />
            <Route path="/phase/:id/guide" element={<GuidePage />} />
            <Route path="/problem/:id" element={<ProblemPage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/settings" element={<SettingsPage />} />
            <Route path="*" element={<MapPage />} />
          </Routes>
        </main>
      </div>
  );
}

export default function App() {
  return (
    <HashRouter>
      <Shell />
    </HashRouter>
  );
}
