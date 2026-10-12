import { useCallback, useRef, useState } from "react";
import { Link, Navigate, useNavigate, useParams } from "react-router-dom";
import confetti from "canvas-confetti";
import { Markdown } from "../components/Markdown";
import { ExerciseView, type Checker, type Verdict } from "../components/ExerciseView";
import { COMBO_FROM, findUnit, LIVES, PERFECT_BONUS, UNIT_BONUS, unitsFor, XP_PER_EXERCISE } from "../lib/basecamp";
import { useProgress } from "../lib/progress";
import { levelFromXp, levelTitle } from "../lib/game";
import { useToolchain } from "../lib/toolchain";
import { LANGS } from "../content";

type Stage = "intro" | "ex" | "done" | "out";

function Hearts({ lives }: { lives: number }) {
  return (
    <span className="hearts" aria-label={`${lives} lives left`}>
      {Array.from({ length: LIVES }, (_, i) => (
        <svg key={i} viewBox="0 0 24 24" width="22" height="22" className={i < lives ? "on" : ""} aria-hidden="true">
          <path d="M12 21s-7.5-4.6-9.6-9.2C.9 8.3 3.1 4.5 6.8 4.5c2.1 0 3.6 1.2 5.2 3.1 1.6-1.9 3.1-3.1 5.2-3.1 3.7 0 5.9 3.8 4.4 7.3C19.5 16.4 12 21 12 21z" />
        </svg>
      ))}
    </span>
  );
}

