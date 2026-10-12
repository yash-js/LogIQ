"""Builds src/content/basecamp.json and checks every Basecamp exercise by running it.

    python3 content/build_basecamp.py
"""

import importlib
import json
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "basecamp"))
sys.path.insert(0, HERE)

import bc  # noqa: E402
from checker import check  # noqa: E402

OUT = os.path.join(HERE, "..", "src", "content", "basecamp.json")
LANGS = ["java", "python", "javascript"]


def java_wrap(code: str) -> str:
    """Keep in sync with wrapJava() in src/lib/basecamp.ts."""
    body = "\n".join(("        " + l) if l.strip() else "" for l in code.split("\n"))
    return (
        "import java.util.*;\nimport java.io.*;\n\npublic class Main {\n"
        "    public static void main(String[] args) throws Exception {\n"
        f"{body}\n    }}\n}}\n"
    )


def run(lang, code, stdin="", full=False):
    env = dict(os.environ)
    env.pop("JAVA_TOOL_OPTIONS", None)
    with tempfile.TemporaryDirectory() as d:
        if lang == "java":
            src = code if full else java_wrap(code)
            with open(os.path.join(d, "Main.java"), "w") as f:
                f.write(src)
            c = subprocess.run(["javac", "-nowarn", "Main.java"], cwd=d, capture_output=True, text=True, env=env, timeout=60)
            if c.returncode != 0:
                return {"rc": "compile", "out": "", "err": c.stderr}
            cmd = ["java", "-cp", ".", "Main"]
        elif lang == "python":
            with open(os.path.join(d, "main.py"), "w") as f:
                f.write(code)
            cmd = [sys.executable, "main.py"]
        else:
            with open(os.path.join(d, "main.js"), "w") as f:
                f.write(code)
            cmd = ["node", "main.js"]
        try:
            r = subprocess.run(cmd, cwd=d, input=stdin, capture_output=True, text=True, env=env, timeout=15)
        except subprocess.TimeoutExpired:
            return {"rc": "timeout", "out": "", "err": "timeout"}
        return {"rc": r.returncode, "out": r.stdout, "err": r.stderr}


def fill(code, choices):
    parts = code.split("___")
    out = parts[0]
    for c, p in zip(choices, parts[1:]):
        out += c + p
    return out


def check_exercise(lang, uid, i, ex):
    """Fills computed fields in place. Returns a list of problems found."""
    errs = []
    k = ex["kind"]
    full = ex.get("full", False)
    where = f"{uid} #{i + 1} {k}"

    def ok_run(code, stdin=""):
        r = run(lang, code, stdin, full)
        if r["rc"] != 0:
            errs.append(f"{where}: did not run cleanly ({r['rc']}): {r['err'][-400:]}\n{code}")
        return r

    if k == "predict":
        r = ok_run(ex["code"], ex["stdin"])
        ex["expected"] = r["out"]
        if not r["out"].strip():
            errs.append(f"{where}: prints nothing")
    elif k == "blank":
        firsts = [b[0] for b in ex["blanks"]]
        base = ok_run(fill(ex["code"], firsts), ex["stdin"])
        ex["expected"] = base["out"]
        for bi, alts in enumerate(ex["blanks"]):
            for alt in alts[1:]:
                ch = list(firsts)
                ch[bi] = alt
                r = run(lang, fill(ex["code"], ch), ex["stdin"], full)
                if r["rc"] != 0 or r["out"] != base["out"]:
                    errs.append(f"{where}: accepted answer {alt!r} for blank {bi + 1} gives a different result")
    elif k == "order":
        r = ok_run("\n".join(ex["lines"]), ex["stdin"])
        ex["expected"] = r["out"]
        if len(ex["lines"]) < 3:
            errs.append(f"{where}: needs at least 3 lines")
    elif k == "fix":
        good = ok_run(ex["solution"], ex["stdin"])
        ex["expected"] = good["out"]
        bad = run(lang, ex["code"], ex["stdin"], full)
        if bad["rc"] == 0 and check(good["out"], bad["out"], True):
            errs.append(f"{where}: the buggy version already produces the right output")
    elif k == "write":
        tests = []
        for stdin in ex["tests"]:
            r = ok_run(ex["solution"], stdin)
            tests.append({"input": stdin, "output": r["out"]})
        ex["tests"] = tests
        passes_all = all(
            (lambda r: r["rc"] == 0 and check(t["output"], r["out"], False))(run(lang, ex["code"], t["input"], full)) for t in tests
        )
        if passes_all:
            errs.append(f"{where}: the starter already passes every test")
    elif k == "choice":
        pass
    else:
        errs.append(f"{where}: unknown kind")
    return errs


def main():
    for lang in LANGS:
        importlib.import_module(lang)
    jobs = []
    for lang in LANGS:
        for u in bc.UNITS[lang]:
            for i, ex in enumerate(u.exercises):
                jobs.append((lang, u.id, i, ex))
    errors = []
    with ThreadPoolExecutor(max_workers=max(2, (os.cpu_count() or 2))) as pool:
        for errs in pool.map(lambda j: check_exercise(*j), jobs):
            errors += errs
    out = {}
    for lang in LANGS:
        out[lang] = [
            {"id": u.id, "title": u.title, "intro": u.intro, "exercises": u.exercises}
            for u in bc.UNITS[lang]
        ]
    counts = {l: (len(out[l]), sum(len(u["exercises"]) for u in out[l])) for l in LANGS}
    if errors:
        print("\n\n".join(errors))
        print(f"\n{len(errors)} problem(s); basecamp.json not written")
        sys.exit(1)
    with open(OUT, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("basecamp ok (units, exercises):", counts)


if __name__ == "__main__":
    main()
