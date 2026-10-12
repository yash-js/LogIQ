import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { Lang } from "../content";
import { dayKey, streak } from "./game";

export interface ProblemProgress {
  attempts: number;
  hintsUsed: number;
  solvedAt?: string;
  xpEarned: number;
  solvedIn?: Lang[];
  code?: Partial<Record<Lang, string>>;
}

export interface DocProgress {
  read: boolean;
  quizPassed: boolean;
  bestScore: number;
}

export interface Settings {
  lang: Lang;
  pythonCmd: string;
  javaHome: string;
  fontSize: number;
}

export interface ProgressState {
  problems: Record<string, ProblemProgress>;
  docs: Record<number, DocProgress>;
  xp: number;
  activity: Record<string, number>;
  bestStreak: number;
  settings: Settings;
  updatedAt: string;
}

interface Actions {
  saveCode(id: string, lang: Lang, code: string): void;
  takeHint(id: string): void;
  recordAttempt(id: string): void;
  recordSolve(id: string, lang: Lang, xp: number): boolean;
  markDocRead(phase: number): void;
  recordQuiz(phase: number, score: number, passed: boolean): void;
  setSettings(s: Partial<Settings>): void;
  replaceAll(s: ProgressState): void;
  reset(): void;
}

export const initialState: ProgressState = {
  problems: {},
  docs: {},
  xp: 0,
  activity: {},
  bestStreak: 0,
  settings: { lang: "java", pythonCmd: "", javaHome: "", fontSize: 14 },
  updatedAt: new Date(0).toISOString(),
};

const now = () => new Date().toISOString();

function blank(): ProblemProgress {
  return { attempts: 0, hintsUsed: 0, xpEarned: 0 };
}

export const useProgress = create<ProgressState & Actions>()(
  persist(
    (set, get) => ({
      ...initialState,

      saveCode(id, lang, code) {
        const p = get().problems[id] ?? blank();
        set({ problems: { ...get().problems, [id]: { ...p, code: { ...p.code, [lang]: code } } } });
      },

      takeHint(id) {
        const p = get().problems[id] ?? blank();
        if (p.solvedAt) return; // reading hints after solving is free
        set({ problems: { ...get().problems, [id]: { ...p, hintsUsed: Math.min(3, p.hintsUsed + 1) } }, updatedAt: now() });
      },

      recordAttempt(id) {
        const p = get().problems[id] ?? blank();
        set({ problems: { ...get().problems, [id]: { ...p, attempts: p.attempts + 1 } }, updatedAt: now() });
      },

      /** Returns true if this is the first solve (XP awarded). */
      recordSolve(id, lang, xp) {
        const s = get();
        const p = s.problems[id] ?? blank();
        const solvedIn = Array.from(new Set([...(p.solvedIn ?? []), lang]));
        const first = !p.solvedAt;
        const today = dayKey();
        const activity = { ...s.activity, [today]: (s.activity[today] ?? 0) + 1 };
        set({
          problems: {
            ...s.problems,
            [id]: { ...p, solvedIn, solvedAt: p.solvedAt ?? now(), xpEarned: first ? xp : p.xpEarned },
          },
          xp: first ? s.xp + xp : s.xp,
          activity,
          bestStreak: Math.max(s.bestStreak, streak(activity)),
          updatedAt: now(),
        });
        return first;
      },

      markDocRead(phase) {
        const d = get().docs[phase] ?? { read: false, quizPassed: false, bestScore: 0 };
        if (d.read) return;
        set({ docs: { ...get().docs, [phase]: { ...d, read: true } }, updatedAt: now() });
      },

      recordQuiz(phase, score, passed) {
        const d = get().docs[phase] ?? { read: true, quizPassed: false, bestScore: 0 };
        set({
          docs: { ...get().docs, [phase]: { read: true, quizPassed: d.quizPassed || passed, bestScore: Math.max(d.bestScore, score) } },
          updatedAt: now(),
        });
      },

      setSettings(s) {
        set({ settings: { ...get().settings, ...s } });
      },

      replaceAll(s) {
        set({ ...s });
      },

      reset() {
        set({ ...initialState, settings: get().settings, updatedAt: now() });
      },
    }),
    { name: "logicquest-progress", version: 1 },
  ),
);

export function snapshot(): ProgressState {
  const s = useProgress.getState();
  return {
    problems: s.problems,
    docs: s.docs,
    xp: s.xp,
    activity: s.activity,
    bestStreak: s.bestStreak,
    settings: s.settings,
    updatedAt: s.updatedAt,
  };
}

/** Merge two devices' progress without losing work on either side. */
export function mergeStates(a: ProgressState, b: ProgressState): ProgressState {
  const problems: Record<string, ProblemProgress> = { ...a.problems };
  for (const [id, pb] of Object.entries(b.problems)) {
    const pa = problems[id];
    if (!pa) {
      problems[id] = pb;
      continue;
    }
    const firstSolve = [pa.solvedAt, pb.solvedAt].filter(Boolean).sort()[0];
    const solvedFrom = firstSolve === pa.solvedAt ? pa : pb;
    problems[id] = {
      attempts: Math.max(pa.attempts, pb.attempts),
      hintsUsed: firstSolve ? solvedFrom.hintsUsed : Math.max(pa.hintsUsed, pb.hintsUsed),
      solvedAt: firstSolve,
      xpEarned: firstSolve ? solvedFrom.xpEarned : 0,
      solvedIn: Array.from(new Set([...(pa.solvedIn ?? []), ...(pb.solvedIn ?? [])])),
      code: a.updatedAt >= b.updatedAt ? { ...pb.code, ...pa.code } : { ...pa.code, ...pb.code },
    };
  }
  const docs: Record<number, DocProgress> = { ...a.docs };
  for (const [k, db] of Object.entries(b.docs)) {
    const da = docs[Number(k)];
    docs[Number(k)] = da
      ? { read: da.read || db.read, quizPassed: da.quizPassed || db.quizPassed, bestScore: Math.max(da.bestScore, db.bestScore) }
      : db;
  }
  const activity: Record<string, number> = { ...a.activity };
  for (const [d, n] of Object.entries(b.activity)) activity[d] = Math.max(activity[d] ?? 0, n);
  const xp = Object.values(problems).reduce((s, p) => s + (p.xpEarned || 0), 0);
  return {
    problems,
    docs,
    xp,
    activity,
    bestStreak: Math.max(a.bestStreak, b.bestStreak, streak(activity)),
    settings: a.updatedAt >= b.updatedAt ? a.settings : b.settings,
    updatedAt: a.updatedAt > b.updatedAt ? a.updatedAt : b.updatedAt,
  };
}
