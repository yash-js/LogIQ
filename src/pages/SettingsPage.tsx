import { useEffect, useState } from "react";
import { useProgress } from "../lib/progress";
import { checkToolchain, inTauri, type ToolchainStatus } from "../lib/runner";
import { dataInfo, exportBackup, importBackup, restoreDaily, revealData, type DataInfo } from "../lib/backup";

function Tool({ name, info }: { name: string; info?: { found: boolean; command: string | null; version: string | null } }) {
  return (
    <div className="tool-row">
      <span>{name}</span>
      {!info ? (
        <span className="muted">checking…</span>
      ) : info.found ? (
        <span className="ok">
          {info.version} <span className="muted">({info.command})</span>
        </span>
      ) : (
        <span className="no">{info.version ?? "Not found"}</span>
      )}
    </div>
  );
}

function YourData() {
  const [info, setInfo] = useState<DataInfo | null>(null);
  const [msg, setMsg] = useState<{ bad: boolean; text: string } | null>(null);
  const [busy, setBusy] = useState(false);
  const [daily, setDaily] = useState("");

  useEffect(() => {
    if (inTauri) void dataInfo().then((i) => {
      setInfo(i);
      setDaily(i.backups[0] ?? "");
    });
  }, []);

  async function act(f: () => Promise<string | null>) {
    setBusy(true);
    setMsg(null);
    try {
      const text = await f();
      if (text) setMsg({ bad: false, text });
      if (inTauri) setInfo(await dataInfo());
    } catch (e) {
      setMsg({ bad: true, text: e instanceof Error ? e.message : String(e) });
    } finally {
      setBusy(false);
    }
  }

  if (!inTauri) return <p className="muted">Open the desktop app to manage your data.</p>;

  return (
    <>
      <p className="muted" style={{ marginTop: 0 }}>
        Everything is stored on this computer in a local SQLite database. No account, nothing uploaded. A copy is saved
        automatically once a day (last 14 days kept).
      </p>
      {info && (
        <div className="tool-row" style={{ borderBottom: 0 }}>
          <span>Database</span>
          <span style={{ display: "flex", gap: 10, alignItems: "center", minWidth: 0 }}>
            <code style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", fontSize: 12.5 }}>{info.dbPath}</code>
            <button className="btn btn-sm" onClick={() => void revealData(info)}>
              Show in folder
            </button>
          </span>
        </div>
      )}

      <h3 style={{ margin: "18px 0 8px" }}>Backup file</h3>
      <p className="small muted" style={{ margin: "0 0 10px" }}>
        Export saves XP, solved problems, quiz results and your saved code to one .json file. Import it on another
        computer, or after reinstalling.
      </p>
      <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
        <button className="btn btn-primary" disabled={busy} onClick={() => act(async () => {
          const path = await exportBackup();
          return path ? `Backup saved to ${path}` : null;
        })}>
          Export backup
        </button>
        <button className="btn" disabled={busy} onClick={() => act(async () => {
          const r = await importBackup("merge");
          return r ? `Merged ${r.solved} solved problems from ${r.path}. Nothing on this computer was lost.` : null;
        })}>
          Import and merge
        </button>
        <button className="btn btn-ghost" disabled={busy} onClick={() => {
          if (!confirm("Replace all progress on this computer with the backup file?")) return;
          void act(async () => {
            const r = await importBackup("replace");
            return r ? `Progress replaced with ${r.path}.` : null;
          });
        }}>
          Import and replace
        </button>
      </div>

      {info && info.backups.length > 0 && (
        <>
          <h3 style={{ margin: "22px 0 8px" }}>Automatic daily copies</h3>
          <div style={{ display: "flex", gap: 10, alignItems: "end", flexWrap: "wrap" }}>
            <div className="field" style={{ minWidth: 260 }}>
              <label htmlFor="daily">Restore progress from</label>
              <select id="daily" className="input" value={daily} onChange={(e) => setDaily(e.target.value)}>
                {info.backups.map((b) => (
                  <option key={b} value={b}>
                    {b.replace(/^progress-|\.db$/g, "")}
                  </option>
                ))}
              </select>
            </div>
            <button className="btn" disabled={busy || !daily} onClick={() => {
              if (!confirm(`Replace current progress with the copy from ${daily.replace(/^progress-|\.db$/g, "")}?`)) return;
              void act(async () => {
                await restoreDaily(daily, "replace");
                return `Restored progress from ${daily.replace(/^progress-|\.db$/g, "")}.`;
              });
            }}>
              Restore
            </button>
          </div>
        </>
      )}
      {msg && <p className={`notice ${msg.bad ? "bad" : "good"}`} style={{ marginTop: 14 }}>{msg.text}</p>}
    </>
  );
}

