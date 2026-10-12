import { HashRouter, Route, Routes } from "react-router-dom";
import { TopBar } from "./components/TopBar";
import { MapPage } from "./pages/MapPage";
import { PhasePage } from "./pages/PhasePage";
import { GuidePage } from "./pages/GuidePage";
import { ProblemPage } from "./pages/ProblemPage";
import { ProfilePage } from "./pages/ProfilePage";
import { SettingsPage } from "./pages/SettingsPage";

export default function App() {
  return (
    <HashRouter>
      <div className="app">
        <TopBar />
        <main className="app-main">
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
    </HashRouter>
  );
}
