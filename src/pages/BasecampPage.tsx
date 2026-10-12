import { Link } from "react-router-dom";
import { LANGS } from "../content";
import { useProgress } from "../lib/progress";
import { basecampDone, oopDone, PLACEMENT_PASS, unitsIn, type Unit } from "../lib/basecamp";
import type { UnitProgress } from "../lib/progress";
import { WorldGlyph } from "../components/WorldGlyph";
import { Topo } from "../components/Topo";

function UnitGrid({ units, progress, nextIdx }: { units: Unit[]; progress?: Record<string, UnitProgress>; nextIdx: number }) {
  return (
    <div className="unit-grid">
      {units.map((u, i) => {
        const p = progress?.[u.id];
        const isNext = i === nextIdx;
        return (
          <Link key={u.id} to={`/basecamp/${u.id}`} className={`card unit-card ${p?.done ? "done" : ""} ${isNext ? "next" : ""}`}>
            <span className="unit-num">{p?.done ? "✓" : i + 1}</span>
            <span className="unit-text">
              <b>{u.title}</b>
              <span className="small muted">
                {u.exercises.length} exercises
                {p?.done ? ` · ${p.xp} XP${p.perfect ? " · perfect" : ""}` : ""}
              </span>
            </span>
            {isNext && <span className="pill xp">Up next</span>}
          </Link>
        );
      })}
    </div>
  );
}

export function BasecampPage() {
  const state = useProgress();
  const lang = state.settings.lang;
  const label = LANGS.find((l) => l.id === lang)!.label;
  const core = unitsIn(lang, "core");
  const oop = unitsIn(lang, "oop");
  const bc = state.basecamp[lang];
  const st = basecampDone(lang, state);
  const oopSt = oopDone(lang, state);
  const nextCore = core.findIndex((u) => !bc?.units[u.id]?.done);
  const nextOop = oop.findIndex((u) => !bc?.units[u.id]?.done);
  const functionsDone = !!bc?.units[`${lang}-09`]?.done;

  return (
    <div style={{ ["--c" as string]: "#ffc24b" }}>
      <header className="world-hero">
        <Topo className="topo" seed={3} peaks={3} width={1400} height={320} />
        <div className="world-hero-inner">
          <div className="world-emblem">
            <WorldGlyph id={0} size={70} />
          </div>
          <div>
            <div className="crumbs">
              <Link to="/">Trail</Link> / Phase 0
            </div>
            <h1 className="display">Basecamp</h1>
            <p>
              {label} basics before the climb: output, variables, input, conditions, loops, arrays, functions and errors. Switch the
              language in the sidebar to learn another one.
            </p>
          </div>
          <div className="world-progress">
            <div className="big">
              {st.done}
              <small> / {st.total} units</small>
            </div>
            <div className="bar" style={{ margin: "10px 0 8px" }}>
              <span style={{ width: `${(st.placed ? 1 : st.done / st.total) * 100}%` }} />
            </div>
            <div className="small muted">{st.placed ? "Placement test passed" : `${label} track`}</div>
          </div>
        </div>
      </header>

      <div className="page" style={{ paddingTop: 26 }}>
        {!st.complete && (
          <div className="card placement">
            <div>
              <h3>Already know {label}?</h3>
              <p className="muted small" style={{ margin: "4px 0 0" }}>
                Take the 10-question placement test. Get {PLACEMENT_PASS} right and Basecamp counts as complete.
              </p>
            </div>
            <Link to="/basecamp/placement" className="btn">
              Take the placement test
            </Link>
          </div>
        )}

        <UnitGrid units={core} progress={bc?.units} nextIdx={nextCore} />

        <div className="section-title">
          <h2>Objects (OOP)</h2>
          <span className="small muted">
            {oopSt.done} / {oopSt.total} units
          </span>
        </div>
        <div className="bar" style={{ margin: "0 0 14px" }}>
          <span style={{ width: `${oopSt.total ? (oopSt.done / oopSt.total) * 100 : 0}%` }} />
        </div>
        {!functionsDone && (
          <p className="small muted" style={{ margin: "0 0 14px" }}>
            Recommended after Functions
          </p>
        )}
        <UnitGrid units={oop} progress={bc?.units} nextIdx={nextOop} />
      </div>
    </div>
  );
}
