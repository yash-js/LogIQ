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

export interface UnitProgress {
  done: boolean;
  perfect: boolean;
  xp: number;
}

export interface BasecampProgress {
  units: Record<string, UnitProgress>;
  /** Passed the placement test, so Basecamp counts as complete. */
  placed?: boolean;
  placementXp?: number;
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
  basecamp: Partial<Record<Lang, BasecampProgress>>;
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
  recordUnit(lang: Lang, unitId: string, xp: number, perfect: boolean): number;
  recordPlacement(lang: Lang, xp: number): number;
  setSettings(s: Partial<Settings>): void;
  replaceAll(s: ProgressState): void;
  reset(): void;
}

export const initialState: ProgressState = {
  problems: {},
  docs: {},
  basecamp: {},
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

      /** Stores a finished Basecamp unit. Returns the XP actually added (best run counts). */
      recordUnit(lang, unitId, xp, perfect) {
        const s = get();
        const bc = s.basecamp[lang] ?? { units: {} };
        const prev = bc.units[unitId];
        const gain = Math.max(0, xp - (prev?.xp ?? 0));
        const today = dayKey();
        const activity = { ...s.activity, [today]: (s.activity[today] ?? 0) + 1 };
        set({
          basecamp: {
            ...s.basecamp,
            [lang]: { ...bc, units: { ...bc.units, [unitId]: { done: true, perfect: !!prev?.perfect || perfect, xp: Math.max(prev?.xp ?? 0, xp) } } },
          },
          xp: s.xp + gain,
          activity,
          bestStreak: Math.max(s.bestStreak, streak(activity)),
          updatedAt: now(),
        });
        return gain;
      },

      recordPlacement(lang, xp) {
        const s = get();
        const bc = s.basecamp[lang] ?? { units: {} };
        if (bc.placed) return 0;
        set({ basecamp: { ...s.basecamp, [lang]: { ...bc, placed: true, placementXp: xp } }, xp: s.xp + xp, updatedAt: now() });
        return xp;
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
      version: 3,
      storage: createJSONStorage(() => progressStorage),
      migrate: (old) => {
        const st = old as ProgressState;
        return { ...st, basecamp: st.basecamp ?? {}, settings: { ...initialState.settings, ...st.settings } } as ProgressState & Actions;
      },
    },
  ),
);

export function snapshot(): ProgressState {
  const s = useProgress.getState();
  return {
    problems: s.problems,
    docs: s.docs,
    basecamp: s.basecamp,
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
  const basecamp: Partial<Record<Lang, BasecampProgress>> = {};
  for (const l of ["java", "python", "javascript"] as Lang[]) {
    const ba = a.basecamp?.[l];
    const bb = b.basecamp?.[l];
    if (!ba && !bb) continue;
    const units: Record<string, UnitProgress> = { ...(ba?.units ?? {}) };
    for (const [uid, ub] of Object.entries(bb?.units ?? {})) {
      const ua = units[uid];
      units[uid] = ua ? { done: ua.done || ub.done, perfect: ua.perfect || ub.perfect, xp: Math.max(ua.xp, ub.xp) } : ub;
    }
    basecamp[l] = {
      units,
      placed: !!(ba?.placed || bb?.placed),
      placementXp: Math.max(ba?.placementXp ?? 0, bb?.placementXp ?? 0),
    };
  }
  const activity: Record<string, number> = { ...a.activity };
  for (const [d, n] of Object.entries(b.activity)) activity[d] = Math.max(activity[d] ?? 0, n);
  const xp =
    Object.values(problems).reduce((s, p) => s + (p.xpEarned || 0), 0) +
    Object.values(basecamp).reduce(
      (s, bc) => s + (bc?.placementXp ?? 0) + Object.values(bc?.units ?? {}).reduce((t, u) => t + u.xp, 0),
      0,
    );
  return {
    problems,
    docs,
    basecamp,
    xp,
    activity,
    bestStreak: Math.max(a.bestStreak, b.bestStreak, streak(activity)),
    lastOpened: a.lastOpened ?? b.lastOpened,
    settings: { ...initialState.settings, ...(a.updatedAt >= b.updatedAt ? a.settings : b.settings) },
    updatedAt: a.updatedAt > b.updatedAt ? a.updatedAt : b.updatedAt,
  };
}
