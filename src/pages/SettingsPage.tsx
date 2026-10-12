import { useEffect, useState } from "react";
import { useProgress } from "../lib/progress";
import { checkToolchain, type ToolchainStatus } from "../lib/runner";
import { sendEmailCode, signInWithGithub, signOut, supabaseConfigured, verifyEmailCode } from "../lib/supabase";
import { syncNow, useSync } from "../lib/sync";

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

function Account() {
  const sync = useSync();
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [sent, setSent] = useState(false);
  const [msg, setMsg] = useState<{ bad: boolean; text: string } | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    const onErr = (e: Event) => setMsg({ bad: true, text: (e as CustomEvent<string>).detail });
    window.addEventListener("lq-auth-error", onErr);
    return () => window.removeEventListener("lq-auth-error", onErr);
  }, []);

  async function act(f: () => Promise<unknown>) {
    setBusy(true);
    setMsg(null);
    try {
      await f();
    } catch (e) {
      setMsg({ bad: true, text: e instanceof Error ? e.message : String(e) });
    } finally {
      setBusy(false);
    }
  }

  if (!supabaseConfigured) {
    return (
      <p className="muted">
        Sync is off. Add <code>VITE_SUPABASE_URL</code> and <code>VITE_SUPABASE_ANON_KEY</code> to <code>.env</code> and restart
        the app to sync progress between your computers. Everything still works offline.
      </p>
    );
  }

  if (sync.session) {
    return (
      <>
        <p>
          Signed in as <strong>{sync.session.user.email ?? sync.session.user.user_metadata?.user_name}</strong>.{" "}
          <span className="muted">
            {sync.status === "synced" && sync.lastSynced ? `Synced ${new Date(sync.lastSynced).toLocaleTimeString()}` : sync.status}
            {sync.error && `: ${sync.error}`}
          </span>
        </p>
        <div style={{ display: "flex", gap: 10 }}>
          <button className="btn" onClick={() => void syncNow()}>
            Sync now
          </button>
          <button className="btn btn-ghost" onClick={() => void signOut()}>
            Sign out
          </button>
        </div>
      </>
    );
  }

  return (
    <>
      <p className="muted" style={{ marginTop: 0 }}>
        Sign in to sync XP, progress and saved code between your Windows and Linux machines.
      </p>
      <button className="btn btn-primary" disabled={busy} onClick={() => act(signInWithGithub)}>
        Continue with GitHub
      </button>
      <p className="small muted">Your browser opens, then sends you back to LogicQuest.</p>
      <div style={{ display: "grid", gridTemplateColumns: "1fr auto", gap: 10, alignItems: "end", marginTop: 14 }}>
        <div className="field">
          <label htmlFor="email">Or get a 6-digit code by email</label>
          <input id="email" className="input" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" />
        </div>
        <button
          className="btn"
          disabled={busy || !email}
          onClick={() =>
            act(async () => {
              await sendEmailCode(email);
              setSent(true);
              setMsg({ bad: false, text: `Code sent to ${email}.` });
            })
          }
        >
          Send code
        </button>
        {sent && (
          <>
            <div className="field">
              <label htmlFor="otp">Code</label>
              <input id="otp" className="input" inputMode="numeric" value={code} onChange={(e) => setCode(e.target.value.trim())} />
            </div>
            <button className="btn btn-primary" disabled={busy || code.length < 6} onClick={() => act(() => verifyEmailCode(email, code))}>
              Sign in
            </button>
          </>
        )}
      </div>
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
            Restart LogicQuest after installing, or point to it below.
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
        <h2 style={{ marginBottom: 12 }}>Account and sync</h2>
        <Account />
      </section>

      <section className="card pad">
        <h2 style={{ marginBottom: 12 }}>Start over</h2>
        <p className="muted" style={{ marginTop: 0 }}>
          Clears XP, solved problems, quiz results and saved code on this computer. If you are signed in, the next sync will
          bring synced progress back.
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
