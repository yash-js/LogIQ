import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";
import { progressStorage } from "./storage";
import type { Lang } from "../content";
import { dayKey, streak } from "./game";

export interface ProblemProgress {
  attempts: number;
  hintsUsed: number;
  solvedAt?: string;
  xpEarned: number;
  solvedIn?: Lang[];
  /** Solved at least once without library shortcuts. */
  pure?: boolean;
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
  nodeCmd: string;
  fontSize: number;
}

export interface ProgressState {
  problems: Record<string, ProblemProgress>;
  docs: Record<number, DocProgress>;
  xp: number;
  activity: Record<string, number>;
  bestStreak: number;
  lastOpened?: string;
  settings: Settings;
  updatedAt: string;
}

interface Actions {
  saveCode(id: string, lang: Lang, code: string): void;
  takeHint(id: string): void;
  recordAttempt(id: string): void;
  recordSolve(id: string, lang: Lang, xp: number, pure: boolean): boolean;
  recordPure(id: string, bonus: number): void;
  setLastOpened(id: string): void;
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
  settings: { lang: "java", pythonCmd: "", javaHome: "", nodeCmd: "", fontSize: 14 },
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
      recordPure(id, bonus) {
        const s = get();
        const p = s.problems[id];
        if (!p?.solvedAt || p.pure) return;
        set({
          problems: { ...s.problems, [id]: { ...p, pure: true, xpEarned: p.xpEarned + bonus } },
          xp: s.xp + bonus,
          updatedAt: now(),
        });
      },

      setLastOpened(id) {
        if (get().lastOpened !== id) set({ lastOpened: id });
      },

      recordSolve(id, lang, xp, pure) {
        const s = get();
        const p = s.problems[id] ?? blank();
        const solvedIn = Array.from(new Set([...(p.solvedIn ?? []), lang]));
        const first = !p.solvedAt;
        const today = dayKey();
        const activity = { ...s.activity, [today]: (s.activity[today] ?? 0) + 1 };
        set({
          problems: {
            ...s.problems,
            [id]: { ...p, solvedIn, pure: p.pure || (first && pure), solvedAt: p.solvedAt ?? now(), xpEarned: first ? xp : p.xpEarned },
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
    {
      name: "logicquest-progress",
      version: 2,
      storage: createJSONStorage(() => progressStorage),
      migrate: (old) => {
        const st = old as ProgressState;
        return { ...st, settings: { ...initialState.settings, ...st.settings } } as ProgressState & Actions;
      },
    },
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
    lastOpened: s.lastOpened,
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
      xpEarned: firstSolve ? Math.max(pa.xpEarned || 0, pb.xpEarned || 0, solvedFrom.xpEarned || 0) : 0,
      pure: !!(pa.pure || pb.pure),
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
    lastOpened: a.lastOpened ?? b.lastOpened,
    settings: { ...initialState.settings, ...(a.updatedAt >= b.updatedAt ? a.settings : b.settings) },
    updatedAt: a.updatedAt > b.updatedAt ? a.updatedAt : b.updatedAt,
  };
}
