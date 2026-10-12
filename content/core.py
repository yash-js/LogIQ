"""Problem registry, I/O serialisation and starter-code generation.

Every problem is a Python reference function decorated with @problem.
The build script runs the reference on each test's arguments to produce the
expected output, so expected outputs are never typed by hand.

Input format (stdin), one parameter after another:
  int / long / double / char / str   -> one line
  int[]                              -> line with n, then a line with n numbers
  int[K]                             -> one line with exactly K numbers
  str[]                              -> line with n, then n lines
  int[][]                            -> line "rows cols", then one line per row

Return types and how they are printed:
  int long double bool str           -> one line (bool as true/false)
  int[] int_list long_list bool_list double_list -> one line, space separated
  str_list                           -> one item per line
  int[][] int_list_2d                -> one row per line
  void (mode="print")                -> the learner prints the output directly
"""

from __future__ import annotations

import inspect
import random
import textwrap
from dataclasses import dataclass, field
from typing import Any, Callable

REGISTRY: list["Problem"] = []

XP = {"easy": 10, "medium": 20, "stretch": 40}


@dataclass
class Problem:
    id: str
    phase: int
    title: str
    difficulty: str
    statement: str
    params: list[tuple[str, str]]
    returns: str
    tests: list[tuple]
    hints: list | dict
    concepts: list[str]
    ref: Callable
    mode: str = "solve"  # "solve" -> learner returns a value; "print" -> learner prints
    practice: dict | None = None
    time_limit_ms: int = 2000
    examples: int = 2
    strict: bool = False
    notes: list[str] = field(default_factory=list)
    # hints may be a shared list, a {lang: [3 strings]} dict, or a mixed list. See normalize_hints.


_counters: dict[int, int] = {}


def _clean(text: str) -> str:
    """Dedent statements that mix indented triple-quoted text with concatenated pieces."""
    lines = text.strip("\n").split("\n")
    indents = [len(l) - len(l.lstrip(" ")) for l in lines[1:] if l.strip()]
    ind = min([i for i in indents if i > 0], default=0)
    out = []
    for l in lines:
        lead = len(l) - len(l.lstrip(" "))
        out.append(l[min(lead, ind):])
    return "\n".join(out).strip()


LANGS = ("java", "python", "javascript")


def normalize_hints(hints) -> dict[str, list[str]]:
    """Turn a shared list, a per-language dict, or a mixed list into three lists of 3."""
    if isinstance(hints, dict) and hints and all(isinstance(v, list) for v in hints.values()):
        missing = [lang for lang in LANGS if lang not in hints]
        assert not missing, f"hints missing {missing}"
        for lang in LANGS:
            assert len(hints[lang]) == 3 and all(isinstance(s, str) for s in hints[lang]), (lang, hints[lang])
        return {lang: list(hints[lang]) for lang in LANGS}
    assert isinstance(hints, list) and len(hints) == 3, "a problem needs exactly 3 hints"
    out: dict[str, list[str]] = {lang: [] for lang in LANGS}
    for item in hints:
        if isinstance(item, str):
            for lang in LANGS:
                out[lang].append(item)
        elif isinstance(item, dict):
            for lang in LANGS:
                assert lang in item and isinstance(item[lang], str), item
                out[lang].append(item[lang])
        else:
            raise AssertionError(f"bad hint entry: {item!r}")
    return out


def problem(*, phase: int, title: str, difficulty: str = "easy", statement: str,
            params: list[tuple[str, str]], returns: str, tests: list[tuple] | None = None,
            gen: Callable[[random.Random], tuple] | None = None, gen_count: int = 0,
            hints: list | dict, concepts: list[str], mode: str = "solve",
            practice: tuple[str, str] | None = None, time_limit_ms: int = 2000,
            examples: int = 2, seed: int | None = None, strict: bool = False):
    def wrap(fn):
        _counters[phase] = _counters.get(phase, 0) + 1
        pid = f"p{phase}-{_counters[phase]:02d}"
        all_tests = list(tests or [])
        if gen:
            rng = random.Random(f"{pid}-{seed}")
            for _ in range(gen_count):
                all_tests.append(gen(rng))
        normalize_hints(hints)  # shape check; build.py stores the normalised form
        REGISTRY.append(Problem(
            id=pid, phase=phase, title=title, difficulty=difficulty,
            statement=_clean(statement), params=params, returns=returns,
            tests=all_tests, hints=hints, concepts=concepts, ref=fn, mode=mode,
            practice={"label": practice[0], "url": practice[1]} if practice else None,
            time_limit_ms=time_limit_ms, examples=examples, strict=strict,
        ))
        return fn
    return wrap


