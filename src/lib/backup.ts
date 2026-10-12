import { invoke } from "@tauri-apps/api/core";
import { open, save } from "@tauri-apps/plugin-dialog";
import { revealItemInDir } from "@tauri-apps/plugin-opener";
import { dayKey } from "./game";
import { initialState, mergeStates, snapshot, useProgress, type ProgressState } from "./progress";
import { flushProgress } from "./storage";

export interface DataInfo {
  dataDir: string;
  dbPath: string;
  backups: string[];
}

interface BackupFile {
  app: "logicquest";
  format: 1;
  exportedAt: string;
  state: ProgressState;
}

export function dataInfo() {
  return invoke<DataInfo>("data_info");
}

export async function revealData(info: DataInfo) {
  await flushProgress();
  await revealItemInDir(info.dbPath);
}

/** Saves all progress (XP, solves, quiz results, saved code) to a JSON file. Returns the path, or null if cancelled. */
export async function exportBackup(): Promise<string | null> {
  await flushProgress();
  const path = await save({
    title: "Save LogicQuest backup",
    defaultPath: `logicquest-backup-${dayKey()}.json`,
    filters: [{ name: "LogicQuest backup", extensions: ["json"] }],
  });
  if (!path) return null;
  const file: BackupFile = { app: "logicquest", format: 1, exportedAt: new Date().toISOString(), state: snapshot() };
  await invoke("write_text_file", { path, contents: JSON.stringify(file, null, 1) });
  return path;
}

function parseBackup(text: string): ProgressState {
  let data: unknown;
  try {
    data = JSON.parse(text);
  } catch {
    throw new Error("That file isn't valid JSON.");
  }
  const d = data as Partial<BackupFile> & { state?: unknown };
  // Accept our export format and the raw persisted format ({ state, version }).
  const st = d.state as ProgressState | undefined;
  if (!st || typeof st !== "object" || typeof st.problems !== "object") {
    throw new Error("That file isn't a LogicQuest backup.");
  }
  return {
    ...initialState,
    ...st,
    settings: { ...initialState.settings, ...(st.settings ?? {}) },
  };
}

export type ImportMode = "merge" | "replace";

/** Loads a backup file. Merge keeps everything from both sides; replace overwrites this computer's progress. */
export async function importBackup(mode: ImportMode): Promise<{ path: string; solved: number } | null> {
  const path = await open({ title: "Open LogicQuest backup", multiple: false, directory: false, filters: [{ name: "LogicQuest backup", extensions: ["json"] }] });
  if (!path || Array.isArray(path)) return null;
  const text = await invoke<string>("read_text_file", { path });
  const incoming = parseBackup(text);
  apply(incoming, mode);
  return { path, solved: Object.values(incoming.problems).filter((p) => p.solvedAt).length };
}

/** Restores one of the automatic daily backups. */
export async function restoreDaily(name: string, mode: ImportMode) {
  const raw = await invoke<string | null>("read_backup", { name });
  if (!raw) throw new Error("That backup is empty.");
  apply(parseBackup(raw), mode);
}

function apply(incoming: ProgressState, mode: ImportMode) {
  const next = mode === "merge" ? mergeStates(snapshot(), incoming) : { ...incoming, updatedAt: new Date().toISOString() };
  useProgress.getState().replaceAll({ ...next, updatedAt: new Date().toISOString() });
  void flushProgress();
}
