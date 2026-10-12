import { NavLink } from "react-router-dom";
import { LANGS } from "../content";
import { useProgress } from "../lib/progress";
import { levelFromXp, levelTitle, streak } from "../lib/game";
import { useToolchain } from "../lib/toolchain";

export function Logo({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 32 32" aria-hidden="true">
      <path d="M7 25 C 7 16, 25 19, 25 8" fill="none" stroke="#ffc24b" strokeWidth="2.4" strokeLinecap="round" strokeDasharray="0.1 4.4" />
      <circle cx="7" cy="25" r="3.6" fill="#34d399" />
      <circle cx="16" cy="17" r="2.8" fill="#c084fc" />
      <circle cx="25" cy="7.5" r="4" fill="#ffc24b" />
    </svg>
  );
}

export function Flame({ lit, size = 18 }: { lit: boolean; size?: number }) {
  return (
    <svg viewBox="0 0 24 24" width={size} height={size} aria-hidden="true">
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

const icons = {
  home: <path d="M4 11l8-7 8 7v9a1 1 0 0 1-1 1h-5v-6h-4v6H5a1 1 0 0 1-1-1z" />,
  camp: (
    <>
      <path d="M3 20L12 5l9 15z" />
      <path d="M12 5v15M9 20l3-5 3 5" />
    </>
  ),
  profile: (
    <>
      <circle cx="12" cy="8" r="4" />
      <path d="M4 21c1-4 4.5-6 8-6s7 2 8 6" />
    </>
  ),
  settings: (
    <>
      <circle cx="12" cy="12" r="3" />
      <path d="M12 2v3M12 19v3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M2 12h3M19 12h3M4.9 19.1L7 17M17 7l2.1-2.1" />
    </>
  ),
};

function Icon({ name }: { name: keyof typeof icons }) {
  return (
    <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      {icons[name]}
    </svg>
  );
}

function LevelRing({ value, level }: { value: number; level: number }) {
  const r = 21;
  const c = 2 * Math.PI * r;
  return (
    <svg viewBox="0 0 50 50" width="50" height="50" className="level-ring" aria-hidden="true">
      <circle cx="25" cy="25" r={r} fill="none" stroke="var(--surface-2)" strokeWidth="4" />
      <circle cx="25" cy="25" r={r} fill="none" stroke="var(--gold)" strokeWidth="4" strokeLinecap="round"
        strokeDasharray={`${c * value} ${c}`} transform="rotate(-90 25 25)" />
      <text x="25" y="30" textAnchor="middle">{level}</text>
    </svg>
  );
}

export function Sidebar() {
  const xp = useProgress((s) => s.xp);
  const activity = useProgress((s) => s.activity);
  const lang = useProgress((s) => s.settings.lang);
  const setSettings = useProgress((s) => s.setSettings);
  const { missing } = useToolchain();
  const lv = levelFromXp(xp);
  const st = streak(activity);

  return (
    <aside className="sidebar">
      <NavLink to="/" className="brand">
        <Logo className="brand-mark" />
        <span>LogIQ</span>
      </NavLink>

      <nav className="side-nav">
        <NavLink to="/" end>
          <Icon name="home" /> <span>Trail</span>
        </NavLink>
        <NavLink to="/basecamp">
          <Icon name="camp" /> <span>Basecamp</span>
        </NavLink>
        <NavLink to="/profile">
          <Icon name="profile" /> <span>Profile</span>
        </NavLink>
        <NavLink to="/settings">
          <Icon name="settings" /> <span>Settings</span>
        </NavLink>
      </nav>

      <div className="side-section">
        <div className="side-label">Solving in</div>
        <div className="lang-pick" role="radiogroup" aria-label="Language">
          {LANGS.map((l) => {
            const gone = missing(l.id);
            return (
              <button
                key={l.id}
                title={gone ? `${l.label} — not installed` : l.label}
                role="radio"
                aria-checked={lang === l.id}
                className={lang === l.id ? "on" : ""}
                onClick={() => setSettings({ lang: l.id })}
              >
                <span className={`lang-dot ${l.id}`} />
                <span className="txt">{l.label}</span>
                {gone && <span className="runtime-miss" aria-label="not installed" />}
              </button>
            );
          })}
        </div>
      </div>

      <div className="side-foot">
        <div className="side-level" title={`${xp} XP total`}>
          <LevelRing value={lv.into / lv.span} level={lv.level} />
          <div>
            <div className="side-level-title">{levelTitle(lv.level)}</div>
            <div className="side-level-xp">
              {lv.into} / {lv.span} XP
            </div>
          </div>
        </div>
        <div className={`side-streak ${st ? "" : "cold"}`}>
          <Flame lit={st > 0} />
          <span className="txt">{st ? `${st}-day streak` : "No streak yet"}</span>
          <span className="num">{st || ""}</span>
        </div>
      </div>
    </aside>
  );
}
