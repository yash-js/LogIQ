import { phases, problems, problemsInPhase, type Problem } from "../content";
import type { ProgressState } from "./progress";
import { basecampDone } from "./basecamp";

/** Share of a phase's problems that must be solved before the next world opens. */
export const UNLOCK_SHARE = 0.6;
export const HINT_PENALTY = 0.25;
export const CLEAN_SOLVE_BONUS = 5;
export const QUEST_MULTIPLIER = 2;
/** Extra XP for a solution that uses no library shortcuts (share of base XP). */
export const PURE_SHARE = 0.5;

export function pureBonus(problem: Problem) {
  return Math.round(problem.xp * PURE_SHARE);
}

export function levelFromXp(xp: number) {
  // Level n starts at 50·n·(n−1) XP: 0, 100, 300, 600, 1000, …
  let level = 1;
  while (50 * (level + 1) * level <= xp) level++;
  const start = 50 * level * (level - 1);
  const next = 50 * (level + 1) * level;
  return { level, into: xp - start, span: next - start };
}

export const LEVEL_TITLES = [
  "Newcomer", "Tinkerer", "Looper", "Pattern Seeker", "Recursion Diver",
  "Array Wrangler", "String Bender", "Problem Solver", "Logic Smith", "DSA Ready",
];

export function levelTitle(level: number) {
  return LEVEL_TITLES[Math.min(level, LEVEL_TITLES.length) - 1];
}

export function xpFor(problem: Problem, hintsUsed: number, cleanSolve: boolean, isQuest: boolean) {
  const share = Math.max(0.25, 1 - HINT_PENALTY * hintsUsed);
  let xp = Math.round(problem.xp * share);
  if (cleanSolve) xp += CLEAN_SOLVE_BONUS;
  if (isQuest) xp *= QUEST_MULTIPLIER;
  return xp;
}

export function solvedCount(state: ProgressState, phase: number) {
  return problemsInPhase(phase).filter((p) => state.problems[p.id]?.solvedAt).length;
}

export function isPhaseOpen(state: ProgressState, phase: number): boolean {
  if (phase === 1) return true;
  const prev = problemsInPhase(phase - 1);
  return solvedCount(state, phase - 1) >= Math.ceil(prev.length * UNLOCK_SHARE);
}

export function needToOpen(state: ProgressState, phase: number): number {
  if (phase === 1) return 0;
  const prev = problemsInPhase(phase - 1);
  return Math.max(0, Math.ceil(prev.length * UNLOCK_SHARE) - solvedCount(state, phase - 1));
}

/** Problems unlock once the phase's study quiz is passed. */
export function areProblemsOpen(state: ProgressState, phase: number): boolean {
  return isPhaseOpen(state, phase) && !!state.docs[phase]?.quizPassed;
}

export function dayKey(d = new Date()) {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}

export function streak(activity: Record<string, number>): number {
  let count = 0;
  const d = new Date();
  // Today not done yet doesn't break the streak.
  if (!activity[dayKey(d)]) d.setDate(d.getDate() - 1);
  while (activity[dayKey(d)]) {
    count++;
    d.setDate(d.getDate() - 1);
  }
  return count;
}

function hash(s: string) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619);
  return h >>> 0;
}

/** Today's quest: a stable pick among open, unsolved problems. Worth double XP. */
export function dailyQuest(state: ProgressState): Problem | null {
  const pool = problems.filter((p) => areProblemsOpen(state, p.phase) && !state.problems[p.id]?.solvedAt);
  if (!pool.length) return null;
  return pool[hash(dayKey()) % pool.length];
}

export interface Badge {
  id: string;
  name: string;
  detail: string;
  earned: boolean;
}

export function badges(state: ProgressState): Badge[] {
  const solved = Object.values(state.problems).filter((p) => p.solvedAt);
  const noHint = solved.filter((p) => p.hintsUsed === 0).length;
  const bothLangs = solved.filter((p) => (p.solvedIn ?? []).length >= 2).length;
  const triLang = solved.filter((p) => (p.solvedIn ?? []).length >= 3).length;
  const pure = solved.filter((p) => p.pure).length;
  const best = state.bestStreak;
  const list: Badge[] = phases.map((ph) => ({
    id: `phase-${ph.id}`,
    name: ph.world,
    detail: `Solve every problem in Phase ${ph.id}`,
    earned: solvedCount(state, ph.id) === problemsInPhase(ph.id).length,
  }));
  list.push(
    { id: "first", name: "First Light", detail: "Solve your first problem", earned: solved.length >= 1 },
    {
      id: "basecamp",
      name: "Basecamp Graduate",
      detail: "Finish Basecamp (or its placement test) in any language",
      earned: (["java", "python", "javascript"] as const).some((l) => basecampDone(l, state).complete),
    },
    { id: "nohint10", name: "Unassisted", detail: "Solve 10 problems without hints", earned: noHint >= 10 },
    { id: "nohint50", name: "Lone Wolf", detail: "Solve 50 problems without hints", earned: noHint >= 50 },
    { id: "purist", name: "Purist", detail: "Finish 10 Pure challenges (no library shortcuts)", earned: pure >= 10 },
    { id: "purist50", name: "From Scratch", detail: "Finish 50 Pure challenges", earned: pure >= 50 },
    { id: "bilingual", name: "Bilingual", detail: "Solve 10 problems in two languages", earned: bothLangs >= 10 },
    { id: "polyglot", name: "Polyglot", detail: "Solve 5 problems in Java, Python and JavaScript", earned: triLang >= 5 },
    { id: "streak7", name: "Week Warrior", detail: "Reach a 7-day streak", earned: best >= 7 },
    { id: "streak30", name: "Habit Formed", detail: "Reach a 30-day streak", earned: best >= 30 },
  );
  return list;
}
