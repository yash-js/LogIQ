//! Local code runner: compiles/executes the learner's Java, Python or JavaScript code
//! against a list of stdin inputs, with a per-test time limit and output cap.

use serde::{Deserialize, Serialize};
use std::path::{Path, PathBuf};
use std::process::Stdio;
use std::sync::Arc;
use std::time::{Duration, Instant, SystemTime, UNIX_EPOCH};
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::process::Command;
use tokio::sync::Semaphore;

const OUTPUT_CAP: u64 = 256 * 1024; // 256 KB per stream
const PARALLEL: usize = 4;

#[derive(Debug, Deserialize, Default, Clone)]
#[serde(rename_all = "camelCase")]
pub struct ToolchainPrefs {
    /// e.g. "python3", "C:\\Python312\\python.exe"
    pub python_cmd: Option<String>,
    /// JDK home; javac/java are taken from <home>/bin
    pub java_home: Option<String>,
    /// e.g. "node", "C:\\Program Files\\nodejs\\node.exe"
    pub node_cmd: Option<String>,
}

#[derive(Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct RunRequest {
    pub language: String, // "java" | "python" | "javascript"
    pub code: String,
    pub inputs: Vec<String>,
    pub time_limit_ms: Option<u64>,
    #[serde(default)]
    pub prefs: ToolchainPrefs,
}

#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct TestRun {
    /// "ok" | "tle" | "re"
    pub status: String,
    pub stdout: String,
    pub stderr: String,
    pub time_ms: u128,
    pub exit_code: Option<i32>,
    pub truncated: bool,
}

#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct RunResponse {
    pub compile_error: Option<String>,
    pub setup_error: Option<String>,
    pub results: Vec<TestRun>,
}

#[derive(Debug, Serialize, Clone)]
#[serde(rename_all = "camelCase")]
pub struct ToolInfo {
    pub found: bool,
    pub command: Option<String>,
    pub version: Option<String>,
}

#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct ToolchainStatus {
    pub python: ToolInfo,
    pub java: ToolInfo,
    pub javac: ToolInfo,
    pub node: ToolInfo,
}

fn base_command(program: &str) -> Command {
    let mut cmd = Command::new(program);
    #[cfg(windows)]
    {
        // CREATE_NO_WINDOW: don't flash a console window for every test run.
        cmd.creation_flags(0x0800_0000);
    }
    cmd.kill_on_drop(true);
    cmd
}

/// Runs `<program> <args>` and returns combined stdout+stderr if it exits successfully.
async fn probe(program: &str, args: &[&str]) -> Option<String> {
    let fut = base_command(program)
        .args(args)
        .stdin(Stdio::null())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .output();
    let out = tokio::time::timeout(Duration::from_secs(8), fut).await.ok()?.ok()?;
    if !out.status.success() {
        return None;
    }
    let mut s = String::from_utf8_lossy(&out.stdout).to_string();
    s.push_str(&String::from_utf8_lossy(&out.stderr));
    let line = s
        .lines()
        .find(|l| !l.trim().is_empty() && !l.contains("JAVA_TOOL_OPTIONS"))
        .unwrap_or("")
        .trim()
        .to_string();
    Some(line)
}

async fn find_python(prefs: &ToolchainPrefs) -> ToolInfo {
    let mut candidates: Vec<String> = Vec::new();
    if let Some(p) = prefs.python_cmd.as_ref().filter(|p| !p.trim().is_empty()) {
        candidates.push(p.trim().to_string());
    }
    if cfg!(windows) {
        candidates.extend(["python", "py", "python3"].map(String::from));
    } else {
        candidates.extend(["python3", "python"].map(String::from));
    }
    for c in candidates {
        // On Windows "python3" can be a Microsoft Store stub; require a real "Python 3" banner.
        if let Some(v) = probe(&c, &["--version"]).await {
            if v.starts_with("Python 3") {
                return ToolInfo { found: true, command: Some(c), version: Some(v) };
            }
        }
    }
    ToolInfo { found: false, command: None, version: None }
}

async fn find_node(prefs: &ToolchainPrefs) -> ToolInfo {
    let mut candidates: Vec<String> = Vec::new();
    if let Some(p) = prefs.node_cmd.as_ref().filter(|p| !p.trim().is_empty()) {
        candidates.push(p.trim().to_string());
    }
    candidates.extend(["node", "nodejs"].map(String::from));
    for c in candidates {
        if let Some(v) = probe(&c, &["--version"]).await {
            if v.starts_with('v') {
                return ToolInfo { found: true, command: Some(c), version: Some(format!("Node.js {v}")) };
            }
        }
    }
    ToolInfo { found: false, command: None, version: None }
}

