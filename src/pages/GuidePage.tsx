import { useEffect, useRef, useState } from "react";
import { Link, Navigate, useParams } from "react-router-dom";
import { docFor, phaseById } from "../content";
import { Markdown } from "../components/Markdown";
import { useProgress } from "../lib/progress";
import { isPhaseOpen } from "../lib/game";

const PASS = 4;

export function GuidePage() {
  const id = Number(useParams().id);
  const phase = phaseById(id);
  const state = useProgress();
  const { markDocRead, recordQuiz } = state;
  const lang = state.settings.lang;
  const endRef = useRef<HTMLDivElement>(null);
  const [picks, setPicks] = useState<(number | null)[]>(() => phase?.quiz.map(() => null) ?? []);
  const [checked, setChecked] = useState(false);

  // The guide counts as read once the quiz section scrolls into view.
  useEffect(() => {
    const el = endRef.current;
    if (!el) return;
    const io = new IntersectionObserver((e) => e[0].isIntersecting && markDocRead(id));
    io.observe(el);
    return () => io.disconnect();
  }, [id, markDocRead]);

  if (!phase || !isPhaseOpen(state, id)) return <Navigate to="/" replace />;

  const score = phase.quiz.reduce((s, q, i) => s + (picks[i] === q.answer ? 1 : 0), 0);
  const passed = score >= PASS;
  const allPicked = picks.every((p) => p !== null);

  function check() {
    setChecked(true);
    recordQuiz(id, score, score >= PASS);
  }

  function retry() {
    setChecked(false);
    setPicks(phase!.quiz.map(() => null));
  }

  return (
    <div className="page page-narrow" style={{ ["--c" as string]: phase.color }}>
      <p className="small">
        <Link to={`/phase/${id}`} className="muted">
          ← {phase.world}
        </Link>
      </p>
      <Markdown text={docFor(id)} lang={lang} />

      <section className="quiz" ref={endRef}>
        <h2>Check your understanding</h2>
        <p className="muted">Get {PASS} of {phase.quiz.length} right to open the problems. You can retry as often as you like.</p>
        {phase.quiz.map((q, qi) => (
          <div className="quiz-q" key={qi}>
            <p>
              {qi + 1}. {q.q}
            </p>
            <div className="quiz-opts">
              {q.options.map((o, oi) => {
                let cls = "quiz-opt";
                if (checked) {
                  if (oi === q.answer) cls += " right";
                  else if (picks[qi] === oi) cls += " wrong";
                } else if (picks[qi] === oi) cls += " picked";
                return (
                  <button
                    key={oi}
                    className={cls}
                    disabled={checked}
                    onClick={() => setPicks((p) => p.map((v, k) => (k === qi ? oi : v)))}
                  >
                    {o}
                  </button>
                );
              })}
            </div>
            {checked && <div className="quiz-why">{q.why}</div>}
          </div>
        ))}
        {!checked ? (
          <button className="btn btn-primary" disabled={!allPicked} onClick={check}>
            Check answers
          </button>
        ) : passed ? (
          <div className="notice good">
            <strong>
              {score}/{phase.quiz.length}. The trail is open.
            </strong>{" "}
            <Link to={`/phase/${id}`} className="btn btn-gold" style={{ marginLeft: 12 }}>
              Start solving
            </Link>
          </div>
        ) : (
          <div className="notice bad">
            <strong>
              {score}/{phase.quiz.length}.
            </strong>{" "}
            Read the explanations above, then try again.{" "}
            <button className="btn" style={{ marginLeft: 12 }} onClick={retry}>
              Try again
            </button>
          </div>
        )}
      </section>
    </div>
  );
}