export function LessonPage() {
  const { unitId = "" } = useParams();
  const nav = useNavigate();
  const found = findUnit(unitId);
  const recordUnit = useProgress((s) => s.recordUnit);

  const [stage, setStage] = useState<Stage>("intro");
  const [idx, setIdx] = useState(0);
  const [lives, setLives] = useState(LIVES);
  const [combo, setCombo] = useState(0);
  const [bestCombo, setBestCombo] = useState(0);
  const [earned, setEarned] = useState(0);
  const [ready, setReady] = useState(false);
  const [busy, setBusy] = useState(false);
  const [verdict, setVerdict] = useState<Verdict | null>(null);
  const [attempt, setAttempt] = useState(0);
  /** Wrong answers on the current exercise. The answer is only revealed after two. */
  const [wrongs, setWrongs] = useState(0);
  const [summary, setSummary] = useState<{ gain: number; total: number; perfect: boolean; levelUp?: number } | null>(null);
  const checker: Checker = useRef(null);
  const tool = useToolchain();

  const restart = useCallback(() => {
    setStage("intro");
    setIdx(0);
    setLives(LIVES);
    setCombo(0);
    setBestCombo(0);
    setEarned(0);
    setVerdict(null);
    setWrongs(0);
    setAttempt((a) => a + 1);
  }, []);

  if (!found) return <Navigate to="/basecamp" replace />;
  const { lang, unit } = found;
  const peers = unitsFor(lang).filter((u) => u.section === unit.section);
  const place = peers.findIndex((u) => u.id === unit.id);
  const next = peers[place + 1];
  const ex = unit.exercises[idx];
  const needsRuntime = ex?.kind === "fix" || ex?.kind === "write";
  const runtimeBlocked = needsRuntime && tool.missing(lang);
  const runtimeTip = `Install ${LANGS.find((l) => l.id === lang)!.label} to run code`;

  async function check() {
    if (!checker.current || busy || runtimeBlocked) return;
    setBusy(true);
    try {
      const v = await checker.current();
      setVerdict(v);
      if (v.error) return; // couldn't run: show the message, no life lost
      if (v.correct) {
        const c = combo + 1;
        setCombo(c);
        setBestCombo((b) => Math.max(b, c));
        setEarned((e) => e + XP_PER_EXERCISE + (c >= COMBO_FROM ? 1 : 0));
      } else {
        setCombo(0);
        setLives((l) => l - 1);
        setWrongs((w) => w + 1);
      }
    } finally {
      setBusy(false);
    }
  }

  function advance() {
    if (verdict && !verdict.correct && !verdict.error && lives <= 0) {
      setStage("out");
      return;
    }
    if (verdict?.error || (verdict && !verdict.correct && wrongs < 2)) {
      // Wrong or couldn't run: try the same exercise again.
      setVerdict(null);
      setAttempt((a) => a + 1);
      return;
    }
    setVerdict(null);
    setWrongs(0);
    if (idx + 1 < unit.exercises.length) {
      setIdx(idx + 1);
      setAttempt((a) => a + 1);
      return;
    }
    const perfect = lives === LIVES;
    const total = earned + UNIT_BONUS + (perfect ? PERFECT_BONUS : 0);
    const before = levelFromXp(useProgress.getState().xp).level;
    const gain = recordUnit(lang, unit.id, total, perfect);
    const after = levelFromXp(useProgress.getState().xp).level;
    setSummary({ gain, total, perfect, levelUp: after > before ? after : undefined });
    setStage("done");
    confetti({ particleCount: 120, spread: 70, origin: { y: 0.6 }, disableForReducedMotion: true, colors: ["#ffc24b", "#34d399", "#c084fc", "#f2eee6"] });
  }

  const revealed = !!verdict && !verdict.error && !verdict.correct && (wrongs >= 2 || lives <= 0);
  const progress = stage === "done" ? 1 : stage === "intro" ? 0 : (idx + (verdict?.correct ? 1 : 0)) / unit.exercises.length;

  return (
    <div className="lesson">
      <header className="lesson-head">
        <Link to="/basecamp" className="btn btn-ghost btn-sm" aria-label="Leave lesson">
          ✕
        </Link>
        <div className="bar lesson-bar" style={{ ["--c" as string]: "var(--gold)" }}>
          <span style={{ width: `${progress * 100}%` }} />
        </div>
        {combo >= COMBO_FROM && <span className="combo">Combo ×{combo}</span>}
        <Hearts lives={lives} />
      </header>

      <main className="lesson-body">
        {stage === "intro" && (
          <div className="lesson-card">
            <div className="ex-kind">
              Unit {place + 1} of {peers.length}
            </div>
            <h1 className="display" style={{ fontSize: 40, marginBottom: 14 }}>
              {unit.title}
            </h1>
            <Markdown text={unit.intro} lang={lang} />
            <p className="note">
              {unit.exercises.length} exercises · {LIVES} lives · {XP_PER_EXERCISE} XP each, +1 while on a combo of {COMBO_FROM}+
            </p>
          </div>
        )}

        {stage === "ex" && ex && (
          <div className="lesson-card" key={`${idx}-${attempt}`}>
            <ExerciseView ex={ex} lang={lang} seed={`${unit.id}-${idx}`} locked={!!verdict && !verdict.error} checker={checker} setReady={setReady} />
          </div>
        )}

        {stage === "done" && summary && (
          <div className="lesson-card center">
            <div className="big-xp">+{summary.gain}</div>
            <h1 className="display" style={{ fontSize: 36 }}>
              {unit.title}: done
            </h1>
            {summary.levelUp && (
              <div className="levelup">
                Level {summary.levelUp}: {levelTitle(summary.levelUp)}
              </div>
            )}
            <ul className="lesson-summary">
              <li>
                Exercises <b>+{summary.total - UNIT_BONUS - (summary.perfect ? PERFECT_BONUS : 0)}</b>
              </li>
              <li>
                Unit complete <b>+{UNIT_BONUS}</b>
              </li>
              {summary.perfect && (
                <li>
                  No lives lost <b>+{PERFECT_BONUS}</b>
                </li>
              )}
              <li>
                Best combo <b>×{bestCombo}</b>
              </li>
            </ul>
            {summary.gain < summary.total && <p className="note">Replays only add XP when they beat your best run.</p>}
          </div>
        )}

        {stage === "out" && (
          <div className="lesson-card center">
            <h1 className="display" style={{ fontSize: 36 }}>
              Out of lives
            </h1>
            <p className="muted">That's how practice works. Read the unit intro again, then give it another go.</p>
          </div>
        )}
      </main>

      <footer className={`lesson-foot ${verdict ? (verdict.error ? "warn" : verdict.correct ? "good" : "bad") : ""}`}>
        <div className="lesson-foot-inner">
          {stage === "intro" && (
            <>
              <span className="muted small">{unit.exercises.length} exercises ahead</span>
              <button className="btn btn-gold btn-lg" onClick={() => setStage("ex")} autoFocus>
                Start
              </button>
            </>
          )}

          {stage === "ex" && !verdict && (
            <>
              <span className="muted small">
                {idx + 1} / {unit.exercises.length}
              </span>
              <span className="tip-host" title={runtimeBlocked ? runtimeTip : undefined}>
                <button className="btn btn-gold btn-lg" disabled={!ready || busy || runtimeBlocked} onClick={() => void check()}>
                  {busy ? "Checking…" : "Check"}
                </button>
              </span>
            </>
          )}

          {stage === "ex" && verdict && (
            <>
              <div className="feedback">
                <b>
                  {verdict.error
                    ? "Couldn't run that"
                    : verdict.correct
                      ? combo >= COMBO_FROM
                        ? `Correct! Combo ×${combo}`
                        : "Correct!"
                      : revealed
                        ? "Here's the answer"
                        : `Not quite. ${lives} ${lives === 1 ? "life" : "lives"} left, try once more.`}
                </b>
                {verdict.error ? (
                  <pre className="errblock">{verdict.error}</pre>
                ) : (
                  <>
                    {revealed && ex?.kind === "predict" && (
                      <div className="small">
                        Expected: <code>{ex.expected.trim().replace(/\n/g, " ⏎ ")}</code>
                      </div>
                    )}
                    {revealed && ex?.kind === "choice" && (
                      <div className="small">
                        Answer: <code>{ex.options[ex.answer]}</code>
                      </div>
                    )}
                    {revealed && ex?.kind === "blank" && (
                      <div className="small">
                        Blanks: {ex.blanks.map((b, i) => <code key={i} style={{ marginRight: 6 }}>{b[0]}</code>)}
                      </div>
                    )}
                    {revealed && (ex?.kind === "order" || ex?.kind === "fix" || ex?.kind === "write") && (
                      <pre className="errblock reveal">{ex.kind === "order" ? ex.lines.join("\n") : ex.solution}</pre>
                    )}
                    {!verdict.correct && !revealed && (ex?.kind === "fix" || ex?.kind === "write") && verdict.got !== undefined && (
                      <div className="small">
                        Your program printed: <code>{verdict.got.trim().slice(0, 200) || "(nothing)"}</code>
                      </div>
                    )}
                    {(verdict.correct || revealed) && (
                      <div className="why">
                        <Markdown text={ex?.why ?? ""} />
                      </div>
                    )}
                  </>
                )}
              </div>
              <button className="btn btn-lg btn-primary" onClick={advance} autoFocus>
                {verdict.correct && !verdict.error
                  ? idx + 1 < unit.exercises.length
                    ? "Continue"
                    : "Finish unit"
                  : lives <= 0 && !verdict.error
                    ? "See result"
                    : revealed
                      ? "Got it, continue"
                      : "Try again"}
              </button>
            </>
          )}

          {stage === "done" && (
            <>
              <button className="btn btn-lg" onClick={restart}>
                Replay
              </button>
              {next ? (
                <button className="btn btn-gold btn-lg" onClick={() => nav(`/basecamp/${next.id}`)} autoFocus>
                  Next: {next.title}
                </button>
              ) : unit.section === "oop" ? (
                <button className="btn btn-gold btn-lg" onClick={() => nav("/basecamp")} autoFocus>
                  Back to Basecamp
                </button>
              ) : (
                <button className="btn btn-gold btn-lg" onClick={() => nav("/")} autoFocus>
                  On to The Crossroads
                </button>
              )}
            </>
          )}

          {stage === "out" && (
            <>
              <Link to="/basecamp" className="btn btn-lg">
                Back to Basecamp
              </Link>
              <button className="btn btn-gold btn-lg" onClick={restart} autoFocus>
                Try the unit again
              </button>
            </>
          )}
        </div>
      </footer>
    </div>
  );
}