fn jdk_tool(prefs: &ToolchainPrefs, tool: &str) -> Vec<String> {
    let exe = if cfg!(windows) { format!("{tool}.exe") } else { tool.to_string() };
    let mut out = Vec::new();
    if let Some(home) = prefs.java_home.as_ref().filter(|p| !p.trim().is_empty()) {
        out.push(Path::new(home.trim()).join("bin").join(&exe).to_string_lossy().to_string());
    }
    if let Ok(home) = std::env::var("JAVA_HOME") {
        out.push(Path::new(&home).join("bin").join(&exe).to_string_lossy().to_string());
    }
    out.push(tool.to_string());
    out
}

async fn find_jdk_tool(prefs: &ToolchainPrefs, tool: &str) -> ToolInfo {
    for c in jdk_tool(prefs, tool) {
        if let Some(v) = probe(&c, &["-version"]).await {
            return ToolInfo { found: true, command: Some(c), version: Some(v) };
        }
    }
    ToolInfo { found: false, command: None, version: None }
}

pub async fn check_toolchain(prefs: ToolchainPrefs) -> ToolchainStatus {
    let (python, java, javac, node) = tokio::join!(
        find_python(&prefs),
        find_jdk_tool(&prefs, "java"),
        find_jdk_tool(&prefs, "javac"),
        find_node(&prefs)
    );
    ToolchainStatus { python, java, javac, node }
}

fn work_dir() -> std::io::Result<PathBuf> {
    let nanos = SystemTime::now().duration_since(UNIX_EPOCH).map(|d| d.as_nanos()).unwrap_or(0);
    let dir = std::env::temp_dir()
        .join("logicquest")
        .join(format!("run-{}-{}", std::process::id(), nanos));
    std::fs::create_dir_all(&dir)?;
    Ok(dir)
}

/// Finds the public class name so the file can be named to match it.
fn java_class_name(code: &str) -> String {
    let bytes = code;
    let mut search = bytes;
    while let Some(idx) = search.find("public") {
        let rest = search[idx + 6..].trim_start();
        let rest = rest.strip_prefix("final").map(|r| r.trim_start()).unwrap_or(rest);
        if let Some(after) = rest.strip_prefix("class") {
            if after.starts_with(char::is_whitespace) {
                let name: String = after
                    .trim_start()
                    .chars()
                    .take_while(|c| c.is_alphanumeric() || *c == '_' || *c == '$')
                    .collect();
                if !name.is_empty() {
                    return name;
                }
            }
        }
        search = &search[idx + 6..];
    }
    "Main".to_string()
}

async fn read_capped<R: tokio::io::AsyncRead + Unpin>(r: Option<R>) -> (String, bool) {
    let Some(r) = r else { return (String::new(), false) };
    let mut buf = Vec::new();
    let mut limited = r.take(OUTPUT_CAP + 1);
    let _ = limited.read_to_end(&mut buf).await;
    let truncated = buf.len() as u64 > OUTPUT_CAP;
    buf.truncate(OUTPUT_CAP as usize);
    (String::from_utf8_lossy(&buf).replace("\r\n", "\n"), truncated)
}

async fn run_one(program: String, args: Vec<String>, cwd: PathBuf, input: String, limit: Duration) -> TestRun {
    let mut cmd = base_command(&program);
    cmd.args(&args)
        .current_dir(&cwd)
        .env("PYTHONIOENCODING", "utf-8")
        .env("PYTHONDONTWRITEBYTECODE", "1")
        .env_remove("JAVA_TOOL_OPTIONS")
        .env_remove("NODE_OPTIONS")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped());

    let start = Instant::now();
    let mut child = match cmd.spawn() {
        Ok(c) => c,
        Err(e) => {
            return TestRun {
                status: "re".into(),
                stdout: String::new(),
                stderr: format!("Could not start {program}: {e}"),
                time_ms: 0,
                exit_code: None,
                truncated: false,
            }
        }
    };

    let stdin = child.stdin.take();
    let feeder = tokio::spawn(async move {
        if let Some(mut s) = stdin {
            let _ = s.write_all(input.as_bytes()).await;
            let _ = s.shutdown().await;
        }
    });
    let out_task = tokio::spawn(read_capped(child.stdout.take()));
    let err_task = tokio::spawn(read_capped(child.stderr.take()));

    let waited = tokio::time::timeout(limit, child.wait()).await;
    let elapsed = start.elapsed().as_millis();
    let (status, exit_code) = match waited {
        Ok(Ok(st)) => (if st.success() { "ok" } else { "re" }, st.code()),
        Ok(Err(_)) => ("re", None),
        Err(_) => {
            let _ = child.kill().await;
            ("tle", None)
        }
    };
    feeder.abort();
    let (stdout, t1) = out_task.await.unwrap_or_default();
    let (stderr, t2) = err_task.await.unwrap_or_default();

    TestRun {
        status: status.into(),
        stdout,
        stderr,
        time_ms: elapsed,
        exit_code,
        truncated: t1 || t2,
    }
}

