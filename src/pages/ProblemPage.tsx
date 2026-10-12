import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Link, Navigate, useNavigate, useParams } from "react-router-dom";
import confetti from "canvas-confetti";
import { LANGS, phaseById, problemById, problemsInPhase } from "../content";
import { Markdown } from "../components/Markdown";
import { CodeEditor } from "../components/CodeEditor";
import { WorldGlyph } from "../components/WorldGlyph";
import { useProgress } from "../lib/progress";
import { judge, runCustom, type JudgeResult, type TestResult } from "../lib/runner";
import { findShortcuts, type Shortcut } from "../lib/builtins";
import { areProblemsOpen, dailyQuest, HINT_PENALTY, levelFromXp, levelTitle, pureBonus, xpFor } from "../lib/game";

type Mode = "run" | "submit" | "custom";
type LeftTab = "problem" | "hints" | "pure";

interface Celebration {
  kind: "first" | "pure" | "again";
  xp: number;
  base: number;
  clean: boolean;
  quest: boolean;
  hints: number;
  pureXp: number;
  shortcuts: Shortcut[];
  levelUp?: number;
}

const VERDICT: Record<TestResult["verdict"], string> = {
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

function useDebounced<T>(value: T, ms: number) {
  const [v, setV] = useState(value);
  useEffect(() => {
    const t = setTimeout(() => setV(value), ms);
    return () => clearTimeout(t);
  }, [value, ms]);
  return v;
}

export function ProblemPage() {
  const { id = "" } = useParams();
  const nav = useNavigate();
  const problem = problemById.get(id);
  const state = useProgress();
  const { saveCode, takeHint, recordAttempt, recordSolve, recordPure, setSettings, setLastOpened } = state;
  const lang = state.settings.lang;
  const prog = state.problems[id];

  const [leftTab, setLeftTab] = useState<LeftTab>("problem");
  const [consoleTab, setConsoleTab] = useState<"result" | "custom">("result");
  const [busy, setBusy] = useState<Mode | null>(null);
  const [result, setResult] = useState<{ mode: Mode; res: JudgeResult } | null>(null);
  const [selected, setSelected] = useState(0);
  const [customInput, setCustomInput] = useState("");
  const [customOut, setCustomOut] = useState<{ stdout: string; stderr: string; note?: string } | null>(null);
  const [celebration, setCelebration] = useState<Celebration | null>(null);
  const [leftW, setLeftW] = useState(() => Math.round(window.innerWidth * 0.36));
  const [consoleH, setConsoleH] = useState(280);
  const [drag, setDrag] = useState<null | "x" | "y">(null);
  const bodyRef = useRef<HTMLDivElement>(null);

  const code = prog?.code?.[lang] ?? problem?.starter[lang] ?? "";
  const codeRef = useRef(code);
  codeRef.current = code;
  const debounced = useDebounced(code, 350);
  const shortcuts = useMemo(() => (problem ? findShortcuts(debounced, lang, problem) : []), [debounced, lang, problem]);

  useEffect(() => {
    setResult(null);
    setCustomOut(null);
    setCelebration(null);
    setLeftTab("problem");
    if (problem) {
      setCustomInput(problem.examples[0]?.input ?? "");
      setLastOpened(problem.id);
    }
  }, [id, problem, setLastOpened]);

  // Drag to resize the panes.
  useEffect(() => {
    if (!drag) return;
    const move = (e: MouseEvent) => {
      const r = bodyRef.current?.getBoundingClientRect();
      if (!r) return;
      if (drag === "x") setLeftW(Math.min(Math.max(e.clientX - r.left, 320), r.width - 420));
      else setConsoleH(Math.min(Math.max(r.bottom - e.clientY, 140), r.height - 160));
    };
    const up = () => setDrag(null);
    window.addEventListener("mousemove", move);
    window.addEventListener("mouseup", up);
    return () => {
      window.removeEventListener("mousemove", move);
      window.removeEventListener("mouseup", up);
    };
  }, [drag]);

  const prefs = useMemo(
    () => ({ pythonCmd: state.settings.pythonCmd, javaHome: state.settings.javaHome, nodeCmd: state.settings.nodeCmd }),
    [state.settings.pythonCmd, state.settings.javaHome, state.settings.nodeCmd],
  );

  const run = useCallback(
    async (mode: "run" | "submit") => {
      if (!problem || busy) return;
      setBusy(mode);
      setConsoleTab("result");
      try {
        const tests = mode === "run" ? problem.examples : problem.tests;
        const src = codeRef.current;
        const res = await judge(problem, lang, src, tests, problem.examples.length, prefs);
        setResult({ mode, res });
        const firstFail = res.results.findIndex((r) => r.verdict !== "accepted");
        setSelected(firstFail >= 0 ? firstFail : 0);

        if (mode === "submit" && res.kind === "ok") {
          const before = useProgress.getState();
          const p = before.problems[problem.id];
          const alreadySolved = !!p?.solvedAt;
          if (!alreadySolved) recordAttempt(problem.id);
          if (res.allPassed) {
            const used = findShortcuts(src, lang, problem);
            const isPure = used.length === 0;
            const hints = p?.hintsUsed ?? 0;
            const bonus = pureBonus(problem);
            const lvBefore = levelFromXp(before.xp).level;
            let c: Celebration;
            if (!alreadySolved) {
              const clean = (p?.attempts ?? 0) === 0 && hints === 0;
              const quest = dailyQuest(before)?.id === problem.id;
              const base = xpFor(problem, hints, clean, quest);
              const xp = base + (isPure ? bonus : 0);
              recordSolve(problem.id, lang, xp, isPure);
              c = { kind: "first", xp, base, clean, quest, hints, pureXp: isPure ? bonus : 0, shortcuts: used };
            } else if (isPure && !p?.pure) {
              recordSolve(problem.id, lang, 0, true);
              recordPure(problem.id, bonus);
              c = { kind: "pure", xp: bonus, base: 0, clean: false, quest: false, hints: 0, pureXp: bonus, shortcuts: [] };
            } else {
              recordSolve(problem.id, lang, 0, isPure);
              c = { kind: "again", xp: 0, base: 0, clean: false, quest: false, hints: 0, pureXp: 0, shortcuts: used };
            }
            const lvAfter = levelFromXp(useProgress.getState().xp).level;
            if (lvAfter > lvBefore) c.levelUp = lvAfter;
            setCelebration(c);
            if (c.kind !== "again") {
              confetti({ particleCount: 150, spread: 80, origin: { y: 0.6 }, disableForReducedMotion: true, colors: ["#ffc24b", "#34d399", "#c084fc", "#22d3ee", "#f2eee6"] });
            }
          }
        }
      } catch (e) {
        setResult({ mode, res: { kind: "setup", message: e instanceof Error ? e.message : String(e), results: [], passed: 0, total: 0, allPassed: false } });
      } finally {
        setBusy(null);
      }
    },
    [problem, busy, lang, prefs, recordAttempt, recordSolve, recordPure],
  );

  const runOnCustom = useCallback(async () => {
    if (!problem || busy) return;
    setBusy("custom");
    try {
      const input = customInput.endsWith("\n") ? customInput : customInput + "\n";
      const raw = await runCustom(lang, codeRef.current, input, problem.timeLimitMs, prefs);
      if (raw.setupError) setCustomOut({ stdout: "", stderr: raw.setupError });
      else if (raw.compileError) setCustomOut({ stdout: "", stderr: raw.compileError, note: "compilation failed" });
      else {
        const r = raw.results[0];
        setCustomOut({ stdout: r.stdout, stderr: r.stderr, note: r.status === "tle" ? "time limit exceeded" : `${r.timeMs} ms` });
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
  const prev = siblings[idx - 1];
  const next = siblings[idx + 1];
  const hintsUsed = prog?.hintsUsed ?? 0;
  const solved = !!prog?.solvedAt;
  const worth = xpFor(problem, hintsUsed, false, false);
  const bonus = pureBonus(problem);
  const sel = result?.res.results[selected];

  return (
    <div className="ws" style={{ ["--c" as string]: phase.color }}>
      <header className="ws-head">
        <div className="crumbs">
          <span className="dot" />
          <Link to={`/phase/${phase.id}`}>{phase.world}</Link>
          <span>·</span>
          <span className="tnum">
            {idx + 1} of {siblings.length}
          </span>
        </div>
        <h1>{problem.title}</h1>
        <span className={`pill ${problem.difficulty}`}>{problem.difficulty}</span>
        {solved ? (
          <span className="pill xp">{prog?.xpEarned} XP earned</span>
        ) : (
          <span className="pill xp">
            {worth} XP{" "}
            <span className="muted" style={{ fontWeight: 500 }}>
              +{bonus} Pure
            </span>
          </span>
        )}
        {prog?.pure && <span className="pill pure">Pure solve</span>}
        <span className="spacer" />
        <button className="btn btn-ghost btn-sm" disabled={!prev} onClick={() => prev && nav(`/problem/${prev.id}`)}>
          ← Previous
        </button>
        <button className="btn btn-ghost btn-sm" disabled={!next} onClick={() => next && nav(`/problem/${next.id}`)}>
          Next →
        </button>
      </header>

      <div className="ws-body" ref={bodyRef} style={{ gridTemplateColumns: `${leftW}px 7px 1fr`, userSelect: drag ? "none" : undefined }}>
        <section className="ws-pane">
          <div className="tabs">
            <button className={leftTab === "problem" ? "on" : ""} onClick={() => setLeftTab("problem")}>
              Problem
            </button>
            <button className={leftTab === "hints" ? "on" : ""} onClick={() => setLeftTab("hints")}>
              Hints<span className="count">{hintsUsed}/3</span>
            </button>
            <button className={leftTab === "pure" ? "on" : ""} onClick={() => setLeftTab("pure")}>
              Pure challenge{shortcuts.length > 0 && <span className="count">{shortcuts.length}</span>}
            </button>
          </div>
          <div className="scroll">
            {leftTab === "problem" && (
              <div className="statement">
                <div className="prob-pills">
                  {problem.concepts.map((c) => (
                    <span className="pill" key={c}>
                      {c}
                    </span>
                  ))}
                </div>
                <Markdown text={problem.statement} />
                {problem.examples.map((ex, i) => (
                  <div className="example" key={i}>
                    <div className="example-head">Example {i + 1}</div>
                    <div className="io">
                      <IO label="Input" text={ex.input} />
                      <IO label="Output" text={ex.output} />
                    </div>
                  </div>
                ))}
                <p className="note">
                  {problem.mode === "print"
                    ? "Print the output yourself inside solve()."
                    : "Return the answer from solve(). Reading input and printing are already done for you."}{" "}
                  Submit also runs {problem.tests.length - problem.examples.length} hidden tests.
                </p>
                {problem.practice && (
                  <p className="note">
                    More practice:{" "}
                    <a href={problem.practice.url} target="_blank" rel="noreferrer">
                      {problem.practice.label}
                    </a>
                  </p>
                )}
              </div>
            )}

            {leftTab === "hints" && (
              <>
                <h2 style={{ marginBottom: 6 }}>Hints</h2>
                <p className="note" style={{ marginTop: 0 }}>
                  Each hint opened before you solve takes {HINT_PENALTY * 100}% off this problem's XP. The first one is a question, not an answer.
                </p>
                {problem.hints.map((h, i) => {
                  const unlocked = i < hintsUsed || solved;
                  const nextUp = i === hintsUsed && !solved;
                  return (
                    <div key={i} className={`hint ${unlocked ? "" : "locked"}`}>
                      <div className="hint-head">
                        <h3>Hint {i + 1}</h3>
                        {!unlocked && (
                          <button className="btn btn-sm" disabled={!nextUp} onClick={() => takeHint(problem.id)}>
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

            {leftTab === "pure" && (
              <>
                <h2 style={{ marginBottom: 6 }}>Pure challenge</h2>
                <p className="note" style={{ marginTop: 0 }}>
                  Solve it with plain loops, conditions, arrays and strings, without library shortcuts like sort, Set, max() or
                  reverse(). A pure solution earns <b style={{ color: "var(--gold)" }}>+{bonus} XP</b>. Using shortcuts is allowed; you
                  just don't get the bonus until you solve it without them.
                </p>
                {prog?.pure ? (
                  <div className="notice good">Done. You solved this one without shortcuts.</div>
                ) : shortcuts.length === 0 ? (
                  <div className="notice good">Your current code uses no library shortcuts.</div>
                ) : (
                  <div className="shortcut-list">
                    {shortcuts.map((s) => (
                      <div className="shortcut" key={s.id}>
                        <b>{s.label}</b>
                        <code>{s.found}</code>
                        <p>{s.tip}</p>
                      </div>
                    ))}
                  </div>
                )}
              </>
            )}
          </div>
        </section>

        <div className={`ws-split ${drag === "x" ? "drag" : ""}`} onMouseDown={() => setDrag("x")} role="separator" aria-orientation="vertical" />

        <section className="ws-pane" style={{ display: "grid", gridTemplateRows: `44px 1fr 6px ${consoleH}px` }}>
          <div className="editor-bar">
            <div className="lang-tabs" role="radiogroup" aria-label="Language">
              {LANGS.map((l) => (
                <button key={l.id} role="radio" aria-checked={lang === l.id} className={lang === l.id ? "on" : ""} onClick={() => setSettings({ lang: l.id })}>
                  <span className={`lang-dot ${l.id}`} />
                  {l.label}
                </button>
              ))}
            </div>
            <span className="spacer" />
            <button
              className={`sc-chip ${shortcuts.length ? "used" : "clean"}`}
              onClick={() => setLeftTab("pure")}
              title="Library helpers detected in your code"
            >
              {shortcuts.length ? `Shortcuts: ${shortcuts.map((s) => s.found.replace(/\s*\($/, "")).join(", ")}` : "No shortcuts"}
            </button>
            <button
              className="btn btn-ghost btn-sm"
              onClick={() => {
                if (confirm("Replace your code with the starter template?")) saveCode(problem.id, lang, problem.starter[lang]);
              }}
            >
              Reset
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
          <div
            className={`ws-split ${drag === "y" ? "drag" : ""}`}
            style={{ width: "auto", height: 6, cursor: "row-resize" }}
            onMouseDown={() => setDrag("y")}
            role="separator"
            aria-orientation="horizontal"
          />
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
                  <div className="empty-console">{busy === "submit" ? `Running ${problem.tests.length} tests…` : "Running the examples…"}</div>
                ) : !result ? (
                  <div className="empty-console">
                    Run checks the examples <span className="kbd">Ctrl+Enter</span>. Submit runs every test and awards XP{" "}
                    <span className="kbd">Ctrl+Shift+Enter</span>.
                  </div>
                ) : result.res.kind === "setup" ? (
                  <div className="notice bad">
                    <span>{result.res.message}</span>
                    <Link to="/settings" className="btn btn-sm">
                      Open settings
                    </Link>
                  </div>
                ) : result.res.kind === "compile" ? (
                  <>
                    <div className="verdict bad">
                      <b>Compilation error</b>
                    </div>
                    <pre className="errblock">{result.res.message}</pre>
                  </>
                ) : (
                  <>
                    <div className={`verdict ${result.res.allPassed ? "good" : "bad"}`}>
                      <b>
                        {result.res.allPassed
                          ? result.mode === "submit"
                            ? "Accepted"
                            : "Examples pass"
                          : VERDICT[result.res.results.find((r) => r.verdict !== "accepted")!.verdict]}
                      </b>
                      <span className="small muted tnum">
                        {result.res.passed}/{result.res.total} tests passed
                        {result.res.allPassed && result.mode === "run" && " · now Submit"}
                      </span>
                    </div>
                    <div className="tests">
                      {result.res.results.map((r, i) => (
                        <button key={i} className={`tchip ${r.verdict === "accepted" ? "" : "fail"} ${i === selected ? "sel" : ""}`} onClick={() => setSelected(i)}>
                          {r.hidden ? `Hidden ${i - problem.examples.length + 1}` : `Example ${i + 1}`}
                        </button>
                      ))}
                    </div>
                    {sel && (
                      <>
                        <div className="result-io">
                          <div className="io">
                            <IO label="Input" text={sel.input} />
                            <IO label="Expected output" text={sel.expected} />
                          </div>
                          <div className="io" style={{ gridTemplateColumns: "1fr" }}>
                            <IO label={`Your output · ${sel.timeMs} ms`} text={sel.stdout} />
                          </div>
                        </div>
                        {sel.stderr && <pre className="errblock">{sel.stderr}</pre>}
                        {sel.verdict === "tle" && <p className="note">Stopped at the time limit. Look for a loop that never ends, or work that repeats.</p>}
                      </>
                    )}
                  </>
                )
              ) : (
                <div className="result-io">
                  <div className="io">
                    <div>
                      <div className="io-label">Input, same format as the examples</div>
                      <textarea
                        className="mono"
                        style={{ width: "100%", height: 140, background: "transparent", border: 0, padding: "6px 14px", resize: "none", fontSize: 13, color: "var(--ink)", outline: "none" }}
                        value={customInput}
                        onChange={(e) => setCustomInput(e.target.value)}
                      />
                    </div>
                    <div>
                      <div className="io-label">Output {customOut?.note && `· ${customOut.note}`}</div>
                      <pre style={{ height: 140 }}>{busy === "custom" ? "Running…" : customOut?.stdout || " "}</pre>
                    </div>
                  </div>
                  {customOut?.stderr && <pre className="errblock" style={{ margin: 10 }}>{customOut.stderr}</pre>}
                </div>
              )}
            </div>
            <div className="console-actions">
              {solved && (
                <span className="small" style={{ color: "var(--good)" }}>
                  Solved in {(prog?.solvedIn ?? []).map((l) => LANGS.find((x) => x.id === l)?.label).join(", ")}
                </span>
              )}
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
      </div>

      {celebration && (
        <div className="overlay" onClick={() => setCelebration(null)}>
          <div className="celebrate" onClick={(e) => e.stopPropagation()} role="dialog" aria-label="Problem solved">
            {celebration.kind === "again" ? (
              <>
                <h2>Accepted again</h2>
                <p className="muted" style={{ marginTop: 0 }}>
                  XP is awarded once per problem.{" "}
                  {celebration.shortcuts.length > 0 && !prog?.pure
                    ? `The Pure bonus still needs a solution without ${celebration.shortcuts.map((s) => s.label).join(", ")}.`
                    : "Solving it in another language counts toward the language badges."}
                </p>
              </>
            ) : (
              <>
                <div className="badge-big">
                  <WorldGlyph id={phase.id} size={44} />
                </div>
                <div className="big">+{celebration.xp}</div>
                <h2>{celebration.kind === "pure" ? "Pure solve!" : `${problem.title} solved`}</h2>
                {celebration.levelUp && (
                  <div className="levelup">
                    Level {celebration.levelUp}: {levelTitle(celebration.levelUp)}
                  </div>
                )}
                {celebration.kind === "first" && (
                  <ul>
                    <li>
                      Base <b>{problem.xp}</b>
                    </li>
                    {celebration.hints > 0 && (
                      <li>
                        {celebration.hints} hint{celebration.hints > 1 ? "s" : ""} <b>−{Math.min(75, celebration.hints * HINT_PENALTY * 100)}%</b>
                      </li>
                    )}
                    {celebration.clean && (
                      <li>
                        First submit, no hints <b>+5</b>
                      </li>
                    )}
                    {celebration.quest && (
                      <li>
                        Today's quest <b>×2</b>
                      </li>
                    )}
                    {celebration.pureXp > 0 && (
                      <li>
                        Pure solve, no shortcuts <b>+{celebration.pureXp}</b>
                      </li>
                    )}
                  </ul>
                )}
                {celebration.kind === "first" && celebration.shortcuts.length > 0 && (
                  <div className="shortcut challenge">
                    <b>Now try it without shortcuts</b>
                    <p>
                      You used {celebration.shortcuts.map((s) => s.label).join(", ")}. Solve it again with only loops and conditions for{" "}
                      <b style={{ color: "var(--gold)" }}>+{bonus} XP</b>.
                    </p>
                  </div>
                )}
              </>
            )}
            <div className="actions">
              {celebration.kind === "first" && celebration.shortcuts.length > 0 ? (
                <button
                  className="btn btn-gold"
                  onClick={() => {
                    setCelebration(null);
                    setLeftTab("pure");
                  }}
                >
                  Take the Pure challenge
                </button>
              ) : (
                <button className="btn" onClick={() => setCelebration(null)}>
                  Stay here
                </button>
              )}
              {next ? (
                <button className={celebration.kind === "first" && celebration.shortcuts.length > 0 ? "btn" : "btn btn-gold"} onClick={() => nav(`/problem/${next.id}`)}>
                  Next problem
                </button>
              ) : (
                <button className="btn" onClick={() => nav(`/phase/${phase.id}`)}>
                  Back to {phase.world}
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
