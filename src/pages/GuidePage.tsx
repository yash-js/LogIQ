import { useEffect, useRef, useState } from "react";
import { Link, Navigate, useLocation, useParams } from "react-router-dom";
import { docFor, LANGS, phaseById } from "../content";
import { filterForLang, Markdown, slug } from "../components/Markdown";
import { useProgress } from "../lib/progress";
import { isPhaseOpen } from "../lib/game";

const PASS = 4;

export function GuidePage() {
  const id = Number(useParams().id);
  const loc = useLocation();
  const phase = phaseById(id);
  const state = useProgress();
  const { markDocRead, recordQuiz } = state;
  const lang = state.settings.lang;
  const endRef = useRef<HTMLDivElement>(null);
  const quiz = phase ? phase.quiz.filter((q) => !q.lang || q.lang === lang) : [];
  const [picks, setPicks] = useState<(number | null)[]>(() => quiz.map(() => null));
  const [checked, setChecked] = useState(false);
  const [quizKey, setQuizKey] = useState(`${id}:${lang}`);
  if (quizKey !== `${id}:${lang}`) {
    setQuizKey(`${id}:${lang}`);
    setPicks(quiz.map(() => null));
    setChecked(false);
  }

  useEffect(() => {
    const el = endRef.current;
    if (!el) return;
    const io = new IntersectionObserver((e) => e[0].isIntersecting && markDocRead(id));
    io.observe(el);
    return () => io.disconnect();
  }, [id, markDocRead]);

  useEffect(() => {
    if (loc.hash === "#check") endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [loc.hash]);

  if (!phase || !isPhaseOpen(state, id)) return <Navigate to="/" replace />;

  const md = filterForLang(docFor(id), lang);
  const sections = md.split("\n").filter((l) => l.startsWith("## ")).map((l) => l.slice(3));
  const score = quiz.reduce((s, q, i) => s + (picks[i] === q.answer ? 1 : 0), 0);
  const passed = score >= PASS;

  const scrollTo = (sid: string) => (e: React.MouseEvent) => {
    e.preventDefault();
    document.getElementById(sid)?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className="guide" style={{ ["--c" as string]: phase.color }}>
      <nav className="toc" aria-label="Sections">
        <Link to={`/phase/${id}`} className="back muted">
          ← {phase.world}
        </Link>
        {sections.map((s) => (
          <a key={s} href={`#${slug(s)}`} onClick={scrollTo(slug(s))}>
            {s.replace(/^\d+\.\s*/, "")}
          </a>
        ))}
        <a href="#check" onClick={scrollTo("check")} style={{ color: "var(--c)", fontWeight: 700 }}>
          The check
        </a>
      </nav>

      <article>
        <div className="lang-note">
          Written for {LANGS.find((l) => l.id === lang)?.label}. Switch the language in the sidebar.
        </div>
        <Markdown text={md} lang={lang} />

        <section className="card quiz" id="check" ref={endRef}>
          <div className="quiz-head">
            <h2>Check your understanding</h2>
            <span className="small muted">
              {PASS} of {quiz.length} to pass · {state.docs[id]?.quizPassed ? "already passed" : "unlimited tries"}
            </span>
          </div>
          {quiz.map((q, qi) => (
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
                    <button key={oi} className={cls} disabled={checked} onClick={() => setPicks((p) => p.map((v, k) => (k === qi ? oi : v)))}>
                      <span className="k">{"ABCD"[oi]}</span>
                      {o}
                    </button>
                  );
                })}
              </div>
              {checked && <div className="quiz-why">{q.why}</div>}
            </div>
          ))}
          {!checked ? (
            <button
              className="btn btn-primary btn-lg"
              disabled={picks.length !== quiz.length || picks.some((p) => p === null)}
              onClick={() => {
                setChecked(true);
                recordQuiz(id, score, score >= PASS);
              }}
            >
              Check answers
            </button>
          ) : passed ? (
            <div className="notice good">
              <strong>
                {score}/{quiz.length} correct. The trail is open.
              </strong>
              <Link to={`/phase/${id}`} className="btn btn-gold">
                Start solving
              </Link>
            </div>
          ) : (
            <div className="notice bad">
              <strong>
                {score}/{quiz.length} correct.
              </strong>
              <span>Read the explanations, then try again.</span>
              <button
                className="btn btn-sm"
                onClick={() => {
                  setChecked(false);
                  setPicks(quiz.map(() => null));
                }}
              >
                Try again
              </button>
            </div>
          )}
        </section>
      </article>
    </div>
  );
}
