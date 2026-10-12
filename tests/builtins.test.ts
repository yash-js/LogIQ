import { findShortcuts } from "../src/lib/builtins.ts";
import problems from "../src/content/problems.json" with { type: "json" };

const P = (id: string) => (problems as any[]).find((p) => p.id === id);
let fail = 0;
function expect(name: string, got: string[], want: string[]) {
  const ok = JSON.stringify(got.sort()) === JSON.stringify(want.sort());
  if (!ok) fail++;
  console.log(ok ? "ok  " : "FAIL", name, ok ? "" : `got ${JSON.stringify(got)} want ${JSON.stringify(want)}`);
}
const ids = (code: string, lang: any, pid = "p4-01") => findShortcuts(code, lang, P(pid)).map((s) => s.id);

// Untouched starters never trigger anything.
for (const p of problems as any[]) for (const l of ["java", "python", "javascript"]) {
  const got = findShortcuts(p.starter[l], l as any, p).map((s) => s.id);
  if (got.length) { fail++; console.log("FAIL starter", p.id, l, got); }
}
console.log("starters checked");

expect("py sorted+set", ids("def solve(arr):\n    s = sorted(set(arr))\n    return s", "python"), ["sort", "set"]);
expect("py slice reverse", ids("def solve(s):\n    return s[::-1]", "python"), ["reverse"]);
expect("py comment ignored", ids("def solve(a):\n    # sorted(a) would be easy\n    return a", "python"), []);
expect("py string ignored", ids("def solve(a):\n    x = 'sorted('\n    return a", "python"), []);
expect("py max", ids("def solve(a, b, c):\n    return max(a, b, c)", "python"), ["maxmin"]);
expect("py loops fine", ids("def solve(arr):\n    best = arr[0]\n    for x in arr:\n        if x > best:\n            best = x\n    return [best]", "python"), []);
expect("java sort + Math.max", ids("static int solve(int[] a){ Arrays.sort(a); return Math.max(a[0], 1); }", "java"), ["sort", "maxmin"]);
expect("java HashSet", ids("static boolean solve(int[] a){ Set<Integer> s = new HashSet<>(); return true; }", "java"), ["set"]);
expect("java StringBuilder reverse", ids("static String solve(String s){ return new StringBuilder(s).reverse().toString(); }", "java"), ["reverse"]);
expect("java plain", ids("static int solve(int[] a){ int b=a[0]; for(int x: a) if (x>b) b=x; return b; }", "java"), []);
expect("js sort/includes", ids("function solve(a){ a.sort((x,y)=>x-y); return a.includes(3); }", "javascript"), ["sort", "search"]);
expect("js new Set", ids("function solve(a){ return new Set(a).size !== a.length; }", "javascript"), ["set"]);
expect("js template ignored", ids("function solve(a){ return `${'x'}.sort(`; }", "javascript"), []);
expect("js BigInt allowed for long", findShortcuts("function solve(n){ let f = 1n; return f; }", "javascript", P("p2-12")).map((s) => s.id), []);
expect("js BigInt flagged for add strings", findShortcuts("function solve(num1, num2){ return String(BigInt(num1)+BigInt(num2)); }", "javascript", P("p6-06")).map((s) => s.id), ["bignum"]);
expect("py whole int add strings", findShortcuts("def solve(num1, num2):\n    return str(int(num1) + int(num2))", "python", P("p6-06")).map((s) => s.id), ["wholeint"]);
expect("py int(c) digit fine", findShortcuts("def solve(num1, num2):\n    d = int(num1[0])\n    return ''", "python", P("p6-06")).map((s) => s.id), []);
expect("py bin", ids("def solve(n):\n    return bin(n)[2:]", "python"), ["base"]);
expect("py datetime", ids("def solve(d, m, y):\n    import datetime\n    return ''", "python"), ["dates"]);
expect("below marker ignored", ids("def solve(a):\n    return a\n\n# ---------- input / output is handled below, no need to change it ----------\nprint(sorted(a))", "python"), []);
process.exit(fail ? 1 : 0);
