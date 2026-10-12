import { Link, useNavigate } from "react-router-dom";
import { phases, phaseById, problemById, problemsInPhase, type Problem } from "../content";
import { useProgress, type ProgressState } from "../lib/progress";
import { areProblemsOpen, dailyQuest, dayKey, isPhaseOpen, needToOpen, solvedCount, streak } from "../lib/game";
import { WorldGlyph } from "../components/WorldGlyph";
import { Topo } from "../components/Topo";
import { Flame } from "../components/Sidebar";

// Pin positions on the map: x in % of width, y in px.
const PINS = [
  { x: 14, y: 72 },
  { x: 50, y: 196 },
  { x: 22, y: 320 },
  { x: 56, y: 444 },
  { x: 16, y: 568 },
  { x: 50, y: 692 },
];

/** The furthest world the learner has opened. */
function currentPhase(state: ProgressState) {
  let cur = 1;
  for (const ph of phases) if (isPhaseOpen(state, ph.id)) cur = ph.id;
  return cur;
}

type Next =
  | { kind: "problem"; problem: Problem; resume: boolean }
  | { kind: "guide"; phase: number }
  | { kind: "done" };

function nextStep(state: ProgressState): Next {
  const last = state.lastOpened ? problemById.get(state.lastOpened) : undefined;
  if (last && !state.problems[last.id]?.solvedAt && areProblemsOpen(state, last.phase)) return { kind: "problem", problem: last, resume: true };
  for (const ph of phases) {
    if (!isPhaseOpen(state, ph.id)) break;
    if (!state.docs[ph.id]?.quizPassed) return { kind: "guide", phase: ph.id };
    const p = problemsInPhase(ph.id).find((x) => !state.problems[x.id]?.solvedAt);
    if (p) return { kind: "problem", problem: p, resume: false };
  }
  return { kind: "done" };
}

function Ring({ value }: { value: number }) {
  const r = 55;
  const c = 2 * Math.PI * r;
  return (
    <svg className="ring" viewBox="0 0 118 118" aria-hidden="true">
      <circle cx="59" cy="59" r={r} fill="none" stroke="var(--c)" strokeOpacity="0.15" strokeWidth="3" />
      {value > 0 && (
        <circle cx="59" cy="59" r={r} fill="none" stroke="var(--c)" strokeWidth="3.5" strokeLinecap="round" strokeDasharray={`${c * value} ${c}`} />
      )}
    </svg>
  );
}

