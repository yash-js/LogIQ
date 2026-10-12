import { Link } from "react-router-dom";
import { phases, problems, problemsInPhase } from "../content";
import { useProgress } from "../lib/progress";
import { badges, dayKey, levelFromXp, levelTitle, solvedCount, streak } from "../lib/game";
import { WorldGlyph } from "../components/WorldGlyph";

const WEEKS = 26;

function BigRing({ value, level }: { value: number; level: number }) {
  const r = 42;
  const c = 2 * Math.PI * r;
  return (
    <svg viewBox="0 0 100 100" className="level-ring" style={{ width: 104, height: 104 }} aria-hidden="true">
      <circle cx="50" cy="50" r={r} fill="none" stroke="var(--surface-2)" strokeWidth="8" />
      <circle cx="50" cy="50" r={r} fill="none" stroke="var(--gold)" strokeWidth="8" strokeLinecap="round" strokeDasharray={`${c * value} ${c}`} transform="rotate(-90 50 50)" />
      <text x="50" y="46" textAnchor="middle" style={{ font: "600 11px var(--font)", fill: "var(--muted)" }}>
        LEVEL
      </text>
      <text x="50" y="66" textAnchor="middle" style={{ font: "800 24px var(--font)", fill: "var(--ink)" }}>
        {level}
      </text>
    </svg>
  );
}

export function ProfilePage() {
  const state = useProgress();
  const lv = levelFromXp(state.xp);
  const solved = Object.values(state.problems).filter((p) => p.solvedAt);
  const pure = solved.filter((p) => p.pure).length;

  const start = new Date();
  start.setDate(start.getDate() - (WEEKS * 7 - 1) - start.getDay() + 6);
  const today = new Date();
  const cells = Array.from({ length: WEEKS * 7 }, (_, i) => {
    const d = new Date(start);
    d.setDate(start.getDate() + i - 6);
    const n = state.activity[dayKey(d)] ?? 0;
    return { key: dayKey(d), n, future: d > today };
  });
  const activeDays = Object.values(state.activity).filter(Boolean).length;

  return (
    <div className="page">
      <div className="profile-head">
        <BigRing value={lv.into / lv.span} level={lv.level} />
        <div>
          <h1 className="display">{levelTitle(lv.level)}</h1>
          <p className="muted" style={{ margin: "6px 0 0" }}>
            {state.xp} XP total · {lv.span - lv.into} XP to level {lv.level + 1}
          </p>
        </div>
      </div>

      <div className="stats">
        <div className="card stat">
          <b>
            {solved.length}
            <span className="muted" style={{ fontSize: 18 }}>
              /{problems.length}
            </span>
          </b>
          <span>problems solved</span>
        </div>
        <div className="card stat">
          <b>{pure}</b>
          <span>Pure solves, no shortcuts</span>
        </div>
        <div className="card stat">
          <b>{streak(state.activity)}</b>
          <span>day streak · best {state.bestStreak}</span>
        </div>
        <div className="card stat">
          <b>{solved.filter((p) => p.hintsUsed === 0).length}</b>
          <span>solved without hints</span>
        </div>
      </div>

      <div className="section-title">
        <h2>Activity</h2>
        <span className="small muted">{activeDays} active days</span>
      </div>
      <div className="card heat-wrap">
        <div className="heat" aria-label="Problems solved per day">
          {cells.map((c) => (
            <i
              key={c.key}
              title={`${c.key}: ${c.n} solved`}
              className={c.n >= 5 ? "l3" : c.n >= 2 ? "l2" : c.n >= 1 ? "l1" : ""}
              style={c.future ? { visibility: "hidden" } : undefined}
            />
          ))}
        </div>
        <div className="heat-legend">
          Less <i style={{ background: "var(--surface-2)" }} />
          <i style={{ background: "#7c4a1d" }} />
          <i style={{ background: "#c2410c" }} />
          <i style={{ background: "#fb923c" }} /> More
        </div>
      </div>

      <div className="section-title">
        <h2>Worlds</h2>
      </div>
      <div className="worlds-grid">
        {phases.map((ph) => {
          const total = problemsInPhase(ph.id).length;
          const n = solvedCount(state, ph.id);
          return (
            <Link to={`/phase/${ph.id}`} className="card world-card" key={ph.id} style={{ ["--c" as string]: ph.color, textDecoration: "none" }}>
              <div className="top">
                <WorldGlyph id={ph.id} size={30} />
                <b>{ph.world}</b>
              </div>
              <div className="bar">
                <span style={{ width: `${(n / total) * 100}%` }} />
              </div>
              <div className="nums">
                <span>{ph.title}</span>
                <span className="tnum">
                  {n}/{total}
                </span>
              </div>
            </Link>
          );
        })}
      </div>

      <div className="section-title">
        <h2>Badges</h2>
        <span className="small muted">
          {badges(state).filter((b) => b.earned).length} of {badges(state).length} earned
        </span>
      </div>
      <div className="badges">
        {badges(state).map((b) => (
          <div key={b.id} className={`card badge ${b.earned ? "" : "off"}`}>
            <span className="medal">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinejoin="round" aria-hidden="true">
                <circle cx="12" cy="9" r="6" />
                <path d="M8.5 14L7 22l5-3 5 3-1.5-8" />
              </svg>
            </span>
            <span>
              <b>{b.name}</b>
              <span>{b.detail}</span>
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
