import { useEffect, useMemo, useRef, useSyncExternalStore } from "react";
import type { Lang } from "../content";
import { useProgress } from "./progress";
import { checkToolchain, inTauri, type ToolchainPrefs, type ToolchainStatus } from "./runner";

export const INSTALL_URL: Record<Lang, string> = {
  java: "https://adoptium.net/temurin/releases/",
  python: "https://www.python.org/downloads/",
  javascript: "https://nodejs.org/en/download",
};

/** True when this language's compiler or interpreter was not found. */
export function runtimeMissing(lang: Lang, status: ToolchainStatus | null): boolean {
  if (!status) return false;
  if (lang === "java") return !status.java.found || !status.javac.found;
  if (lang === "python") return !status.python.found;
  return !status.node.found;
}

interface Snap {
  status: ToolchainStatus | null;
  /** Languages whose banner was closed during this app session. */
  dismissed: Partial<Record<Lang, true>>;
}

let snap: Snap = { status: null, dismissed: {} };
const listeners = new Set<() => void>();
let activePrefs: ToolchainPrefs = {};
let loadedKey = "";
let pending: Promise<void> | null = null;
let pendingKey = "";
let generation = 0;
let focusBound = false;

function emit() {
  for (const listener of listeners) listener();
}

function prefsKey(prefs: ToolchainPrefs) {
  return `${prefs.pythonCmd ?? ""}\0${prefs.javaHome ?? ""}\0${prefs.nodeCmd ?? ""}`;
}

function subscribe(listener: () => void) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

function getSnap() {
  return snap;
}

/** Runs the toolchain check. Concurrent calls for the same settings share one request. */
export function refreshToolchain(prefs: ToolchainPrefs, force = false): Promise<void> {
  const key = prefsKey(prefs);
  if (pending && pendingKey === key) return pending;
  if (!force && loadedKey === key && snap.status) return Promise.resolve();
  const ticket = ++generation;
  pendingKey = key;
  pending = checkToolchain(prefs)
    .then((status) => {
      if (ticket !== generation) return;
      loadedKey = key;
      snap = { ...snap, status };
    })
    .catch(() => {
      /* keep the last result; a failed probe should not hide a real warning */
    })
    .finally(() => {
      if (ticket !== generation) return;
      pending = null;
      emit();
    });
  return pending;
}

export function dismissRuntimeBanner(lang: Lang) {
  if (snap.dismissed[lang]) return;
  snap = { ...snap, dismissed: { ...snap.dismissed, [lang]: true } };
  emit();
}

function bindFocus() {
  if (focusBound || typeof window === "undefined") return;
  focusBound = true;
  window.addEventListener("focus", () => {
    void refreshToolchain(activePrefs, true);
  });
}

/** Shared toolchain status. Pages read the cache instead of each calling the checker. */
export function useToolchain() {
  const pythonCmd = useProgress((s) => s.settings.pythonCmd);
  const javaHome = useProgress((s) => s.settings.javaHome);
  const nodeCmd = useProgress((s) => s.settings.nodeCmd);
  const lang = useProgress((s) => s.settings.lang);
  const prefs = useMemo(() => ({ pythonCmd, javaHome, nodeCmd }), [pythonCmd, javaHome, nodeCmd]);
  const state = useSyncExternalStore(subscribe, getSnap, getSnap);
  const seenLang = useRef(lang);

  useEffect(() => {
    if (!inTauri) return;
    bindFocus();
    activePrefs = prefs;
    const langChanged = seenLang.current !== lang;
    seenLang.current = lang;
    void refreshToolchain(prefs, langChanged);
  }, [prefs, lang]);

  return {
    status: state.status,
    dismissed: !!state.dismissed[lang],
    missing(language: Lang) {
      return inTauri && runtimeMissing(language, state.status);
    },
    recheck: () => refreshToolchain(prefs, true),
    dismiss: () => dismissRuntimeBanner(lang),
  };
}