export function MapPage() {
  const state = useProgress();
  const nav = useNavigate();
  const quest = dailyQuest(state);
  const st = streak(state.activity);
  const solvedTotal = Object.values(state.problems).filter((p) => p.solvedAt).length;
  const cur = currentPhase(state);
  const next = nextStep(state);

  const week = Array.from({ length: 7 }, (_, i) => {
    const d = new Date();
    d.setDate(d.getDate() - (6 - i));
    return { k: dayKey(d), label: "SMTWTFS"[d.getDay()], on: !!state.activity[dayKey(d)], today: i === 6 };
  });

  const nextPhase = next.kind === "problem" ? next.problem.phase : next.kind === "guide" ? next.phase : cur;
  const np = phaseById(nextPhase)!;

  return (
    <div className="page">
      <div className="home-head">
        <div>
          <h1 className="display">Your trail</h1>
          <p>
            {solvedTotal === 0
              ? "Six worlds stand between you and DSA. Each one starts with a short guide, then a trail of problems."
              : `${solvedTotal} of 145 problems solved. ${st ? "Keep the streak alive with one more today." : "One problem today starts a new streak."}`}
          </p>
        </div>
      </div>

      <div className="home-cards">
        {next.kind === "done" ? (
          <div className="continue" style={{ ["--c" as string]: "var(--gold)" }}>
            <span className="eyebrow">All worlds complete</span>
            <h2>You finished LogicQuest. Time for DSA.</h2>
            <span className="meta">Try the Pure challenges you skipped, or solve problems again in another language.</span>
          </div>
        ) : (
          <Link
            className="continue"
            style={{ ["--c" as string]: np.color }}
            to={next.kind === "problem" ? `/problem/${next.problem.id}` : `/phase/${next.phase}/guide`}
          >
            <WorldGlyph id={np.id} size={150} className="glyph" />
            <span className="eyebrow">
              {next.kind === "guide" ? `Phase ${np.id} · ${np.world}` : next.resume ? "Pick up where you left off" : `Next on the trail · ${np.world}`}
            </span>
            <h2>{next.kind === "guide" ? `Read the ${np.title} guide` : next.problem.title}</h2>
            <span className="meta">
              {next.kind === "guide"
                ? "Pass the 5-question check to open this world's problems."
                : `${next.problem.difficulty} · ${next.problem.xp} XP · ${solvedCount(state, np.id)}/${problemsInPhase(np.id).length} solved in ${np.world}`}
            </span>
            <span className="go">
              <span className="btn btn-primary">{next.kind === "guide" ? "Open the guide" : next.resume ? "Continue" : "Start"}</span>
            </span>
          </Link>
        )}

        {quest ? (
          <button className="card mini quest-card" onClick={() => nav(`/problem/${quest.id}`)}>
            <span className="label">
              <svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M12 2l3 7 7 .6-5.3 4.7 1.6 7.2L12 17.8 5.7 21.5l1.6-7.2L2 9.6 9 9z" fill="currentColor" />
              </svg>
              Today's quest · double XP
            </span>
            <h3>{quest.title}</h3>
            <span className="sub">
              {phaseById(quest.phase)?.world} · {quest.difficulty} · {quest.xp * 2} XP
            </span>
            <span style={{ marginTop: "auto" }}>
              <span className="btn btn-sm btn-gold">Start quest</span>
            </span>
          </button>
        ) : (
          <div className="card mini">
            <span className="label">Today's quest</span>
            <span className="sub">Pass a world's check to get a daily quest worth double XP.</span>
          </div>
        )}

        <div className="card mini">
          <span className="label">
            <Flame lit={st > 0} size={16} /> Streak
          </span>
          <span className="value">
            {st} <span className="small muted">day{st === 1 ? "" : "s"}</span>
          </span>
          <div className="week" aria-label="Last 7 days">
            {week.map((d) => (
              <i key={d.k} className={`${d.on ? "on" : ""} ${d.today ? "today" : ""}`} title={d.k}>
                {d.label}
              </i>
            ))}
          </div>
        </div>
      </div>

      <section className="map" aria-label="World map">
        <Topo className="topo" seed={11} peaks={6} />
        <div className="map-title">
          <h2>The six worlds</h2>
          <span className="small muted">A world opens after you solve 60% of the one before it</span>
        </div>
        <div className="map-trail">
          <svg className="path" viewBox="0 0 100 760" preserveAspectRatio="none" aria-hidden="true">
            <path
              d={PINS.map((p, i) => {
                const x = p.x;
                if (i === 0) return `M ${x} ${p.y}`;
                const prev = PINS[i - 1];
                const px = prev.x;
                return `C ${px} ${p.y - 40}, ${x} ${prev.y + 40}, ${x} ${p.y}`;
              }).join(" ")}
              fill="none"
              stroke="#ffc24b"
              strokeOpacity="0.55"
              strokeWidth="2.5"
              strokeDasharray="2 9"
              strokeLinecap="round"
              vectorEffect="non-scaling-stroke"
            />
          </svg>
          {phases.map((ph, i) => {
            const open = isPhaseOpen(state, ph.id);
            const total = problemsInPhase(ph.id).length;
            const solved = solvedCount(state, ph.id);
            const here = ph.id === cur && open;
            const pos = PINS[i];
            const cls = `pin ${open ? "" : "locked"} ${here ? "current" : ""}`;
            const style = { left: `${pos.x}%`, top: pos.y, ["--c" as string]: ph.color, transform: "translate(-52px, -50%)" };
            const inner = (
              <>
                <div className="pin-medal">
                  <Ring value={solved / total} />
                  <WorldGlyph id={ph.id} size={50} />
                  <span className="pin-num">{ph.id}</span>
                  {!open && (
                    <span className="lock">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" aria-hidden="true">
                        <rect x="5" y="11" width="14" height="10" rx="2" />
                        <path d="M8 11V8a4 4 0 0 1 8 0v3" />
                      </svg>
                    </span>
                  )}
                  {here && <span className="you-are-here">You are here</span>}
                </div>
                <div className="pin-text">
                  <span className="pin-world">{ph.world}</span>
                  <span className="pin-topic">{ph.title}</span>
                  <span className="pin-meta">
                    {!open
                      ? `Solve ${needToOpen(state, ph.id)} more in ${phases[i - 1].world} to open`
                      : !state.docs[ph.id]?.quizPassed
                        ? "Start with the guide"
                        : `${solved} of ${total} solved`}
                  </span>
                </div>
              </>
            );
            return open ? (
              <Link key={ph.id} to={`/phase/${ph.id}`} className={cls} style={style}>
                {inner}
              </Link>
            ) : (
              <div key={ph.id} className={cls} style={style} aria-disabled="true">
                {inner}
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
}
