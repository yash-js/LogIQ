import { invoke } from "@tauri-apps/api/core";
import type { Lang, Problem, TestCase } from "../content";
import { outputsMatch } from "./checker";

export interface ToolchainPrefs {
  pythonCmd?: string;
  javaHome?: string;
}

interface RawRun {
  status: "ok" | "tle" | "re";
  stdout: string;
  stderr: string;
  timeMs: number;
  exitCode: number | null;
  truncated: boolean;
}

interface RawResponse {
  compileError: string | null;
  setupError: string | null;
  results: RawRun[];
}

export type Verdict = "accepted" | "wrong" | "tle" | "runtime";

export interface TestResult extends RawRun {
  verdict: Verdict;
  input: string;
  expected: string;
  hidden: boolean;
}

export interface JudgeResult {
  kind: "ok" | "compile" | "setup";
  message?: string;
  results: TestResult[];
  passed: number;
  total: number;
  allPassed: boolean;
}

export interface ToolInfo {
  found: boolean;
  command: string | null;
  version: string | null;
}

export interface ToolchainStatus {
  python: ToolInfo;
  java: ToolInfo;
  javac: ToolInfo;
}

export const inTauri = typeof window !== "undefined" && "__TAURI_INTERNALS__" in window;

export async function checkToolchain(prefs: ToolchainPrefs): Promise<ToolchainStatus> {
  if (!inTauri) {
    const none = { found: false, command: null, version: "Open the desktop app to run code" };
    return { python: none, java: none, javac: none };
  }
  return invoke<ToolchainStatus>("check_toolchain", { prefs });
}

async function runRaw(lang: Lang, code: string, inputs: string[], timeLimitMs: number, prefs: ToolchainPrefs) {
  if (!inTauri) {
    return {
      compileError: null,
      setupError: "Code runs on your machine through the LogicQuest desktop app. Start it with `npm run tauri dev`.",
      results: [],
    } satisfies RawResponse;
  }
  return invoke<RawResponse>("run_code", { req: { language: lang, code, inputs, timeLimitMs, prefs } });
}

/** Runs code against test cases and grades every result. */
export async function judge(
  problem: Problem,
  lang: Lang,
  code: string,
  tests: TestCase[],
  hiddenFrom: number,
  prefs: ToolchainPrefs,
): Promise<JudgeResult> {
  const raw = await runRaw(lang, code, tests.map((t) => t.input), problem.timeLimitMs, prefs);
  if (raw.setupError) return { kind: "setup", message: raw.setupError, results: [], passed: 0, total: tests.length, allPassed: false };
  if (raw.compileError)
    return { kind: "compile", message: raw.compileError, results: [], passed: 0, total: tests.length, allPassed: false };

  const results: TestResult[] = raw.results.map((r, i) => {
    const t = tests[i];
    let verdict: Verdict;
    if (r.status === "tle") verdict = "tle";
    else if (r.status === "re") verdict = "runtime";
    else verdict = outputsMatch(t.output, r.stdout, problem.strict) ? "accepted" : "wrong";
    return { ...r, verdict, input: t.input, expected: t.output, hidden: i >= hiddenFrom };
  });
  const passed = results.filter((r) => r.verdict === "accepted").length;
  return { kind: "ok", results, passed, total: tests.length, allPassed: passed === tests.length };
}

/** Runs code on one custom input without grading. */
export async function runCustom(lang: Lang, code: string, input: string, timeLimitMs: number, prefs: ToolchainPrefs) {
  const raw = await runRaw(lang, code, [input], timeLimitMs, prefs);
  return raw;
}
