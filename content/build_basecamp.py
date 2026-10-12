"""Builds src/content/basecamp.json and checks every Basecamp exercise by running it.

    python3 content/build_basecamp.py
"""

import importlib
import json
import os
import re
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
        if ex.get("tests"):
            built = []
            for stdin in ex["tests"]:
                good = ok_run(ex["solution"], stdin)
                built.append({"input": stdin, "output": good["out"]})
            ex["tests"] = built
            ex["stdin"] = built[0]["input"]
            ex["expected"] = built[0]["output"]
            passes = 0
            for t in built:
                bad = run(lang, ex["code"], t["input"], full)
                if bad["rc"] == 0 and check(t["output"], bad["out"], True):
                    passes += 1
            if passes == len(built):
                errs.append(f"{where}: the buggy version already produces the right output")
        else:
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


def structural_errors():
    """Shape checks that don't need a compiler. Exercise runners add their own."""
    errs = []
    for lang in LANGS:
        units = bc.UNITS[lang]
        core = [u for u in units if u.section == "core"]
        oop = [u for u in units if u.section == "oop"]
        exercises = sum(len(u.exercises) for u in units)
        if len(units) != 20 or exercises != 120 or len(core) != 10 or len(oop) != 10:
            errs.append(f"{lang}: expected 20 units (10 core + 10 oop) and 120 exercises, "
                        f"got {len(units)} units ({len(core)} core, {len(oop)} oop) and {exercises} exercises")
        for u in oop:
            kinds = [e["kind"] for e in u.exercises]
            if len(u.exercises) != 6:
                errs.append(f"{u.id}: expected 6 exercises, got {len(u.exercises)}")
            for need in ("predict", "fix", "write"):
                if need not in kinds:
                    errs.append(f"{u.id}: missing a {need} exercise")
            words = len(re.findall(r"\b\w+\b", u.intro))
            if words > 180:
                errs.append(f"{u.id}: intro is {words} words (keep it under 180)")
            if lang == "java":
                for i, ex in enumerate(u.exercises):
                    if ex["kind"] != "choice" and not ex.get("full"):
                        errs.append(f"{u.id} #{i + 1}: Java OOP exercise must set full=True")
            if u.id.endswith("-oop-10"):
                for ex in u.exercises:
                    if ex["kind"] == "write" and len(ex.get("tests") or []) < 3:
                        errs.append(f"{u.id}: write needs 3+ tests")
                    if ex["kind"] == "fix" and len(ex.get("tests") or []) < 3:
                        errs.append(f"{u.id}: fix needs 3+ tests")
    return errs


def main():
    for lang in LANGS:
        importlib.import_module(lang)
        importlib.import_module(f"{lang}_oop")
    errors = structural_errors()
    jobs = []
    for lang in LANGS:
        for u in bc.UNITS[lang]:
            for i, ex in enumerate(u.exercises):
                jobs.append((lang, u.id, i, ex))
    with ThreadPoolExecutor(max_workers=max(2, (os.cpu_count() or 2))) as pool:
        for errs in pool.map(lambda j: check_exercise(*j), jobs):
            errors += errs
    out = {}
    for lang in LANGS:
        out[lang] = [
            {"id": u.id, "title": u.title, "intro": u.intro, "section": u.section, "exercises": u.exercises}
            for u in bc.UNITS[lang]
        ]
    counts = {l: (len(out[l]), sum(len(u["exercises"]) for u in out[l])) for l in LANGS}
    if errors:
        print("\n\n".join(errors))
        print(f"\n{len(errors)} problem(s); basecamp.json not written")
        sys.exit(1)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("basecamp ok (units, exercises):", counts)


if __name__ == "__main__":
    main()