# --------------------------------------------------------------------------- I/O

def fmt_num(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float):
        if abs(v) >= 1e15:
            return repr(v)  # keeps an exponent so checkers compare with tolerance
        if v == int(v):
            return f"{v:.1f}"
        s = f"{v:.6f}".rstrip("0").rstrip(".")
        return s
    return str(v)


def serialize_input(ptype: str, v: Any) -> str:
    if ptype in ("int", "long", "double"):
        return fmt_num(v)
    if ptype in ("char", "str"):
        return v
    if ptype == "int[]":
        return f"{len(v)}\n{' '.join(map(str, v))}"
    if ptype.startswith("int[") and ptype.endswith("]") and ptype[4:-1].isdigit():
        assert len(v) == int(ptype[4:-1]), (ptype, v)
        return " ".join(map(str, v))
    if ptype == "str[]":
        return "\n".join([str(len(v)), *v])
    if ptype == "int[][]":
        cols = len(v[0]) if v else 0
        return "\n".join([f"{len(v)} {cols}", *(" ".join(map(str, r)) for r in v)])
    raise ValueError(ptype)


def build_input(p: Problem, args: tuple) -> str:
    assert len(args) == len(p.params), (p.id, args)
    return "\n".join(serialize_input(t, a) for (_, t), a in zip(p.params, args)) + "\n"


def format_output(rtype: str, v: Any) -> str:
    if rtype in ("int", "long", "double", "bool"):
        return fmt_num(v)
    if rtype == "str":
        return v
    if rtype in ("int[]", "int_list", "long_list", "bool_list", "double_list"):
        return " ".join(fmt_num(x) for x in v)
    if rtype in ("str_list", "lines"):
        return "\n".join(v)
    if rtype in ("int[][]", "int_list_2d"):
        return "\n".join(" ".join(map(str, r)) for r in v)
    raise ValueError(rtype)


# ------------------------------------------------------------------ starter code

JAVA_TYPES = {
    "int": "int", "long": "long", "double": "double", "char": "char", "str": "String",
    "int[]": "int[]", "str[]": "String[]", "int[][]": "int[][]",
}
JAVA_RET = {
    "int": "int", "long": "long", "double": "double", "bool": "boolean", "str": "String",
    "int[]": "int[]", "int_list": "List<Integer>", "long_list": "List<Long>",
    "bool_list": "List<Boolean>", "double_list": "double[]", "str_list": "List<String>",
    "int[][]": "int[][]", "int_list_2d": "List<List<Integer>>", "void": "void",
}
JAVA_DEFAULT = {
    "int": "0", "long": "0L", "double": "0.0", "boolean": "false", "String": '""',
    "int[]": "new int[0]", "double[]": "new double[0]", "int[][]": "new int[0][0]",
}


def java_param_type(t: str) -> str:
    if t.startswith("int[") and t[4:-1].isdigit():
        return "int[]"
    return JAVA_TYPES[t]


def java_reader(t: str) -> str:
    if t.startswith("int[") and t[4:-1].isdigit():
        return "readInts()"
    return {
        "int": "readInt()", "long": "readLong()", "double": "readDouble()", "char": "readChar()",
        "str": "readLine()", "int[]": "readIntArray()", "str[]": "readStringArray()",
        "int[][]": "readMatrix()",
    }[t]


JAVA_HELPERS = {
    "readLine": """    static String readLine() throws IOException {
        String s = br.readLine();
        return s == null ? "" : s;
    }""",
    "readInt": """    static int readInt() throws IOException {
        return Integer.parseInt(readLine().trim());
    }""",
    "readLong": """    static long readLong() throws IOException {
        return Long.parseLong(readLine().trim());
    }""",
    "readDouble": """    static double readDouble() throws IOException {
        return Double.parseDouble(readLine().trim());
    }""",
    "readChar": """    static char readChar() throws IOException {
        return readLine().charAt(0);
    }""",
    "readInts": """    static int[] readInts() throws IOException {
        String s = readLine().trim();
        if (s.isEmpty()) return new int[0];
        String[] parts = s.split("\\\\s+");
        int[] a = new int[parts.length];
        for (int i = 0; i < parts.length; i++) a[i] = Integer.parseInt(parts[i]);
        return a;
    }""",
    "readIntArray": """    static int[] readIntArray() throws IOException {
        int n = readInt();
        int[] a = readInts();
        return a.length == n ? a : Arrays.copyOf(a, n);
    }""",
    "readStringArray": """    static String[] readStringArray() throws IOException {
        int n = readInt();
        String[] a = new String[n];
        for (int i = 0; i < n; i++) a[i] = readLine();
        return a;
    }""",
    "readMatrix": """    static int[][] readMatrix() throws IOException {
        int rows = readInts()[0];
        int[][] m = new int[rows][];
        for (int i = 0; i < rows; i++) m[i] = readInts();
        return m;
    }""",
}
HELPER_DEPS = {
    "readInt": ["readLine"], "readLong": ["readLine"], "readDouble": ["readLine"],
    "readChar": ["readLine"], "readInts": ["readLine"], "readIntArray": ["readInt", "readInts"],
    "readStringArray": ["readInt", "readLine"], "readMatrix": ["readInts"],
}


