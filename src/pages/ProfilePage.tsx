import { phases, problems, problemsInPhase } from "../content";
import { useProgress } from "../lib/progress";
import { badges, dayKey, levelFromXp, levelTitle, solvedCount, streak } from "../lib/game";

const WEEKS = 20;

export function ProfilePage() {
  const state = useProgress();
  const lv = levelFromXp(state.xp);
  const solved = Object.values(state.problems).filter((p) => p.solvedAt);
  const noHints = solved.filter((p) => p.hintsUsed === 0).length;

  const start = new Date();
  start.setDate(start.getDate() - (WEEKS * 7 - 1) - start.getDay());
  const cells = Array.from({ length: WEEKS * 7 }, (_, i) => {
    const d = new Date(start);
    d.setDate(start.getDate() + i);
    const n = state.activity[dayKey(d)] ?? 0;
    return { key: dayKey(d), n, future: d > new Date() };
  });

  return (
    <div className="page">
      <h1>
        Level {lv.level}: {levelTitle(lv.level)}
      </h1>
      <p className="muted">
        {lv.span - lv.into} XP to level {lv.level + 1}.
      </p>
      <div className="stats">
        <div className="stat">
          <b>{state.xp}</b>
          <span>total XP</span>
        </div>
        <div className="stat">
          <b>
            {solved.length}/{problems.length}
          </b>
          <span>problems solved</span>
        </div>
        <div className="stat">
          <b>{streak(state.activity)}</b>
          <span>day streak (best {state.bestStreak})</span>
        </div>
        <div className="stat">
          <b>{noHints}</b>
          <span>solved without hints</span>
        </div>
      </div>

      <h2>Last {WEEKS} weeks</h2>
      <div className="heat" aria-label="Problems solved per day">
        {cells.map((c) => (
          <i
            key={c.key}
            title={`${c.key}: ${c.n} solved`}
            className={c.future ? "" : c.n >= 5 ? "l3" : c.n >= 2 ? "l2" : c.n >= 1 ? "l1" : ""}
            style={c.future ? { opacity: 0 } : undefined}
          />
        ))}
      </div>

      <h2>Worlds</h2>
      <div className="phasebars">
        {phases.map((ph) => {
          const total = problemsInPhase(ph.id).length;
          const n = solvedCount(state, ph.id);
          return (
            <div className="phasebar" key={ph.id} style={{ ["--c" as string]: ph.color }}>
              <span>
                {ph.id}. {ph.world}
              </span>
              <div className="bar">
                <span style={{ width: `${(n / total) * 100}%` }} />
              </div>
              <span className="muted">
                {n}/{total}
              </span>
            </div>
          );
        })}
      </div>

      <h2 style={{ marginTop: 32 }}>Badges</h2>
      <div className="badges">
        {badges(state).map((b) => (
          <div key={b.id} className={`badge ${b.earned ? "" : "off"}`}>
            <b>{b.name}</b>
            <span>{b.detail}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
