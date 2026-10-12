import problemsJson from "./problems.json";
import phasesJson from "./phases.json";

export type Lang = "java" | "python" | "javascript";

export const LANGS: { id: Lang; label: string }[] = [
  { id: "java", label: "Java" },
  { id: "python", label: "Python" },
  { id: "javascript", label: "JavaScript" },
];

export interface TestCase {
  input: string;
  output: string;
}

export interface Problem {
  id: string;
  phase: number;
  title: string;
  difficulty: "easy" | "medium" | "stretch";
  xp: number;
  concepts: string[];
  statement: string;
  params: { name: string; type: string }[];
  returns: string;
  mode: "solve" | "print";
  strict: boolean;
  timeLimitMs: number;
  examples: TestCase[];
  tests: TestCase[];
  hints: Record<Lang, string[]>;
  practice: { label: string; url: string } | null;
  starter: Record<Lang, string>;
}

export interface QuizQuestion {
  q: string;
  options: string[];
  answer: number;
  why: string;
  /** Omitted questions are shown for every language. */
  lang?: Lang;
}

export interface Phase {
  id: number;
  title: string;
  world: string;
  tagline: string;
  color: string;
  quiz: QuizQuestion[];
}

export const problems = problemsJson as Problem[];
export const phases = phasesJson as Phase[];

const docModules = import.meta.glob("./docs/phase*.md", { query: "?raw", import: "default", eager: true }) as Record<
  string,
  string
>;

export function docFor(phase: number): string {
  return docModules[`./docs/phase${phase}.md`] ?? "";
}

export const problemById = new Map(problems.map((p) => [p.id, p]));

export function problemsInPhase(phase: number): Problem[] {
  return problems.filter((p) => p.phase === phase);
}

export function phaseById(id: number): Phase | undefined {
  return phases.find((p) => p.id === id);
}
