import { createClient, type Session, type SupabaseClient } from "@supabase/supabase-js";
import { listen } from "@tauri-apps/api/event";
import { getCurrent, onOpenUrl } from "@tauri-apps/plugin-deep-link";
import { openUrl } from "@tauri-apps/plugin-opener";
import { inTauri } from "./runner";

const url = import.meta.env.VITE_SUPABASE_URL as string | undefined;
const key = import.meta.env.VITE_SUPABASE_ANON_KEY as string | undefined;

export const supabaseConfigured = !!(url && key);

export const supabase: SupabaseClient | null = supabaseConfigured
  ? createClient(url!, key!, {
      auth: { flowType: "pkce", detectSessionInUrl: false, persistSession: true, autoRefreshToken: true },
    })
  : null;

export const REDIRECT_URL = "logicquest://auth-callback";

export async function signInWithGithub() {
  if (!supabase) throw new Error("Supabase is not configured.");
  const { data, error } = await supabase.auth.signInWithOAuth({
    provider: "github",
    options: { redirectTo: REDIRECT_URL, skipBrowserRedirect: true },
  });
  if (error) throw error;
  if (inTauri) await openUrl(data.url);
  else window.location.href = data.url;
}

export async function sendEmailCode(email: string) {
  if (!supabase) throw new Error("Supabase is not configured.");
  const { error } = await supabase.auth.signInWithOtp({ email, options: { shouldCreateUser: true } });
  if (error) throw error;
}

export async function verifyEmailCode(email: string, token: string): Promise<Session | null> {
  if (!supabase) throw new Error("Supabase is not configured.");
  const { data, error } = await supabase.auth.verifyOtp({ email, token, type: "email" });
  if (error) throw error;
  return data.session;
}

export async function signOut() {
  await supabase?.auth.signOut();
}

async function handleAuthUrl(raw: string) {
  if (!supabase || !raw.startsWith(REDIRECT_URL)) return;
  const u = new URL(raw);
  const code = u.searchParams.get("code");
  const err = u.searchParams.get("error_description");
  if (err) {
    window.dispatchEvent(new CustomEvent("lq-auth-error", { detail: err }));
    return;
  }
  if (code) {
    const { error } = await supabase.auth.exchangeCodeForSession(code);
    if (error) window.dispatchEvent(new CustomEvent("lq-auth-error", { detail: error.message }));
  }
}

/** Listens for logicquest://auth-callback links coming back from the browser. */
export async function initDeepLinks() {
  if (!inTauri || !supabase) return;
  try {
    const initial = await getCurrent();
    for (const u of initial ?? []) await handleAuthUrl(u);
    await onOpenUrl((urls) => urls.forEach((u) => void handleAuthUrl(u)));
    // Windows/Linux deliver the link to a second app instance, which forwards it here.
    await listen<string>("deep-link-url", (e) => void handleAuthUrl(e.payload));
  } catch (e) {
    console.warn("deep link setup failed", e);
  }
}
