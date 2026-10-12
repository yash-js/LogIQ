import { NavLink } from "react-router-dom";
import { useProgress } from "../lib/progress";
import { levelFromXp, levelTitle, streak } from "../lib/game";
import { useSync } from "../lib/sync";
import { supabaseConfigured } from "../lib/supabase";

export function Logo({ className }: { className?: string }) {
  // A trail with three stops: the path from logic to DSA.
  return (
    <svg className={className} viewBox="0 0 32 32" aria-hidden="true">
      <path d="M6 26 C 6 16, 26 20, 26 8" fill="none" stroke="#f2b544" strokeWidth="3" strokeLinecap="round" strokeDasharray="0.1 5.5" />
      <circle cx="6" cy="26" r="4" fill="#22c55e" />
      <circle cx="16" cy="17" r="3.2" fill="#a855f7" />
      <circle cx="26" cy="7" r="4.5" fill="#f2b544" />
    </svg>
  );
}

export function Flame({ lit }: { lit: boolean }) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path
        d="M12 2c1 4 5 6 5 11a5 5 0 0 1-10 0c0-2 1-3.5 2-4.5 0 2 1 3 2 3 0-3-1-6 1-9.5z"
        fill={lit ? "#fb923c" : "none"}
        stroke={lit ? "#fb923c" : "currentColor"}
        strokeWidth="1.6"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function TopBar() {
  const xp = useProgress((s) => s.xp);
  const activity = useProgress((s) => s.activity);
  const lang = useProgress((s) => s.settings.lang);
  const setSettings = useProgress((s) => s.setSettings);
  const sync = useSync();
  const lv = levelFromXp(xp);
  const st = streak(activity);

  return (
    <header className="topbar">
      <NavLink to="/" className="brand">
        <Logo className="brand-mark" />
        LogicQuest
      </NavLink>
      <nav className="nav">
        <NavLink to="/" end>
          Map
        </NavLink>
        <NavLink to="/profile">Profile</NavLink>
        <NavLink to="/settings">Settings</NavLink>
      </nav>
      <div className="topbar-right">
        <div className="seg" role="group" aria-label="Language">
          <button className={lang === "java" ? "on" : ""} onClick={() => setSettings({ lang: "java" })}>
            Java
          </button>
          <button className={lang === "python" ? "on" : ""} onClick={() => setSettings({ lang: "python" })}>
            Python
          </button>
        </div>
        <div className={`streak ${st ? "" : "cold"}`} title={st ? `${st}-day streak` : "Solve a problem today to start a streak"}>
          <Flame lit={st > 0} />
          {st}
        </div>
        <div className="levelchip" title={`${xp} XP total`}>
          <div className="levelchip-level">{lv.level}</div>
          <div className="levelchip-title">{levelTitle(lv.level)}</div>
          <div className="xpbar">
            <span style={{ width: `${(lv.into / lv.span) * 100}%` }} />
          </div>
        </div>
        {supabaseConfigured && (
          <span
            className={`syncdot ${sync.status}`}
            title={sync.session ? `Sync: ${sync.status}${sync.error ? ` (${sync.error})` : ""}` : "Not signed in: progress is saved on this computer only"}
          />
        )}
      </div>
    </header>
  );
}
