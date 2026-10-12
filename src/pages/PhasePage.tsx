import { Link, Navigate, useParams } from "react-router-dom";
import { phaseById, problemsInPhase } from "../content";
import { useProgress } from "../lib/progress";
import { areProblemsOpen, dailyQuest, isPhaseOpen, solvedCount } from "../lib/game";

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

  return (
    <div style={{ ["--c" as string]: phase.color }}>
      <div className="phase-hero">
        <div className="phase-hero-inner">
          <div className="phase-kicker">Phase {phase.id} · {phase.title}</div>
          <h1>{phase.world}</h1>
          <p>
            {phase.tagline} {solved} of {list.length} solved.
          </p>
        </div>
      </div>
      <div className="page phase-grid">
        <aside className="panel study">
          <h3>Study first</h3>
          <div className={`study-step ${doc?.read ? "done" : ""}`}>
            <span className="tick">{doc?.read ? "✓" : "1"}</span>
            <div>
              <div>Read the guide</div>
              <div className="small muted">Examples are shown in your chosen language.</div>
            </div>
          </div>
          <div className={`study-step ${doc?.quizPassed ? "done" : ""}`}>
            <span className="tick">{doc?.quizPassed ? "✓" : "2"}</span>
            <div>
              <div>Pass the check (4 of 5)</div>
              <div className="small muted">
                {doc?.quizPassed ? `Best score ${doc.bestScore}/5` : "Opens the problems on this trail."}
              </div>
            </div>
          </div>
          <Link className={open ? "btn" : "btn btn-primary"} to={`/phase/${id}/guide`}>
            {open ? "Review the guide" : doc?.read ? "Continue to the check" : "Open the guide"}
          </Link>
        </aside>

        <section>
          {!open && <p className="notice" style={{ marginTop: 0 }}>Pass the check in the guide to start solving.</p>}
          <div className={`stones ${open ? "" : "locked"}`}>
            {list.map((p, i) => {
              const pr = state.problems[p.id];
              const cls = pr?.solvedAt ? "solved" : pr?.attempts ? "tried" : "";
              const isQuest = quest?.id === p.id;
              const body = (
                <>
                  <span className={`stone-dot ${p.difficulty === "stretch" ? "boss" : ""}`}>
                    <span>{pr?.solvedAt ? "✓" : i + 1}</span>
                  </span>
                  <div className="stone-body">
                    <div className="stone-title">{p.title}</div>
                    <div className="stone-meta">
                      <span className={`diff-${p.difficulty}`}>{p.difficulty}</span>
                      <span>{p.xp} XP</span>
                      {pr?.solvedAt && pr.hintsUsed > 0 && <span>{pr.hintsUsed} hint{pr.hintsUsed > 1 ? "s" : ""}</span>}
                      {isQuest && <span style={{ color: "var(--gold)" }}>today's quest</span>}
                    </div>
                  </div>
                </>
              );
              return open ? (
                <Link key={p.id} to={`/problem/${p.id}`} className={`stone ${cls} ${isQuest ? "quest" : ""}`}>
                  {body}
                </Link>
              ) : (
                <div key={p.id} className="stone">
                  {body}
                </div>
              );
            })}
          </div>
        </section>
      </div>
    </div>
  );
}