export function SettingsPage() {
  const settings = useProgress((s) => s.settings);
  const setSettings = useProgress((s) => s.setSettings);
  const reset = useProgress((s) => s.reset);
  const [tools, setTools] = useState<ToolchainStatus | null>(null);
  const [py, setPy] = useState(settings.pythonCmd);
  const [jh, setJh] = useState(settings.javaHome);
  const [nc, setNc] = useState(settings.nodeCmd);

  async function detect(prefs = { pythonCmd: settings.pythonCmd, javaHome: settings.javaHome, nodeCmd: settings.nodeCmd }) {
    setTools(null);
    setTools(await checkToolchain(prefs));
  }

  useEffect(() => {
    void detect();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="page page-narrow settings">
      <h1>Settings</h1>

      <section className="card pad">
        <h2 style={{ marginBottom: 12 }}>Code runners</h2>
        <Tool name="Python" info={tools?.python} />
        <Tool name="java" info={tools?.java} />
        <Tool name="javac" info={tools?.javac} />
        <Tool name="Node.js" info={tools?.node} />
        {tools && (!tools.python.found || !tools.javac.found || !tools.node.found) && (
          <p className="notice warn" style={{ marginTop: 14, display: "block" }}>
            {!tools.javac.found && (
              <>
                Java needs a JDK 17 or newer (Temurin from adoptium.net works).{" "}
              </>
            )}
            {!tools.python.found && <>Python needs Python 3 from python.org; tick "Add python.exe to PATH" on Windows. </>}
            {!tools.node.found && <>JavaScript needs Node.js (the LTS version from nodejs.org). </>}
            You only need the language you plan to use.
            Restart LogIQ after installing, or point to it below.
          </p>
        )}
        <div style={{ display: "grid", gap: 12, marginTop: 16 }}>
          <div className="field">
            <label htmlFor="py">Python command or path (optional)</label>
            <input id="py" className="input" value={py} onChange={(e) => setPy(e.target.value)} placeholder="python3, py, or C:\Python312\python.exe" />
          </div>
          <div className="field">
            <label htmlFor="jh">JDK folder, JAVA_HOME (optional)</label>
            <input id="jh" className="input" value={jh} onChange={(e) => setJh(e.target.value)} placeholder="C:\Program Files\Eclipse Adoptium\jdk-21 or /usr/lib/jvm/java-21-openjdk" />
          </div>
          <div className="field">
            <label htmlFor="nc">Node.js command or path (optional)</label>
            <input id="nc" className="input" value={nc} onChange={(e) => setNc(e.target.value)} placeholder="node, or C:\Program Files\nodejs\node.exe" />
          </div>
          <div>
            <button
              className="btn"
              onClick={() => {
                setSettings({ pythonCmd: py.trim(), javaHome: jh.trim(), nodeCmd: nc.trim() });
                void detect({ pythonCmd: py.trim(), javaHome: jh.trim(), nodeCmd: nc.trim() });
              }}
            >
              Save and check again
            </button>
          </div>
        </div>
      </section>

      <section className="card pad">
        <h2 style={{ marginBottom: 12 }}>Editor</h2>
        <div className="field" style={{ maxWidth: 220 }}>
          <label htmlFor="fs">Font size</label>
          <select id="fs" className="input" value={settings.fontSize} onChange={(e) => setSettings({ fontSize: Number(e.target.value) })}>
            {[12, 13, 14, 15, 16, 18, 20].map((n) => (
              <option key={n} value={n}>
                {n}px
              </option>
            ))}
          </select>
        </div>
      </section>

      <section className="card pad">
        <h2 style={{ marginBottom: 12 }}>Your data</h2>
        <YourData />
      </section>

      <section className="card pad">
        <h2 style={{ marginBottom: 12 }}>Start over</h2>
        <p className="muted" style={{ marginTop: 0 }}>
          Clears XP, solved problems, quiz results and saved code on this computer. Export a backup first if you might want it back.
        </p>
        <button
          className="btn btn-danger"
          onClick={() => {
            if (confirm("Clear all progress on this computer?")) reset();
          }}
        >
          Clear progress
        </button>
      </section>
    </div>
  );
}