def java_print(rt: str) -> str:
    if rt in ("int", "long", "double", "bool", "str"):
        return "System.out.println(ans);"
    if rt == "int[]":
        return "System.out.println(Arrays.stream(ans).mapToObj(String::valueOf).collect(Collectors.joining(\" \")));"
    if rt == "double_list":
        return "System.out.println(Arrays.stream(ans).mapToObj(String::valueOf).collect(Collectors.joining(\" \")));"
    if rt in ("int_list", "long_list", "bool_list"):
        return "System.out.println(ans.stream().map(String::valueOf).collect(Collectors.joining(\" \")));"
    if rt == "str_list":
        return "for (String line : ans) System.out.println(line);"
    if rt == "int[][]":
        return ("for (int[] row : ans)\n"
                "            System.out.println(Arrays.stream(row).mapToObj(String::valueOf).collect(Collectors.joining(\" \")));")
    if rt == "int_list_2d":
        return ("for (List<Integer> row : ans)\n"
                "            System.out.println(row.stream().map(String::valueOf).collect(Collectors.joining(\" \")));")
    raise ValueError(rt)


def java_starter(p: Problem, body: str | None = None) -> str:
    ret = "void" if p.mode == "print" else JAVA_RET[p.returns]
    sig = ", ".join(f"{java_param_type(t)} {n}" for n, t in p.params)
    if body is None:
        if ret == "void":
            body = "        // Print your output here using System.out.println / System.out.print\n"
        else:
            default = JAVA_DEFAULT.get(ret, "new ArrayList<>()")
            body = f"        // Write your logic here\n\n        return {default};\n"
    needed: list[str] = []

    def need(h):
        for d in HELPER_DEPS.get(h, []):
            need(d)
        if h not in needed:
            needed.append(h)

    reads = []
    for n, t in p.params:
        r = java_reader(t)
        need(r[:-2])
        reads.append(f"        {java_param_type(t)} {n} = {r};")
    call = ", ".join(n for n, _ in p.params)
    if ret == "void":
        out = f"        solve({call});"
    else:
        out = f"        {ret} ans = solve({call});\n        {java_print(p.returns)}"
    helpers = "\n\n".join(JAVA_HELPERS[h] for h in needed)
    return f"""import java.io.*;
import java.util.*;
import java.util.stream.*;

public class Main {{

    static {ret} solve({sig}) {{
{body.rstrip()}
    }}

    // ---------- input / output is handled below, no need to change it ----------

    public static void main(String[] args) throws IOException {{
{chr(10).join(reads)}
{out}
    }}

    static BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

{helpers}
}}
"""


def py_reader(n: str, t: str) -> str:
    if t in ("int", "long"):
        return f"{n} = int(input())"
    if t == "double":
        return f"{n} = float(input())"
    if t == "char":
        return f"{n} = input()[0]"
    if t == "str":
        return f"{n} = input()"
    if t == "int[]":
        return f"input()\n{n} = list(map(int, input().split()))"
    if t.startswith("int[") and t[4:-1].isdigit():
        return f"{n} = list(map(int, input().split()))"
    if t == "str[]":
        return f"{n} = [input() for _ in range(int(input()))]"
    if t == "int[][]":
        return f"{n} = [list(map(int, input().split())) for _ in range(int(input().split()[0]))]"
    raise ValueError(t)


def py_print(rt: str) -> str:
    if rt == "bool":
        return "print(str(ans).lower())"
    if rt in ("int", "long", "double", "str"):
        return "print(ans)"
    if rt == "bool_list":
        return "print(*[str(x).lower() for x in ans])"
    if rt in ("int[]", "int_list", "long_list", "double_list"):
        return "print(*ans)"
    if rt == "str_list":
        return 'print(*ans, sep="\\n")'
    if rt in ("int[][]", "int_list_2d"):
        return "for row in ans:\n    print(*row)"
    raise ValueError(rt)