pub async fn run_code(req: RunRequest) -> RunResponse {
    let limit = Duration::from_millis(req.time_limit_ms.unwrap_or(3000).clamp(500, 20_000));
    let dir = match work_dir() {
        Ok(d) => d,
        Err(e) => {
            return RunResponse { compile_error: None, setup_error: Some(format!("Temp folder error: {e}")), results: vec![] }
        }
    };

    let (program, args): (String, Vec<String>) = match req.language.as_str() {
        "python" => {
            let py = find_python(&req.prefs).await;
            let Some(cmd) = py.command else {
                let _ = std::fs::remove_dir_all(&dir);
                return RunResponse {
                    compile_error: None,
                    setup_error: Some("Python 3 not found. Install it from python.org (tick \"Add to PATH\") or set the path in Settings.".into()),
                    results: vec![],
                };
            };
            if let Err(e) = std::fs::write(dir.join("main.py"), &req.code) {
                return RunResponse { compile_error: None, setup_error: Some(e.to_string()), results: vec![] };
            }
            let mut a = Vec::new();
            if cmd == "py" {
                a.push("-3".to_string());
            }
            a.push("main.py".to_string());
            (cmd, a)
        }
        "javascript" => {
            let node = find_node(&req.prefs).await;
            let Some(cmd) = node.command else {
                let _ = std::fs::remove_dir_all(&dir);
                return RunResponse {
                    compile_error: None,
                    setup_error: Some("Node.js not found. Install the LTS version from nodejs.org or set the path in Settings.".into()),
                    results: vec![],
                };
            };
            if let Err(e) = std::fs::write(dir.join("main.js"), &req.code) {
                return RunResponse { compile_error: None, setup_error: Some(e.to_string()), results: vec![] };
            }
            (cmd, vec!["--stack-size=65500".to_string(), "main.js".to_string()])
        }
        "java" => {
            let (javac, java) = tokio::join!(find_jdk_tool(&req.prefs, "javac"), find_jdk_tool(&req.prefs, "java"));
            let (Some(javac), Some(java)) = (javac.command, java.command) else {
                let _ = std::fs::remove_dir_all(&dir);
                return RunResponse {
                    compile_error: None,
                    setup_error: Some("JDK not found. Install JDK 17+ (e.g. Temurin from adoptium.net) or set JAVA_HOME in Settings.".into()),
                    results: vec![],
                };
            };
            let class = java_class_name(&req.code);
            let file = format!("{class}.java");
            if let Err(e) = std::fs::write(dir.join(&file), &req.code) {
                return RunResponse { compile_error: None, setup_error: Some(e.to_string()), results: vec![] };
            }
            let compile = base_command(&javac)
                .args(["-encoding", "UTF-8", "-nowarn", &file])
                .current_dir(&dir)
                .env_remove("JAVA_TOOL_OPTIONS")
                .stdin(Stdio::null())
                .stdout(Stdio::piped())
                .stderr(Stdio::piped())
                .output();
            match tokio::time::timeout(Duration::from_secs(30), compile).await {
                Ok(Ok(out)) if out.status.success() => {}
                Ok(Ok(out)) => {
                    let mut msg = String::from_utf8_lossy(&out.stderr).to_string();
                    msg.push_str(&String::from_utf8_lossy(&out.stdout));
                    let _ = std::fs::remove_dir_all(&dir);
                    return RunResponse { compile_error: Some(msg.replace("\r\n", "\n")), setup_error: None, results: vec![] };
                }
                Ok(Err(e)) => {
                    let _ = std::fs::remove_dir_all(&dir);
                    return RunResponse { compile_error: None, setup_error: Some(format!("javac failed to start: {e}")), results: vec![] };
                }
                Err(_) => {
                    let _ = std::fs::remove_dir_all(&dir);
                    return RunResponse { compile_error: Some("Compilation timed out.".into()), setup_error: None, results: vec![] };
                }
            }
            (
                java,
                vec![
                    "-Xss64m".into(),
                    "-XX:+UseSerialGC".into(),
                    "-XX:TieredStopAtLevel=1".into(),
                    "-Dfile.encoding=UTF-8".into(),
                    "-cp".into(),
                    ".".into(),
                    class,
                ],
            )
        }
        other => {
            let _ = std::fs::remove_dir_all(&dir);
            return RunResponse { compile_error: None, setup_error: Some(format!("Unsupported language: {other}")), results: vec![] };
        }
    };

    // Java start-up costs ~0.3–0.5 s, so give the JVM extra headroom.
    let limit = if req.language == "java" { limit + Duration::from_millis(1500) } else { limit };
    let sem = Arc::new(Semaphore::new(PARALLEL));
    let mut handles = Vec::new();
    for input in req.inputs {
        let sem = sem.clone();
        let (p, a, d) = (program.clone(), args.clone(), dir.clone());
        handles.push(tokio::spawn(async move {
            let _permit = sem.acquire_owned().await;
            run_one(p, a, d, input, limit).await
        }));
    }
    let mut results = Vec::new();
    for h in handles {
        results.push(h.await.unwrap_or(TestRun {
            status: "re".into(),
            stdout: String::new(),
            stderr: "Runner task failed".into(),
            time_ms: 0,
            exit_code: None,
            truncated: false,
        }));
    }
    let _ = std::fs::remove_dir_all(&dir);
    RunResponse { compile_error: None, setup_error: None, results }
}

