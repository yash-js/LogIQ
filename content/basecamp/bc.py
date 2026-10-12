"""Basecamp: language lessons as small exercises.

Each language file (java.py, python.py, javascript.py) declares units with
`unit(...)` and adds exercises to it. build_basecamp.py runs every runnable
snippet with the real compiler/interpreter to fill in expected outputs and to
check that blanks, line orders, fixes and reference solutions are correct.

Exercise kinds
  choice   multiple choice                          (no code run)
  predict  read code, type its exact output         (expected = real output)
  blank    fill the ___ gaps in code                (every accepted answer must give the same output)
  order    put shuffled lines in order              (correct order must give the expected output)
  fix      edit buggy code so it prints the target  (buggy must differ, fixed must match)
  write    write a small program from a starter     (reference solution must pass every stdin test)

Java snippets are statements unless `full=True`; they are wrapped in
`public class Main { public static void main(String[] args) ... }` to run.
"""

from __future__ import annotations

import textwrap
from dataclasses import dataclass, field

UNITS: dict[str, list["Unit"]] = {"java": [], "python": [], "javascript": []}


def _d(s: str) -> str:
    return textwrap.dedent(s).strip("\n")


@dataclass
class Unit:
    lang: str
    id: str
    title: str
    intro: str
    exercises: list[dict] = field(default_factory=list)

    def choice(self, prompt, options, answer, why, code=None):
        assert 0 <= answer < len(options)
        self.exercises.append({"kind": "choice", "prompt": _d(prompt), "options": options, "answer": answer, "why": _d(why),
                               "code": _d(code) if code else None})
        return self

    def predict(self, code, why, stdin="", full=False, prompt="What does this print?"):
        self.exercises.append({"kind": "predict", "prompt": prompt, "code": _d(code), "why": _d(why), "stdin": stdin, "full": full})
        return self

    def blank(self, prompt, code, answers, why, stdin="", full=False):
        code = _d(code)
        assert code.count("___") == len(answers), (self.id, prompt)
        self.exercises.append({"kind": "blank", "prompt": _d(prompt), "code": code,
                               "blanks": [a if isinstance(a, list) else [a] for a in answers],
                               "why": _d(why), "stdin": stdin, "full": full})
        return self

    def order(self, prompt, code, why, stdin="", full=False):
        lines = [l for l in _d(code).split("\n") if l.strip()]
        assert len(set(lines)) == len(lines), (self.id, "order lines must be unique")
        self.exercises.append({"kind": "order", "prompt": _d(prompt), "lines": lines, "why": _d(why), "stdin": stdin, "full": full})
        return self

    def fix(self, prompt, buggy, fixed, why, stdin="", full=False):
        self.exercises.append({"kind": "fix", "prompt": _d(prompt), "code": _d(buggy), "solution": _d(fixed),
                               "why": _d(why), "stdin": stdin, "full": full})
        return self

    def write(self, prompt, starter, solution, tests, why, full=False):
        self.exercises.append({"kind": "write", "prompt": _d(prompt), "code": _d(starter), "solution": _d(solution),
                               "tests": tests, "why": _d(why), "full": full})
        return self


def unit(lang: str, title: str, intro: str) -> Unit:
    u = Unit(lang=lang, id=f"{lang}-{len(UNITS[lang]) + 1:02d}", title=title, intro=_d(intro))
    UNITS[lang].append(u)
    return u