def py_starter(p: Problem, body: str | None = None) -> str:
    sig = ", ".join(n for n, _ in p.params)
    if body is None:
        if p.mode == "print":
            body = "    # Print your output here\n    pass\n"
        else:
            body = "    # Write your logic here\n    pass\n"
    reads = "\n".join(py_reader(n, t) for n, t in p.params)
    out = f"solve({sig})" if p.mode == "print" else f"ans = solve({sig})\n{py_print(p.returns)}"
    return f"""def solve({sig}):
{body.rstrip()}


# ---------- input / output is handled below, no need to change it ----------

{reads}
{out}
"""


# ------------------------------------------------------------------ JavaScript

JS_HELPERS = {
    "readLine": 'const readLine = () => __lines[__at++] ?? "";',
    "readInt": "const readInt = () => Number(readLine().trim());",
    "readDouble": "const readDouble = () => Number(readLine().trim());",
    "readInts": 'const readInts = () => {\n  const s = readLine().trim();\n  return s ? s.split(/\\s+/).map(Number) : [];\n};',
    "readIntArray": "const readIntArray = () => {\n  readLine(); // length\n  return readInts();\n};",
    "readStringArray": "const readStringArray = () => {\n  const n = readInt();\n  return Array.from({ length: n }, () => readLine());\n};",
    "readMatrix": "const readMatrix = () => {\n  const rows = readInts()[0];\n  return Array.from({ length: rows }, () => readInts());\n};",
}
JS_DEPS = {
    "readInt": ["readLine"], "readDouble": ["readLine"], "readInts": ["readLine"],
    "readIntArray": ["readLine", "readInts"], "readStringArray": ["readInt", "readLine"],
    "readMatrix": ["readInts"],
}


def js_reader(t: str) -> str:
    if t.startswith("int[") and t[4:-1].isdigit():
        return "readInts()"
    return {
        "int": "readInt()", "long": "readInt()", "double": "readDouble()", "char": "readLine()[0]",
        "str": "readLine()", "int[]": "readIntArray()", "str[]": "readStringArray()", "int[][]": "readMatrix()",
    }[t]


def js_print(rt: str) -> str:
    if rt in ("int", "long", "double", "bool", "str"):
        return "console.log(String(ans));"
    if rt in ("int[]", "int_list", "long_list", "bool_list", "double_list"):
        return 'console.log(ans.join(" "));'
    if rt == "str_list":
        return 'console.log(ans.join("\\n"));'
    if rt in ("int[][]", "int_list_2d"):
        return 'for (const row of ans) console.log(row.join(" "));'
    raise ValueError(rt)


JS_DEFAULT = {"int": "0", "long": "0", "double": "0", "bool": "false", "str": '""'}


def js_starter(p: Problem, body: str | None = None, big: bool = False) -> str:
    sig = ", ".join(n for n, _ in p.params)
    if body is None:
        if p.mode == "print":
            body = "  // Print your output here with console.log\n"
        else:
            tip = ("  // The answer can be larger than Number.MAX_SAFE_INTEGER.\n"
                   "  // Use BigInt (e.g. 1n, BigInt(x)) to keep it exact.\n") if big else ""
            body = f"{tip}  // Write your logic here\n\n  return {JS_DEFAULT.get(p.returns, '[]')};\n"
    needed: list[str] = []

    def need(h):
        for d in JS_DEPS.get(h, []):
            need(d)
        if h not in needed:
            needed.append(h)

    reads = []
    for n, t in p.params:
        r = js_reader(t)
        need(r.split("(")[0])
        reads.append(f"const {n} = {r};")
    out = f"solve({sig});" if p.mode == "print" else f"const ans = solve({sig});\n{js_print(p.returns)}"
    helpers = "\n".join(JS_HELPERS[h] for h in needed)
    return f"""function solve({sig}) {{
{body.rstrip()}
}}

// ---------- input / output is handled below, no need to change it ----------

const __lines = require("fs").readFileSync(0, "utf8").split(/\\r?\\n/);
let __at = 0;
{helpers}

{chr(10).join(reads)}
{out}
"""


def ref_body(p: Problem) -> str:
    """Source of the reference function body, re-indented to 4 spaces."""
    src = inspect.getsource(p.ref)
    lines = src.splitlines()
    i = next(k for k, l in enumerate(lines) if l.lstrip().startswith("def "))
    body = textwrap.dedent("\n".join(lines[i + 1:]))
    return textwrap.indent(body, "    ") + "\n"
