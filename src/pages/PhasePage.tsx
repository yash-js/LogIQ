import { Link, Navigate, useParams } from "react-router-dom";
import { phaseById, problemsInPhase } from "../content";
import { useProgress } from "../lib/progress";
import { areProblemsOpen, dailyQuest, isPhaseOpen, solvedCount } from "../lib/game";
import { WorldGlyph } from "../components/WorldGlyph";
import { Topo } from "../components/Topo";

const ROW = 74;
const OFFSETS = [0, 90, 180, 90];

export function PhasePage() {
  const id = Number(useParams().id);
  const phase = phaseById(id);
  const state = useProgress();
  if (!phase || !isPhaseOpen(state, id)) return <Navigate to="/" replace />;

  const list = problemsInPhase(id);
  const doc = state.docs[id];
  const open = areProblemsOpen(state, id);
  const quest = dailyQuest(state);
  const solved = solvedCount(state, id);
  const pure = list.filter((p) => state.problems[p.id]?.pure).length;
  const nextIdx = list.findIndex((p) => !state.problems[p.id]?.solvedAt);

  const pts = list.map((_, i) => ({ x: OFFSETS[i % OFFSETS.length] + 25, y: i * ROW + 32 }));
  const d = pts
    .map((p, i) => {
      if (i === 0) return `M ${p.x} ${p.y}`;
      const q = pts[i - 1];
      return `C ${q.x} ${q.y + ROW / 2}, ${p.x} ${p.y - ROW / 2}, ${p.x} ${p.y}`;
    })
    .join(" ");
  const doneUpTo = nextIdx < 0 ? list.length : nextIdx;
  const dDone = pts
    .slice(0, Math.max(1, doneUpTo + (doneUpTo < list.length ? 1 : 0)))
    .map((p, i, arr) => {
      if (i === 0) return `M ${p.x} ${p.y}`;
      const q = arr[i - 1];
      return `C ${q.x} ${q.y + ROW / 2}, ${p.x} ${p.y - ROW / 2}, ${p.x} ${p.y}`;
    })
    .join(" ");

  return (
    <div style={{ ["--c" as string]: phase.color }}>
      <header className="world-hero">
        <Topo className="topo" seed={id * 31} peaks={3} width={1400} height={320} />
        <div className="world-hero-inner">
          <div className="world-emblem">
            <WorldGlyph id={id} size={70} />
          </div>
          <div>
            <div className="crumbs">
              <Link to="/">Trail</Link> / Phase {id}
            </div>
            <h1 className="display">{phase.world}</h1>
            <p>
              {phase.title}. {phase.tagline}
            </p>
          </div>
          <div className="world-progress">
            <div className="big">
              {solved}
              <small> / {list.length} solved</small>
            </div>
            <div className="bar" style={{ margin: "10px 0 8px" }}>
              <span style={{ width: `${(solved / list.length) * 100}%` }} />
            </div>
            <div className="small muted">{pure} Pure solves</div>
          </div>
        </div>
      </header>

      <div className="page" style={{ paddingTop: 0 }}>
        <div className="steps">
          <Link to={`/phase/${id}/guide`} className={`step ${doc?.read ? "done" : "active"}`}>
            <span className="n">{doc?.read ? "✓" : 1}</span>
            <span>
              <div className="t">Read the guide</div>
              <div className="d">Examples in your language</div>
            </span>
          </Link>
          <Link to={`/phase/${id}/guide#check`} className={`step ${doc?.quizPassed ? "done" : doc?.read ? "active" : ""}`}>
            <span className="n">{doc?.quizPassed ? "✓" : 2}</span>
            <span>
              <div className="t">Pass the check</div>
              <div className="d">{doc?.quizPassed ? `Best score ${doc.bestScore}/5` : "4 of 5 correct opens the trail"}</div>
            </span>
          </Link>
          <div className={`step ${solved === list.length ? "done" : open ? "active" : ""}`}>
            <span className="n">{solved === list.length ? "✓" : 3}</span>
            <span>
              <div className="t">Solve the trail</div>
              <div className="d">
                {list.length} problems · {list.reduce((s, p) => s + p.xp, 0)} XP
              </div>
            </span>
          </div>
        </div>

        {!open && (
          <div className="notice warn" style={{ marginBottom: 24 }}>
            <span>The trail opens after you pass the check at the end of the guide.</span>
            <Link to={`/phase/${id}/guide`} className="btn btn-sm btn-primary">
              Open the guide
            </Link>
          </div>
        )}

        <div className="trail-wrap">
          <div className={`ptrail ${open ? "" : "locked"}`} style={{ height: list.length * ROW }}>
            <svg width="300" height={list.length * ROW} aria-hidden="true">
              <path d={d} fill="none" stroke="var(--line)" strokeWidth="3" strokeDasharray="1 8" strokeLinecap="round" />
              {doneUpTo > 0 && <path d={dDone} fill="none" stroke="var(--c)" strokeOpacity="0.7" strokeWidth="3" strokeLinecap="round" />}
            </svg>
            {list.map((p, i) => {
              const pr = state.problems[p.id];
              const isQuest = quest?.id === p.id;
              const cls = [
                "pnode",
                pr?.solvedAt ? "solved" : pr?.attempts ? "tried" : "",
                pr?.pure ? "pure" : "",
                i === nextIdx && open ? "next" : "",
                p.difficulty === "stretch" ? "stretch" : "",
              ].join(" ");
              const style = { left: OFFSETS[i % OFFSETS.length], top: i * ROW };
              const body = (
                <>
                  <span className="pnode-dot">
                    <span>{pr?.solvedAt ? "✓" : i + 1}</span>
                  </span>
                  <span>
                    <div className="pnode-title">{p.title}</div>
                    <div className="pnode-meta">
                      <span>{p.difficulty}</span>
                      <span>{p.xp} XP</span>
                      {pr?.solvedAt && !pr.pure && <span>Pure challenge open</span>}
                      {isQuest && <span className="q">Today's quest ×2</span>}
                    </div>
                  </span>
                </>
              );
              return open ? (
                <Link key={p.id} to={`/problem/${p.id}`} className={cls} style={style}>
                  {body}
                </Link>
              ) : (
                <div key={p.id} className={cls} style={style}>
                  {body}
                </div>
              );
            })}
          </div>

          <aside className="card legend">
            <h3 style={{ marginBottom: 4 }}>Reading the trail</h3>
            <div className="legend-row">
              <i /> Not started
            </div>
            <div className="legend-row">
              <i className="t" /> Tried, not solved yet
            </div>
            <div className="legend-row">
              <i className="s" /> Solved
            </div>
            <div className="legend-row">
              <i className="p" /> Solved without library shortcuts
            </div>
            <div className="legend-row">
              <i className="b" /> Stretch problem
            </div>
            <p className="small muted" style={{ margin: "6px 0 0" }}>
              Solve in any order. Each hint you open before solving takes 25% off that problem's XP.
            </p>
          </aside>
        </div>
      </div>
    </div>
  );
}
