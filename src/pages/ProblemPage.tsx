import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Link, Navigate, useNavigate, useParams } from "react-router-dom";
import confetti from "canvas-confetti";
import { phaseById, problemById, problemsInPhase, type Lang } from "../content";
import { Markdown } from "../components/Markdown";
import { CodeEditor } from "../components/CodeEditor";
import { useProgress } from "../lib/progress";
import { judge, runCustom, type JudgeResult, type TestResult } from "../lib/runner";
import { areProblemsOpen, dailyQuest, HINT_PENALTY, levelFromXp, levelTitle, xpFor } from "../lib/game";

type Mode = "run" | "submit" | "custom";

interface Celebration {
  xp: number;
  first: boolean;
  clean: boolean;
  quest: boolean;
  hints: number;
  levelUp?: number;
}

const VERDICT_TEXT: Record<TestResult["verdict"], string> = {
  accepted: "Passed",
  wrong: "Wrong answer",
  tle: "Time limit exceeded",
  runtime: "Runtime error",
};

function IO({ label, text }: { label: string; text: string }) {
  return (
    <div>
      <div className="io-label">{label}</div>
      <pre>{text.replace(/\n$/, "") || " "}</pre>
    </div>
  );
}

export function ProblemPage() {
  const { id = "" } = useParams();
  const nav = useNavigate();
  const problem = problemById.get(id);
  const state = useProgress();
  const { saveCode, takeHint, recordAttempt, recordSolve, setSettings } = state;
  const lang = state.settings.lang;
  const prog = state.problems[id];

  const [leftTab, setLeftTab] = useState<"problem" | "hints">("problem");
  const [consoleTab, setConsoleTab] = useState<"result" | "custom">("result");
  const [busy, setBusy] = useState<Mode | null>(null);
  const [result, setResult] = useState<{ mode: Mode; res: JudgeResult } | null>(null);
  const [selected, setSelected] = useState(0);
  const [customInput, setCustomInput] = useState("");
  const [customOut, setCustomOut] = useState<{ stdout: string; stderr: string; note?: string } | null>(null);
  const [celebration, setCelebration] = useState<Celebration | null>(null);

  const code = prog?.code?.[lang] ?? problem?.starter[lang] ?? "";
  const codeRef = useRef(code);
  codeRef.current = code;

  useEffect(() => {
    setResult(null);
    setCustomOut(null);
    setCelebration(null);
    setLeftTab("problem");
    if (problem) setCustomInput(problem.examples[0]?.input ?? "");
  }, [id, problem]);

  const prefs = useMemo(
    () => ({ pythonCmd: state.settings.pythonCmd, javaHome: state.settings.javaHome }),
    [state.settings.pythonCmd, state.settings.javaHome],
  );

  const run = useCallback(
    async (mode: "run" | "submit") => {
      if (!problem || busy) return;
      setBusy(mode);
      setConsoleTab("result");
      try {
        const tests = mode === "run" ? problem.examples : problem.tests;
        const res = await judge(problem, lang, codeRef.current, tests, problem.examples.length, prefs);
        setResult({ mode, res });
        const firstFail = res.results.findIndex((r) => r.verdict !== "accepted");
        setSelected(firstFail >= 0 ? firstFail : 0);

        if (mode === "submit" && res.kind === "ok") {
          const before = useProgress.getState();
          const p = before.problems[problem.id];
          const alreadySolved = !!p?.solvedAt;
          if (!alreadySolved) recordAttempt(problem.id);
          if (res.allPassed) {
            const hints = p?.hintsUsed ?? 0;
            const clean = !alreadySolved && (p?.attempts ?? 0) === 0 && hints === 0;
            const quest = dailyQuest(before)?.id === problem.id;
            const xp = xpFor(problem, hints, clean, quest);
            const lvBefore = levelFromXp(before.xp).level;
            const first = recordSolve(problem.id, lang, xp);
            const lvAfter = levelFromXp(useProgress.getState().xp).level;
            setCelebration({ xp, first, clean, quest, hints, levelUp: lvAfter > lvBefore ? lvAfter : undefined });
            if (first) {
              confetti({ particleCount: 140, spread: 75, origin: { y: 0.65 }, colors: ["#f2b544", "#22c55e", "#a855f7", "#ece8df"] });
            }
          }
        }
      } catch (e) {
        setResult({
          mode,
          res: { kind: "setup", message: e instanceof Error ? e.message : String(e), results: [], passed: 0, total: 0, allPassed: false },
        });
      } finally {
        setBusy(null);
      }
    },
    [problem, busy, lang, prefs, recordAttempt, recordSolve],
  );

  const runOnCustom = useCallback(async () => {
    if (!problem || busy) return;
    setBusy("custom");
    try {
      const raw = await runCustom(lang, codeRef.current, customInput.endsWith("\n") ? customInput : customInput + "\n", problem.timeLimitMs, prefs);
      if (raw.setupError) setCustomOut({ stdout: "", stderr: raw.setupError });
      else if (raw.compileError) setCustomOut({ stdout: "", stderr: raw.compileError, note: "Compilation failed" });
      else {
        const r = raw.results[0];
        setCustomOut({ stdout: r.stdout, stderr: r.stderr, note: r.status === "tle" ? "Time limit exceeded" : `${r.timeMs} ms` });
      }
    } finally {
      setBusy(null);
    }
  }, [problem, busy, lang, customInput, prefs]);

  if (!problem) return <Navigate to="/" replace />;
  if (!areProblemsOpen(state, problem.phase)) return <Navigate to={`/phase/${problem.phase}`} replace />;

  const phase = phaseById(problem.phase)!;
  const siblings = problemsInPhase(problem.phase);
  const idx = siblings.findIndex((p) => p.id === problem.id);
  const next = siblings[idx + 1];
  const hintsUsed = prog?.hintsUsed ?? 0;
  const solved = !!prog?.solvedAt;
  const worth = xpFor(problem, hintsUsed, false, false);

  const selectedTest = result?.res.results[selected];

  return (
    <div className="workspace" style={{ ["--c" as string]: phase.color }}>
      <section className="ws-left">
        <div className="tabs">
          <button className={leftTab === "problem" ? "on" : ""} onClick={() => setLeftTab("problem")}>
            Problem
          </button>
          <button className={leftTab === "hints" ? "on" : ""} onClick={() => setLeftTab("hints")}>
            Hints {hintsUsed > 0 && `(${hintsUsed}/3)`}
          </button>
          <span className="spacer" />
          <Link to={`/phase/${problem.phase}`} className="btn btn-ghost small" style={{ alignSelf: "center", padding: "4px 10px" }}>
            {phase.world}
          </Link>
        </div>
        <div className="ws-scroll">
          {leftTab === "problem" ? (
            <>
              <div className="prob-title">
                <span className="muted">
                  {idx + 1}/{siblings.length}
                </span>
                <h1>{problem.title}</h1>
              </div>
              <div className="prob-meta">
                <span className={`chip diff-${problem.difficulty}`}>{problem.difficulty}</span>
                <span className="chip" style={{ color: "var(--gold)" }}>
                  {solved ? `Solved · ${prog?.xpEarned} XP earned` : `${worth} XP`}
                </span>
                {problem.concepts.map((c) => (
                  <span className="chip" key={c}>
                    {c}
                  </span>
                ))}
              </div>
              <Markdown text={problem.statement} />
              {problem.examples.map((ex, i) => (
                <div key={i}>
                  <h3 style={{ marginTop: 20 }}>Example {i + 1}</h3>
                  <div className="io">
                    <IO label="Input" text={ex.input} />
                    <IO label="Output" text={ex.output} />
                  </div>
                </div>
              ))}
              <p className="small muted">
                {problem.mode === "print"
                  ? "Print the output yourself inside solve()."
                  : "Return the answer from solve(); reading input and printing are already done for you."}{" "}
                {problem.tests.length - problem.examples.length} hidden tests run on Submit.
              </p>
              {problem.practice && (
                <p className="small">
                  Practice more:{" "}
                  <a href={problem.practice.url} target="_blank" rel="noreferrer">
                    {problem.practice.label}
                  </a>
                </p>
              )}
            </>
          ) : (
            <>
              <h2 style={{ marginBottom: 6 }}>Hints</h2>
              <p className="muted small" style={{ marginTop: 0 }}>
                Each hint you open before solving takes {HINT_PENALTY * 100}% off this problem's XP. Try for a few minutes
                first; the first hint is usually a question, not an answer.
              </p>
              {problem.hints.map((h, i) => {
                const unlocked = i < hintsUsed || solved;
                const nextUp = i === hintsUsed && !solved;
                return (
                  <div key={i} className={`hint ${unlocked ? "" : "locked"}`}>
                    <div className="hint-head">
                      <strong>Hint {i + 1}</strong>
                      {!unlocked && (
                        <button className="btn small" disabled={!nextUp} onClick={() => takeHint(problem.id)}>
                          {nextUp ? `Reveal (−${HINT_PENALTY * 100}% XP)` : `Open hint ${i} first`}
                        </button>
                      )}
                    </div>
                    {unlocked && <p>{h}</p>}
                  </div>
                );
              })}
            </>
          )}
        </div>
      </section>

      <section className="ws-right">
        <div className="editor-bar">
          <div className="seg" role="group" aria-label="Language">
            {(["java", "python"] as Lang[]).map((l) => (
              <button key={l} className={lang === l ? "on" : ""} onClick={() => setSettings({ lang: l })}>
                {l === "java" ? "Java" : "Python"}
              </button>
            ))}
          </div>
          <span className="small muted">
            {lang === "java" ? "JDK on your machine" : "Python 3 on your machine"} · Ctrl+Enter runs, Ctrl+Shift+Enter submits
          </span>
          <span style={{ flex: 1 }} />
          <button
            className="btn btn-ghost small"
            style={{ padding: "4px 10px" }}
            onClick={() => {
              if (confirm("Replace your code with the starter template?")) saveCode(problem.id, lang, problem.starter[lang]);
            }}
          >
            Reset code
          </button>
        </div>
        <div className="editor-wrap">
          <CodeEditor
            key={`${problem.id}-${lang}`}
            lang={lang}
            value={code}
            fontSize={state.settings.fontSize}
            onChange={(v) => saveCode(problem.id, lang, v)}
            onRun={() => void run("run")}
            onSubmit={() => void run("submit")}
          />
        </div>
        <div className="console">
          <div className="tabs">
            <button className={consoleTab === "result" ? "on" : ""} onClick={() => setConsoleTab("result")}>
              Result
            </button>
            <button className={consoleTab === "custom" ? "on" : ""} onClick={() => setConsoleTab("custom")}>
              Custom input
            </button>
          </div>
          <div className="console-body">
            {consoleTab === "result" ? (
              busy && busy !== "custom" ? (
                <p className="muted">{busy === "submit" ? `Running ${problem.tests.length} tests…` : "Running examples…"}</p>
              ) : !result ? (
                <p className="muted">Run checks the examples. Submit runs every test and awards XP.</p>
              ) : result.res.kind === "setup" ? (
                <div className="notice bad">
                  {result.res.message} <Link to="/settings">Open settings</Link>
                </div>
              ) : result.res.kind === "compile" ? (
                <>
                  <div className="verdict bad">Compilation error</div>
                  <pre className="errblock">{result.res.message}</pre>
                </>
              ) : (
                <>
                  <div className={`verdict ${result.res.allPassed ? "good" : "bad"}`}>
                    {result.res.allPassed
                      ? result.mode === "submit"
                        ? "Accepted"
                        : "Examples pass. Now submit."
                      : VERDICT_TEXT[result.res.results.find((r) => r.verdict !== "accepted")!.verdict]}
                    <span className="small muted">
                      {result.res.passed}/{result.res.total} tests passed
                    </span>
                  </div>
                  <div className="testpills">
                    {result.res.results.map((r, i) => (
                      <button
                        key={i}
                        className={`testpill ${r.verdict === "accepted" ? "pass" : "fail"} ${i === selected ? "sel" : ""}`}
                        onClick={() => setSelected(i)}
                      >
                        {r.hidden ? "Hidden " : "Example "}
                        {r.hidden ? i - problem.examples.length + 1 : i + 1}
                      </button>
                    ))}
                  </div>
                  {selectedTest && (
                    <>
                      <div className="io">
                        <IO label="Input" text={selectedTest.input} />
                        <IO label="Expected" text={selectedTest.expected} />
                      </div>
                      <div className="io" style={{ gridTemplateColumns: "1fr" }}>
                        <IO label={`Your output · ${selectedTest.timeMs} ms`} text={selectedTest.stdout} />
                      </div>
                      {selectedTest.stderr && <pre className="errblock">{selectedTest.stderr}</pre>}
                      {selectedTest.verdict === "tle" && (
                        <p className="small muted">Stopped after the time limit. Look for a loop that never ends, or work that repeats.</p>
                      )}
                    </>
                  )}
                </>
              )
            ) : (
              <div className="io">
                <div>
                  <div className="io-label">Input (same format as the examples)</div>
                  <textarea
                    className="input"
                    style={{ width: "100%", height: 150, fontFamily: "var(--mono)", fontSize: 13 }}
                    value={customInput}
                    onChange={(e) => setCustomInput(e.target.value)}
                  />
                </div>
                <div>
                  <div className="io-label">Output {customOut?.note && `· ${customOut.note}`}</div>
                  <pre style={{ height: 150 }}>{busy === "custom" ? "Running…" : customOut?.stdout || " "}</pre>
                  {customOut?.stderr && <pre className="errblock" style={{ marginTop: 8 }}>{customOut.stderr}</pre>}
                </div>
              </div>
            )}
          </div>
          <div className="console-actions">
            {solved && <span className="small" style={{ color: "var(--good)" }}>Solved{prog?.solvedIn?.length === 2 ? " in Java and Python" : ""}</span>}
            <span className="spacer" />
            {consoleTab === "custom" ? (
              <button className="btn" disabled={!!busy} onClick={() => void runOnCustom()}>
                Run with this input
              </button>
            ) : (
              <button className="btn" disabled={!!busy} onClick={() => void run("run")}>
                Run
              </button>
            )}
            <button className="btn btn-gold" disabled={!!busy} onClick={() => void run("submit")}>
              Submit
            </button>
          </div>
        </div>
      </section>

      {celebration && (
        <div className="overlay" onClick={() => setCelebration(null)}>
          <div className="celebrate" onClick={(e) => e.stopPropagation()} role="dialog" aria-label="Problem solved">
            {celebration.first ? (
              <>
                <div className="big">+{celebration.xp}</div>
                <h2>Solved: {problem.title}</h2>
                {celebration.levelUp && (
                  <div className="levelup">
                    Level {celebration.levelUp} reached: {levelTitle(celebration.levelUp)}
                  </div>
                )}
                <ul>
                  <li>Base {problem.xp} XP</li>
                  {celebration.hints > 0 && (
                    <li>
                      {celebration.hints} hint{celebration.hints > 1 ? "s" : ""}: −{Math.min(75, celebration.hints * HINT_PENALTY * 100)}%
                    </li>
                  )}
                  {celebration.clean && <li>Clean solve, first submit and no hints: +5</li>}
                  {celebration.quest && <li>Today's quest: double XP</li>}
                </ul>
              </>
            ) : (
              <>
                <h2>Accepted again</h2>
                <ul>
                  <li>XP is awarded once per problem. Solving it in the other language counts toward Bilingual.</li>
                </ul>
              </>
            )}
            <div className="actions">
              <button className="btn" onClick={() => setCelebration(null)}>
                Stay here
              </button>
              {next ? (
                <button className="btn btn-gold" onClick={() => nav(`/problem/${next.id}`)}>
                  Next: {next.title}
                </button>
              ) : (
                <button className="btn btn-gold" onClick={() => nav(`/`)}>
                  Back to the map
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
