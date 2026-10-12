import { useNavigate } from "react-router-dom";
import { openUrl } from "@tauri-apps/plugin-opener";
import { LANGS } from "../content";
import { useProgress } from "../lib/progress";
import { inTauri } from "../lib/runner";
import { INSTALL_URL, useToolchain } from "../lib/toolchain";

/** Amber bar shown when the selected language cannot run code on this machine. */
export function RuntimeBanner() {
  const nav = useNavigate();
  const lang = useProgress((s) => s.settings.lang);
  const tool = useToolchain();
  if (!inTauri || tool.dismissed || !tool.missing(lang)) return null;
  const label = LANGS.find((l) => l.id === lang)!.label;
  return (
    <div className="notice warn runtime-banner" role="status">
      <span>{label} isn't installed, so Run and Submit won't work.</span>
      <button className="btn btn-sm" onClick={() => void openUrl(INSTALL_URL[lang])}>
        Install {label}
      </button>
      <button className="btn btn-sm" onClick={() => void tool.recheck()}>
        I installed it, check again
      </button>
      <button className="btn btn-sm" onClick={() => nav("/settings")}>
        Open Settings
      </button>
      <button className="btn btn-ghost btn-sm runtime-dismiss" onClick={tool.dismiss} aria-label="Dismiss">
        ✕
      </button>
    </div>
  );
}
