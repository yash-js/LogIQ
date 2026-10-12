"""Builds src/content/problems.json from the phase files and validates it.

    python3 content/build.py            # build JSON
    python3 content/build.py --verify   # also run every reference through real
                                        # Python and Java processes end to end
"""

import importlib
import json
import os
import subprocess
import sys
import tempfile
import textwrap
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import core  # noqa: E402
from checker import check  # noqa: E402

OUT = os.path.join(HERE, "..", "src", "content", "problems.json")
PHASES = [int(x) for x in os.environ.get("LQ_PHASES", "1,2,3,4,5,6").split(",")]


def load():
    for ph in PHASES:
        importlib.import_module(f"phase{ph}")
    return core.REGISTRY


def expected_for(p, args):
    import copy
    val = p.ref(*copy.deepcopy(args))
    return core.format_output(p.returns, val)


def build(problems):
    out = []
    for p in problems:
        tests = []
        for args in p.tests:
            tests.append({"input": core.build_input(p, args), "output": expected_for(p, args)})
        assert len(tests) >= 5, f"{p.id} {p.title}: only {len(tests)} tests"
        inputs = [t["input"] for t in tests]
        assert len(set(inputs)) == len(inputs), f"{p.id}: duplicate tests"
        out.append({
            "id": p.id,
            "phase": p.phase,
            "title": p.title,
            "difficulty": p.difficulty,
            "xp": core.XP[p.difficulty],
            "concepts": p.concepts,
            "statement": p.statement,
            "params": [{"name": n, "type": t} for n, t in p.params],
            "returns": "void" if p.mode == "print" else p.returns,
            "mode": p.mode,
            "strict": p.strict,
            "timeLimitMs": p.time_limit_ms,
            "examples": tests[: p.examples],
            "tests": tests,
            "hints": p.hints,
            "practice": p.practice,
            "starter": {"java": core.java_starter(p), "python": core.py_starter(p)},
        })
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    by_phase = {}
    for p in out:
        by_phase[p["phase"]] = by_phase.get(p["phase"], 0) + 1
    print(f"wrote {len(out)} problems {by_phase} -> {os.path.relpath(OUT)}")
    return out


# ------------------------------------------------------------------ verification

def run(cmd, cwd, stdin, timeout=20):
    env = dict(os.environ)
    env.pop("JAVA_TOOL_OPTIONS", None)
    r = subprocess.run(cmd, cwd=cwd, input=stdin, capture_output=True, text=True, timeout=timeout, env=env)
    return r


def py_solution(p):
    body = core.ref_body(p)
    sig = ", ".join(n for n, _ in p.params)
    if p.mode == "print":
        body = (f"    def _ref({sig}):\n" + textwrap.indent(body, "    ")
                + f"    for _line in _ref({sig}):\n        print(_line)\n")
    return core.py_starter(p, body)


def java_literal(rt, v):
    def jstr(s):
        return json.dumps(s)
    if rt in ("int",):
        return str(v)
    if rt == "long":
        return f"{v}L"
    if rt == "double":
        return repr(float(v))
    if rt == "bool":
        return "true" if v else "false"
    if rt == "str":
        return jstr(v)
    if rt == "int[]":
        return "new int[]{" + ", ".join(map(str, v)) + "}"
    if rt == "double_list":
        return "new double[]{" + ", ".join(repr(float(x)) for x in v) + "}"
    if rt == "int_list":
        return "new ArrayList<>(List.of(" + ", ".join(map(str, v)) + "))"
    if rt == "long_list":
        return "new ArrayList<>(List.of(" + ", ".join(f"{x}L" for x in v) + "))"
    if rt == "bool_list":
        return "new ArrayList<>(List.of(" + ", ".join("true" if x else "false" for x in v) + "))"
    if rt in ("str_list", "lines"):
        return "new ArrayList<>(List.of(" + ", ".join(jstr(x) for x in v) + "))"
    if rt == "int[][]":
        return "new int[][]{" + ", ".join("{" + ", ".join(map(str, r)) + "}" for r in v) + "}"
    if rt == "int_list_2d":
        return "new ArrayList<>(List.of(" + ", ".join("List.of(" + ", ".join(map(str, r)) + ")" for r in v) + "))"
    raise ValueError(rt)


