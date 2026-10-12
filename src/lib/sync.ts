import { create } from "zustand";
import type { Session } from "@supabase/supabase-js";
import { supabase } from "./supabase";
import { mergeStates, snapshot, useProgress, type ProgressState } from "./progress";

type SyncStatus = "offline" | "syncing" | "synced" | "error";

interface SyncState {
  session: Session | null;
  status: SyncStatus;
  lastSynced?: string;
  error?: string;
}

export const useSync = create<SyncState>(() => ({ session: null, status: "offline" }));

let timer: ReturnType<typeof setTimeout> | undefined;
let applyingRemote = false;

async function pull(userId: string): Promise<ProgressState | null> {
  const { data, error } = await supabase!.from("user_progress").select("state").eq("user_id", userId).maybeSingle();
  if (error) throw error;
  return (data?.state as ProgressState) ?? null;
}

async function push(userId: string, state: ProgressState) {
  const { error } = await supabase!
    .from("user_progress")
    .upsert({ user_id: userId, state, updated_at: new Date().toISOString() });
  if (error) throw error;
}

export async function syncNow() {
  const session = useSync.getState().session;
  if (!supabase || !session) return;
  useSync.setState({ status: "syncing", error: undefined });
  try {
    const remote = await pull(session.user.id);
    const local = snapshot();
    const merged = remote ? mergeStates(local, remote) : local;
    applyingRemote = true;
    useProgress.getState().replaceAll(merged);
    applyingRemote = false;
    await push(session.user.id, merged);
    useSync.setState({ status: "synced", lastSynced: new Date().toISOString() });
  } catch (e) {
    applyingRemote = false;
    useSync.setState({ status: "error", error: e instanceof Error ? e.message : String(e) });
  }
}

export function initSync() {
  if (!supabase) return;
  supabase.auth.getSession().then(({ data }) => {
    useSync.setState({ session: data.session, status: data.session ? "syncing" : "offline" });
    if (data.session) void syncNow();
  });
  supabase.auth.onAuthStateChange((event, session) => {
    useSync.setState({ session, status: session ? useSync.getState().status : "offline" });
    if (event === "SIGNED_IN") void syncNow();
  });
  // Push local changes a few seconds after they happen.
  useProgress.subscribe((s, prev) => {
    if (applyingRemote || s.updatedAt === prev.updatedAt) return;
    const session = useSync.getState().session;
    if (!session) return;
    clearTimeout(timer);
    timer = setTimeout(async () => {
      try {
        await push(session.user.id, snapshot());
        useSync.setState({ status: "synced", lastSynced: new Date().toISOString() });
      } catch (e) {
        useSync.setState({ status: "error", error: e instanceof Error ? e.message : String(e) });
      }
    }, 3000);
  });
}
