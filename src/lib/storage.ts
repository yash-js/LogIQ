// Progress storage. In the desktop app it lives in SQLite (src-tauri/src/store.rs);
// in a plain browser preview it falls back to localStorage.

import { invoke } from "@tauri-apps/api/core";
import type { StateStorage } from "zustand/middleware";
import { inTauri } from "./runner";

let pending: string | null = null;
let timer: ReturnType<typeof setTimeout> | undefined;

async function flush() {
  clearTimeout(timer);
  if (pending === null) return;
  const value = pending;
  pending = null;
  try {
    await invoke("save_state", { value });
  } catch (e) {
    console.error("Saving progress failed", e);
  }
}

if (typeof window !== "undefined") {
  window.addEventListener("beforeunload", () => void flush());
  window.addEventListener("blur", () => void flush());
}

export const progressStorage: StateStorage = inTauri
  ? {
      async getItem(name) {
        const stored = await invoke<string | null>("load_state");
        if (stored) return stored;
        // One-time move from older versions that kept progress in localStorage.
        const legacy = localStorage.getItem(name);
        if (legacy) await invoke("save_state", { value: legacy });
        return legacy;
      },
      setItem(_name, value) {
        // Typing in the editor changes state on every keystroke; write at most every 400 ms.
        pending = value;
        clearTimeout(timer);
        timer = setTimeout(() => void flush(), 400);
      },
      removeItem() {
        pending = null;
      },
    }
  : localStorage;

export const flushProgress = flush;
