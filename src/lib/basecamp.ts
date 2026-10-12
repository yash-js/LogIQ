import basecampJson from "../content/basecamp.json";
import type { Lang } from "../content";
import { outputsMatch } from "./checker";
import { runCustom, type ToolchainPrefs } from "./runner";

interface Base {
  prompt: string;
  why: string;
  code?: string | null;
  full?: boolean;
}

export type Exercise =
  | (Base & { kind: "choice"; options: string[]; answer: number })
  | (Base & { kind: "predict"; code: string; expected: string; stdin: string })
  | (Base & { kind: "blank"; code: string; blanks: string[][]; expected: string; stdin: string })
  | (Base & { kind: "order"; lines: string[]; expected: string; stdin: string })
  | (Base & { kind: "fix"; code: string; solution: string; expected: string; stdin: string })
  | (Base & { kind: "write"; code: string; solution: string; tests: { input: string; output: string }[] });

export interface Unit {
  id: string;
  title: string;
  intro: string;
  exercises: Exercise[];
}

export const basecamp = basecampJson as unknown as Record<Lang, Unit[]>;

export function unitsFor(lang: Lang): Unit[] {
  return basecamp[lang] ?? [];
}

export function findUnit(id: string): { lang: Lang; unit: Unit; index: number } | null {
  for (const lang of Object.keys(basecamp) as Lang[]) {
    const index = basecamp[lang].findIndex((u) => u.id === id);
    if (index >= 0) return { lang, unit: basecamp[lang][index], index };
  }
  return null;
}

export const XP_PER_EXERCISE = 2;
export const UNIT_BONUS = 10;
export const PERFECT_BONUS = 5;
export const COMBO_FROM = 3;
export const LIVES = 3;
export const PLACEMENT_PASS = 8;
export const PLACEMENT_XP = 60;

/** Keep in sync with java_wrap() in content/build_basecamp.py. */
export function wrapJava(code: string): string {
  const body = code
    .split("\n")
    .map((l) => (l.trim() ? "        " + l : ""))
    .join("\n");
  return `import java.util.*;\nimport java.io.*;\n\npublic class Main {\n    public static void main(String[] args) throws Exception {\n${body}\n    }\n}\n`;
}

export function runnable(lang: Lang, code: string, full?: boolean) {
  return lang === "java" && !full ? wrapJava(code) : code;
}

const norm = (s: string) => s.replace(/\s+/g, "").replace(/'/g, '"');

export function blankCorrect(answers: string[], blanks: string[][]) {
  return blanks.map((alts, i) => alts.some((a) => norm(a) === norm(answers[i] ?? "")));
}

export function predictCorrect(expected: string, answer: string) {
  return outputsMatch(expected, answer, false);
}

/** Stable shuffle that never returns the original order (for 2+ distinct items). */
export function shuffled<T>(items: T[], seed: string): T[] {
  let h = 2166136261;
  for (let i = 0; i < seed.length; i++) h = Math.imul(h ^ seed.charCodeAt(i), 16777619);
  const rnd = () => {
    h = Math.imul(h ^ (h >>> 15), 2246822507);
    h = Math.imul(h ^ (h >>> 13), 3266489909);
    return ((h ^= h >>> 16) >>> 0) / 2 ** 32;
  };
  const out = [...items];
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(rnd() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  if (out.length > 1 && out.every((x, i) => x === items[i])) [out[0], out[1]] = [out[1], out[0]];
  return out;
}

export interface RunCheck {
  ok: boolean;
  /** Set when the code couldn't run at all (missing runtime, compile error). Doesn't cost a life. */
  error?: string;
  got?: string;
}

/** Runs code against one or more stdin/expected pairs. */
export async function runAndCompare(
  lang: Lang,
  code: string,
  full: boolean | undefined,
  cases: { input: string; output: string }[],
  prefs: ToolchainPrefs,
): Promise<RunCheck> {
  for (const c of cases) {
    const raw = await runCustom(lang, runnable(lang, code, full), c.input, 5000, prefs);
    if (raw.setupError) return { ok: false, error: raw.setupError };
    if (raw.compileError) return { ok: false, error: raw.compileError };
    const r = raw.results[0];
    if (r.status === "tle") return { ok: false, got: "Time limit exceeded: a loop never ended?" };
    if (r.status !== "ok") return { ok: false, got: (r.stdout + "\n" + r.stderr).trim() };
    if (!outputsMatch(c.output, r.stdout, false)) return { ok: false, got: r.stdout };
  }
  return { ok: true };
}

/** Placement test: one question per unit, taken from its choice/predict exercises. */
export function placementQuestions(lang: Lang): { unit: string; ex: Exercise }[] {
  return unitsFor(lang).map((u) => {
    const pool = u.exercises.filter((e) => e.kind === "predict" || e.kind === "choice");
    const pick = pool.find((e) => e.kind === "predict") ?? pool[0];
    return { unit: u.title, ex: pick };
  });
}

export function basecampDone(lang: Lang, state: { basecamp: Partial<Record<Lang, { units: Record<string, { done: boolean }>; placed?: boolean }>> }) {
  const bc = state.basecamp[lang];
  if (!bc) return { done: 0, total: unitsFor(lang).length, complete: false, placed: false };
  const done = unitsFor(lang).filter((u) => bc.units[u.id]?.done).length;
  return { done, total: unitsFor(lang).length, complete: !!bc.placed || done === unitsFor(lang).length, placed: !!bc.placed };
}

