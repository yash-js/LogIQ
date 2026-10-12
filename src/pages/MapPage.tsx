import { Link, useNavigate } from "react-router-dom";
import { phases, problemsInPhase, phaseById } from "../content";
import { useProgress } from "../lib/progress";
import { dailyQuest, isPhaseOpen, needToOpen, solvedCount, streak } from "../lib/game";

function Ring({ value, color }: { value: number; color: string }) {
  const r = 46.5;
  const c = 2 * Math.PI * r;
  return (
    <svg viewBox="0 0 96 96" aria-hidden="true">
      <circle cx="48" cy="48" r={r} fill="none" stroke={color} strokeWidth="3" strokeDasharray={`${c * value} ${c}`} strokeLinecap="round" opacity={value ? 1 : 0} />
    </svg>
  );
}

export function MapPage() {
  const state = useProgress();
  const nav = useNavigate();
  const quest = dailyQuest(state);
  const st = streak(state.activity);
  const totalSolved = Object.values(state.problems).filter((p) => p.solvedAt).length;

  const greeting =
    totalSolved === 0
      ? "Six worlds stand between you and DSA. Start with the guide for The Crossroads."
      : st > 0
        ? `${st}-day streak. Keep it going with one problem today.`
        : "Welcome back. One problem today restarts your streak.";

  return (
    <div className="page">
      <div className="map-head">
        <div>
          <h1>Your trail</h1>
          <p>{greeting}</p>
        </div>
        {quest && (
          <button className="quest btn-ghost" style={{ cursor: "pointer", textAlign: "left" }} onClick={() => nav(`/problem/${quest.id}`)}>
            <svg className="quest-icon" viewBox="0 0 40 40" aria-hidden="true">
              <circle cx="20" cy="20" r="18" fill="none" stroke="#f2b544" strokeWidth="2" />
              <path d="M20 9 L23 17 L31 17 L24.5 22 L27 30 L20 25 L13 30 L15.5 22 L9 17 L17 17 Z" fill="#f2b544" />
            </svg>
            <div>
              <div className="small">Today's quest · double XP</div>
              <h3>{quest.title}</h3>
              <div className="muted small">{phaseById(quest.phase)?.world}</div>
            </div>
          </button>
        )}
      </div>

      <div className="trail">
        <svg className="trail-path" viewBox="0 0 100 600" preserveAspectRatio="none" aria-hidden="true">
          <path
            d={phases
              .map((_, i) => {
                const y = 50 + i * 100;
                const x = i % 2 === 0 ? 4.5 : 50.5;
                if (i === 0) return `M ${x} ${y}`;
                const px = (i - 1) % 2 === 0 ? 4.5 : 50.5;
                return `C ${px} ${y - 50}, ${x} ${y - 50}, ${x} ${y}`;
              })
              .join(" ")}
            fill="none"
            stroke="#343b58"
            strokeWidth="2"
            strokeDasharray="1 3"
            vectorEffect="non-scaling-stroke"
          />
        </svg>
        {phases.map((ph, i) => {
          const open = isPhaseOpen(state, ph.id);
          const total = problemsInPhase(ph.id).length;
          const solved = solvedCount(state, ph.id);
          const need = needToOpen(state, ph.id);
          const cls = `station ${i % 2 ? "right" : ""} ${open ? "" : "locked"}`;
          const inner = (
            <>
              <div className="station-node">
                <Ring value={solved / total} color={ph.color} />
                <b>{ph.id}</b>
              </div>
              <div>
                <div className="station-world">{ph.world}</div>
                <div className="station-title">{ph.title}</div>
                <div className="station-meta">
                  {open
                    ? `${solved} of ${total} solved${state.docs[ph.id]?.quizPassed ? "" : " · guide not finished"}`
                    : `Solve ${need} more in Phase ${ph.id - 1} to open`}
                </div>
              </div>
            </>
          );
          return open ? (
            <Link key={ph.id} to={`/phase/${ph.id}`} className={cls} style={{ ["--c" as string]: ph.color }}>
              {inner}
            </Link>
          ) : (
            <div key={ph.id} className={cls} style={{ ["--c" as string]: ph.color }} aria-disabled="true">
              {inner}
            </div>
          );
        })}
      </div>
    </div>
  );
}
