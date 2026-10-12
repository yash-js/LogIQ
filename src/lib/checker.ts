// Output comparison. Keep in sync with content/checker.py.

function lines(text: string): string[] {
  const ls = text.replace(/\r\n/g, "\n").split("\n").map((l) => l.replace(/\s+$/, ""));
  while (ls.length && ls[ls.length - 1] === "") ls.pop();
  return ls;
}

function num(tok: string): number | null {
  if (!/^[-+]?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?$/.test(tok)) return null;
  const v = Number(tok);
  return Number.isFinite(v) ? v : null;
}

function tokEq(actual: string, expected: string): boolean {
  if (actual === expected) return true;
  const la = actual.toLowerCase();
  if ((la === "true" || la === "false") && la === expected.toLowerCase()) return true;
  const x = num(actual);
  const y = num(expected);
  if (x === null || y === null) return false;
  const both = actual + expected;
  if (!both.includes(".") && !/e/i.test(both)) return false; // integers must match exactly
  return Math.abs(x - y) <= 1e-5 * Math.max(1, Math.abs(y));
}

export function outputsMatch(expected: string, actual: string, strict: boolean): boolean {
  const e = lines(expected);
  const a = lines(actual);
  if (e.length !== a.length) return false;
  for (let i = 0; i < e.length; i++) {
    if (e[i] === a[i]) continue;
    if (strict) return false;
    const te = e[i].split(/\s+/).filter(Boolean);
    const ta = a[i].split(/\s+/).filter(Boolean);
    if (te.length !== ta.length) return false;
    for (let k = 0; k < te.length; k++) if (!tokEq(ta[k], te[k])) return false;
  }
  return true;
}
