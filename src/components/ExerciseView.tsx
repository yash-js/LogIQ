import { useEffect, useMemo, useState, type MutableRefObject } from "react";
import type { Lang } from "../content";
import { Markdown } from "./Markdown";
import { CodeEditor } from "./CodeEditor";
import { blankCorrect, predictCorrect, runAndCompare, shuffled, type Exercise } from "../lib/basecamp";
import { useProgress } from "../lib/progress";
import { inTauri } from "../lib/runner";

export interface Verdict {
  correct: boolean;
  /** Code couldn't run (missing runtime / compile error): shown, but no life lost. */
  error?: string;
  got?: string;
}

export type Checker = MutableRefObject<null | (() => Promise<Verdict>)>;

const FENCE: Record<Lang, string> = { java: "java", python: "python", javascript: "javascript" };

export function CodeBlock({ code, lang }: { code: string; lang: Lang }) {
  return <Markdown text={"```" + FENCE[lang] + "\n" + code + "\n```"} />;
}

export function ExerciseView({
  ex,
  lang,
  seed,
  locked,
  checker,
  setReady,
}: {
  ex: Exercise;
  lang: Lang;
  seed: string;
  locked: boolean;
  checker: Checker;
  setReady(r: boolean): void;
}) {
  const settings = useProgress((s) => s.settings);
  const prefs = { pythonCmd: settings.pythonCmd, javaHome: settings.javaHome, nodeCmd: settings.nodeCmd };

  // ---------------------------------------------------------------- choice
  const [pick, setPick] = useState<number | null>(null);
  // ---------------------------------------------------------------- predict
  const [typed, setTyped] = useState("");
  // ---------------------------------------------------------------- blank
  const [fills, setFills] = useState<string[]>(() => (ex.kind === "blank" ? ex.blanks.map(() => "") : []));
  // ---------------------------------------------------------------- order
  const pool0 = useMemo(() => (ex.kind === "order" ? shuffled(ex.lines.map((_, i) => i), seed) : []), [ex, seed]);
  const [placed, setPlaced] = useState<number[]>([]);
  // ---------------------------------------------------------------- fix / write
  const [code, setCode] = useState(ex.kind === "fix" || ex.kind === "write" ? ex.code : "");

  useEffect(() => {
    let ready = false;
    if (ex.kind === "choice") ready = pick !== null;
    if (ex.kind === "predict") ready = typed.trim().length > 0;
    if (ex.kind === "blank") ready = fills.every((f) => f.trim());
    if (ex.kind === "order") ready = placed.length === ex.lines.length;
    if (ex.kind === "fix" || ex.kind === "write") ready = code.trim().length > 0;
    setReady(ready);
  }, [ex, pick, typed, fills, placed, code, setReady]);

  checker.current = async () => {
    switch (ex.kind) {
      case "choice":
        return { correct: pick === ex.answer };
      case "predict":
        return { correct: predictCorrect(ex.expected, typed), got: typed };
      case "blank":
        return { correct: blankCorrect(fills, ex.blanks).every(Boolean) };
      case "order": {
        const lines = placed.map((i) => ex.lines[i]);
        if (lines.every((l, i) => l === ex.lines[i])) return { correct: true };
        // A different order can still be right (e.g. two independent declarations): run it.
        if (!inTauri) return { correct: false };
        const r = await runAndCompare(lang, lines.join("\n"), ex.full, [{ input: ex.stdin, output: ex.expected }], prefs);
        return { correct: r.ok, got: r.got ?? r.error };
      }
      case "fix": {
        const r = await runAndCompare(lang, code, ex.full, [{ input: ex.stdin, output: ex.expected }], prefs);
        return { correct: r.ok, error: r.error, got: r.got };
      }
      case "write": {
        const r = await runAndCompare(lang, code, ex.full, ex.tests, prefs);
        return { correct: r.ok, error: r.error, got: r.got };
      }
    }
  };

  return (
    <div className="ex">
      <div className="ex-kind">
        {
          {
            choice: "Pick one",
            predict: "Predict the output",
            blank: "Fill the blanks",
            order: "Put the lines in order",
            fix: "Fix the bug",
            write: "Write it yourself",
          }[ex.kind]
        }
      </div>
      <h2 className="ex-prompt">
        <Markdown text={ex.prompt} />
      </h2>

      {ex.kind === "choice" && (
        <>
          {ex.code && <CodeBlock code={ex.code} lang={lang} />}
          <div className="quiz-opts">
            {ex.options.map((o, i) => (
              <button key={i} className={`quiz-opt ${pick === i ? "picked" : ""}`} disabled={locked} onClick={() => setPick(i)}>
                <span className="k">{"ABCD"[i]}</span>
                <span className="mono-opt">{o}</span>
              </button>
            ))}
          </div>
        </>
      )}

      {ex.kind === "predict" && (
        <>
          <CodeBlock code={ex.code} lang={lang} />
          <label className="ex-label" htmlFor="out">
            Output, exactly as printed
          </label>
          <textarea
            id="out"
            className="input mono ex-out"
            rows={Math.max(2, ex.expected.split("\n").length)}
            value={typed}
            disabled={locked}
            onChange={(e) => setTyped(e.target.value)}
            placeholder="Type what appears on screen"
            autoFocus
          />
        </>
      )}

      {ex.kind === "blank" && (
        <pre className="ex-code blank-code">
          {ex.code.split("___").map((part, i, arr) => (
            <span key={i}>
              {part}
              {i < arr.length - 1 && (
                <input
                  className="blank-input"
                  aria-label={`Blank ${i + 1}`}
                  value={fills[i]}
                  disabled={locked}
                  size={Math.max(3, (fills[i] || "").length + 1)}
                  onChange={(e) => setFills((f) => f.map((v, k) => (k === i ? e.target.value : v)))}
                  autoFocus={i === 0}
                  spellCheck={false}
                />
              )}
            </span>
          ))}
        </pre>
      )}

      {ex.kind === "order" && (
        <div className="order">
          <div className="order-col">
            <div className="ex-label">Your program</div>
            <div className="order-target">
              {placed.length === 0 && <div className="order-empty">Click lines below in the order they should run.</div>}
              {placed.map((li, k) => (
                <button key={li} className="order-line" disabled={locked} onClick={() => setPlaced((p) => p.filter((x) => x !== li))} title="Click to remove">
                  <span className="ln">{k + 1}</span>
                  <code>{ex.lines[li]}</code>
                </button>
              ))}
            </div>
          </div>
          <div className="order-col">
            <div className="ex-label">Lines</div>
            <div className="order-pool">
              {pool0
                .filter((li) => !placed.includes(li))
                .map((li) => (
                  <button key={li} className="order-line" disabled={locked} onClick={() => setPlaced((p) => [...p, li])}>
                    <code>{ex.lines[li]}</code>
                  </button>
                ))}
            </div>
          </div>
        </div>
      )}

      {(ex.kind === "fix" || ex.kind === "write") && (
        <>
          {ex.kind === "fix" && ex.stdin && (
            <p className="note">
              Input: <code>{ex.stdin.trim()}</code>
            </p>
          )}
          {ex.kind === "write" && (
            <p className="note">
              Checked with {ex.tests.length} inputs, e.g. <code>{ex.tests[0].input.trim().replace(/\n/g, " ⏎ ")}</code> →{" "}
              <code>{ex.tests[0].output.trim()}</code>
            </p>
          )}
          {lang === "java" && !ex.full && <p className="note">Write the lines inside <code>main</code>; LogicQuest adds the class around them.</p>}
          <div className="ex-editor">
            <CodeEditor lang={lang} value={code} fontSize={settings.fontSize} onChange={setCode} onRun={() => {}} onSubmit={() => {}} />
          </div>
          {!inTauri && <p className="note">Code runs in the desktop app.</p>}
        </>
      )}
    </div>
  );
}
