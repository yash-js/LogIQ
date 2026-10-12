import { useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { LANGS } from "../content";
import { useProgress } from "../lib/progress";
import { PLACEMENT_PASS, PLACEMENT_XP, placementQuestions, predictCorrect } from "../lib/basecamp";
import { CodeBlock } from "../components/ExerciseView";
import { Markdown } from "../components/Markdown";

export function PlacementPage() {
  const lang = useProgress((s) => s.settings.lang);
  const recordPlacement = useProgress((s) => s.recordPlacement);
  const nav = useNavigate();
  const label = LANGS.find((l) => l.id === lang)!.label;
  const qs = useMemo(() => placementQuestions(lang), [lang]);
  const [answers, setAnswers] = useState<(string | number | null)[]>(() => qs.map(() => null));
  const [result, setResult] = useState<{ score: number; gain: number } | null>(null);

  const correct = (i: number) => {
    const { ex } = qs[i];
    const a = answers[i];
    if (ex.kind === "choice") return a === ex.answer;
    if (ex.kind === "predict") return typeof a === "string" && predictCorrect(ex.expected, a);
    return false;
  };

  function submit() {
    const score = qs.reduce((s, _, i) => s + (correct(i) ? 1 : 0), 0);
    const gain = score >= PLACEMENT_PASS ? recordPlacement(lang, PLACEMENT_XP) : 0;
    setResult({ score, gain });
    document.querySelector(".app-main")?.scrollTo({ top: 0, behavior: "smooth" });
  }

  return (
    <div className="page page-narrow">
      <p className="small">
        <Link to="/basecamp" className="muted">
          ← Basecamp
        </Link>
      </p>
      <h1 className="display" style={{ fontSize: 40 }}>
        {label} placement test
      </h1>
      <p className="muted">
        One question from each Basecamp unit. {PLACEMENT_PASS} of {qs.length} correct marks Basecamp complete for {label} and gives {PLACEMENT_XP} XP.
      </p>

      {result && (
        <div className={`notice ${result.score >= PLACEMENT_PASS ? "good" : "bad"}`} style={{ margin: "18px 0" }}>
          <strong>
            {result.score}/{qs.length} correct.
          </strong>
          {result.score >= PLACEMENT_PASS ? (
            <>
              <span>Basecamp is done. {result.gain ? `+${result.gain} XP.` : ""}</span>
              <button className="btn btn-gold btn-sm" onClick={() => nav("/")}>
                Go to the trail
              </button>
            </>
          ) : (
            <>
              <span>The units you missed are marked below. Work through Basecamp; it goes quickly when you know most of it.</span>
              <Link to="/basecamp" className="btn btn-sm">
                Back to Basecamp
              </Link>
            </>
          )}
        </div>
      )}

      {qs.map(({ unit, ex }, i) => (
        <section key={i} className="card pad placement-q">
          <div className="ex-kind">
            {i + 1}. {unit} {result && (correct(i) ? <span className="ok">· correct</span> : <span className="no">· missed</span>)}
          </div>
          <div className="ex-prompt-sm">
            <Markdown text={ex.prompt} />
          </div>
          {ex.kind === "choice" && (
            <>
              {ex.code && <CodeBlock code={ex.code} lang={lang} />}
              <div className="quiz-opts">
                {ex.options.map((o, oi) => {
                  let cls = "quiz-opt";
                  if (result) {
                    if (oi === ex.answer) cls += " right";
                    else if (answers[i] === oi) cls += " wrong";
                  } else if (answers[i] === oi) cls += " picked";
                  return (
                    <button key={oi} className={cls} disabled={!!result} onClick={() => setAnswers((a) => a.map((v, k) => (k === i ? oi : v)))}>
                      <span className="k">{"ABCD"[oi]}</span>
                      <span className="mono-opt">{o}</span>
                    </button>
                  );
                })}
              </div>
            </>
          )}
          {ex.kind === "predict" && (
            <>
              <CodeBlock code={ex.code} lang={lang} />
              <textarea
                className="input mono ex-out"
                rows={Math.max(2, ex.expected.split("\n").length)}
                disabled={!!result}
                placeholder="Exact output"
                value={(answers[i] as string) ?? ""}
                onChange={(e) => setAnswers((a) => a.map((v, k) => (k === i ? e.target.value : v)))}
              />
              {result && !correct(i) && (
                <p className="note">
                  Expected: <code>{ex.expected.trim().replace(/\n/g, " ⏎ ")}</code>
                </p>
              )}
            </>
          )}
        </section>
      ))}

      {!result && (
        <button className="btn btn-gold btn-lg" disabled={answers.some((a) => a === null || a === "")} onClick={submit}>
          Check my answers
        </button>
      )}
    </div>
  );
}