def java_io_program(p, args):
    """Java starter whose solve() returns/prints the expected value for `args`.
    Verifies the generated input readers and output printers end to end."""
    import copy
    val = p.ref(*copy.deepcopy(args))
    if p.mode == "print":
        lines = "".join(f"        System.out.println({json.dumps(l)});\n" for l in val)
        body = lines
    else:
        body = f"        return {java_literal(p.returns, val)};\n"
    return core.java_starter(p, body)


def verify(problems, built):
    by_id = {b["id"]: b for b in built}
    failures = []

    def verify_one(p):
        b = by_id[p.id]
        errs = []
        with tempfile.TemporaryDirectory() as d:
            # Python: the full reference runs through the real starter template on every test.
            with open(os.path.join(d, "main.py"), "w") as f:
                f.write(py_solution(p))
            import time
            slowest = 0.0
            for i, t in enumerate(b["tests"]):
                t0 = time.time()
                r = run([sys.executable, "main.py"], d, t["input"])
                slowest = max(slowest, time.time() - t0)
                if slowest * 1000 > p.time_limit_ms * 0.4:
                    errs.append(f"reference is slow: {slowest*1000:.0f} ms vs limit {p.time_limit_ms} ms")
                if r.returncode != 0 or not check(t["output"], r.stdout, p.strict):
                    errs.append(f"py test {i}: rc={r.returncode} got={r.stdout[:200]!r} want={t['output'][:200]!r} err={r.stderr[-400:]}")
                    break
            # Java: the starter compiles, reads every test's input, and prints in the checked format.
            for i, (args, t) in enumerate(zip(p.tests, b["tests"])):
                if (i >= 2 and i != len(p.tests) - 1) or len(t["output"]) > 20000:
                    continue  # huge literals exceed Java's method size limit
                jd = os.path.join(d, f"j{i}")
                os.makedirs(jd)
                with open(os.path.join(jd, "Main.java"), "w") as f:
                    f.write(java_io_program(p, args))
                c = run(["javac", "-nowarn", "Main.java"], jd, "", timeout=60)
                if c.returncode != 0:
                    errs.append(f"javac test {i}: {c.stderr[:800]}")
                    break
                r = run(["java", "-cp", ".", "Main"], jd, t["input"])
                if r.returncode != 0 or not check(t["output"], r.stdout, p.strict):
                    errs.append(f"java test {i}: got={r.stdout[:200]!r} want={t['output'][:200]!r} err={r.stderr[-400:]}")
                    break
            # Untouched starters must compile / parse.
            with open(os.path.join(d, "Main.java"), "w") as f:
                f.write(b["starter"]["java"])
            c = run(["javac", "-nowarn", "Main.java"], d, "", timeout=60)
            if c.returncode != 0:
                errs.append(f"blank java starter does not compile: {c.stderr[:600]}")
            c = run([sys.executable, "-c", "import ast,sys; ast.parse(sys.stdin.read())"], d, b["starter"]["python"])
            if c.returncode != 0:
                errs.append("blank python starter does not parse")
        return p, errs

    with ThreadPoolExecutor(max_workers=max(2, os.cpu_count() or 2)) as ex:
        for p, errs in ex.map(verify_one, problems):
            status = "ok " if not errs else "ERR"
            print(f"{status} {p.id} {p.title}")
            for e in errs:
                print("     " + e)
            if errs:
                failures.append(p.id)
    print(f"\n{len(problems) - len(failures)}/{len(problems)} verified")
    return not failures


if __name__ == "__main__":
    probs = load()
    built = build(probs)
    if "--verify" in sys.argv:
        only = [a for a in sys.argv[1:] if a.startswith("p")]
        sel = [p for p in probs if not only or any(p.id.startswith(o) for o in only)]
        sys.exit(0 if verify(sel, built) else 1)