#[cfg(test)]
mod tests {
    use super::*;

    /// The exact JSON shape src/lib/runner.ts sends and expects back.
    #[tokio::test]
    async fn frontend_contract() {
        let req: RunRequest = serde_json::from_str(
            r#"{"language":"python","code":"print(int(input())+1)","inputs":["1\n"],"timeLimitMs":2000,"prefs":{"pythonCmd":"","javaHome":""}}"#,
        )
        .unwrap();
        let res = serde_json::to_value(run_code(req).await).unwrap();
        assert!(res.get("compileError").is_some() && res.get("setupError").is_some());
        let r0 = &res["results"][0];
        for k in ["status", "stdout", "stderr", "timeMs", "exitCode", "truncated"] {
            assert!(r0.get(k).is_some(), "missing {k}");
        }
        assert_eq!(r0["stdout"].as_str().unwrap().trim(), "2");
        let st = serde_json::to_value(check_toolchain(serde_json::from_str(r#"{"pythonCmd":"","javaHome":""}"#).unwrap()).await).unwrap();
        assert_eq!(st["python"]["found"], true);
        assert_eq!(st["javac"]["found"], true);
        assert_eq!(st["node"]["found"], true);
    }

    #[tokio::test]
    async fn javascript_run() {
        let r = run_code(RunRequest {
            language: "javascript".into(),
            code: "const l=require('fs').readFileSync(0,'utf8').split('\\n');console.log(Number(l[0])*3)".into(),
            inputs: vec!["14\n".into()],
            time_limit_ms: Some(2000),
            prefs: Default::default(),
        })
        .await;
        assert!(r.setup_error.is_none(), "{:?}", r.setup_error);
        assert_eq!(r.results[0].stdout.trim(), "42");
    }

    #[test]
    fn class_name_detection() {
        assert_eq!(java_class_name("import java.util.*;\npublic class Solver {}"), "Solver");
        assert_eq!(java_class_name("public final class Main{}"), "Main");
        assert_eq!(java_class_name("class X {}"), "Main");
    }

    #[tokio::test]
    async fn python_echo_and_tle() {
        let r = run_code(RunRequest {
            language: "python".into(),
            code: "import sys\nn=int(input())\nif n<0:\n  while True: pass\nprint(n*2)".into(),
            inputs: vec!["21\n".into(), "-1\n".into()],
            time_limit_ms: Some(800),
            prefs: Default::default(),
        })
        .await;
        assert_eq!(r.results[0].status, "ok");
        assert_eq!(r.results[0].stdout.trim(), "42");
        assert_eq!(r.results[1].status, "tle");
    }

    #[tokio::test]
    async fn java_compile_and_run() {
        let r = run_code(RunRequest {
            language: "java".into(),
            code: "import java.util.*;\npublic class Main { public static void main(String[] a){ Scanner s=new Scanner(System.in); int n=s.nextInt(); System.out.println(n+1);} }".into(),
            inputs: vec!["41\n".into()],
            time_limit_ms: Some(2000),
            prefs: Default::default(),
        })
        .await;
        assert!(r.setup_error.is_none(), "{:?}", r.setup_error);
        assert!(r.compile_error.is_none(), "{:?}", r.compile_error);
        assert_eq!(r.results[0].stdout.trim(), "42");

        let bad = run_code(RunRequest {
            language: "java".into(),
            code: "public class Main { int x = }".into(),
            inputs: vec!["".into()],
            time_limit_ms: None,
            prefs: Default::default(),
        })
        .await;
        assert!(bad.compile_error.is_some());
    }
}
