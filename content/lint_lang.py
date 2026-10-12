"""Fail if teaching text for one language mentions another language's markers.

    python3 content/lint_lang.py

Visible text is the guide, the quiz, that language's hints, and the problem
statement after `:::only` filtering. Markdown table rows and fenced code blocks
tagged java / python / javascript are not scanned: tables are allowed to compare
languages, and fenced samples are either hidden or are that language's own code.
"""

from __future__ import annotations

import importlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)

import core  # noqa: E402

LANGS = ("java", "python", "javascript")
FENCE_LANG = {"java": "java", "python": "python", "javascript": "javascript", "js": "javascript"}

# Suggested markers from the language pass. Dots and brackets are literal.
FORBIDDEN: dict[str, list[str]] = {
    "python": [
        r"System\.out",
        r"Integer\.",
        r"Math\.",
        r"StringBuilder",
        r"\.equals\(",
        r"boolean\[",
        r"int\[\]",
        r"char\[\]",
        r"\+\+",
        r"===",
        r"console\.log",
        r"charCodeAt",
        r"BigInt",
        r"\bJava\b",
        r"\bJavaScript\b",
    ],
    "java": [
        r"print\(",
        r"len\(",
        r"ord\(",
        r"chr\(",
        r"elif",
        r"\bTrue\b",
        r"\bFalse\b",
        r"===",
        r"console\.log",
        r"charCodeAt",
        r"BigInt",
        r"\bPython\b",
        r"\bJavaScript\b",
    ],
    "javascript": [
        r"System\.out",
        r"Integer\.",
        r"StringBuilder",
        r"\.equals\(",
        r"boolean\[",
        r"int\[\]",
        r"char\[\]",
        r"print\(",
        r"len\(",
        r"ord\(",
        r"chr\(",
        r"elif",
        r"\bTrue\b",
        r"\bFalse\b",
        r"\bPython\b",
        r"\bJava\b(?!Script)",
    ],
}

# Extra markers for Basecamp OOP units. Applied on top of FORBIDDEN, including code.
OOP_EXTRA: dict[str, list[str]] = {
    "java": [r"\bself\b", r"__init__", r"\bdef\b", r"__str__", r"__repr__", r"__eq__"],
    "javascript": [r"\bself\b", r"__init__", r"\bdef\b", r"__str__", r"__repr__", r"__eq__"],
    "python": [r"this\.", r"\bextends\b", r"\bvoid\b", r"public class"],
}


# (language, regex matched against the visible text, why this hit is acceptable)
# A hit is ignored when an allowlist pattern for that language covers it.
ALLOWLIST: list[tuple[str, str, str]] = [
    # ("python", r"example", "why this mention cannot be rewritten"),
]


def filter_for_lang(text: str, lang: str | None) -> str:
    """Same rules as filterForLang in src/components/Markdown.tsx."""
    out: list[str] = []
    allowed: set[str] | None = None
    for line in text.split("\n"):
        trimmed = line.strip()
        if allowed is None:
            opened = re.match(r"^:::only\s+(.+)$", trimmed)
            if opened:
                allowed = {part.strip().lower() for part in opened.group(1).split(",") if part.strip()}
                continue
            out.append(line)
            continue
        if trimmed == ":::":
            allowed = None
            continue
        if lang is None or lang in allowed:
            out.append(line)
    return "\n".join(out)


def visible_text(text: str, lang: str) -> str:
    """Prose the learner reads: :::only applied, other-language fences removed,
    this language's fences ignored, table rows ignored."""
    text = filter_for_lang(text, lang)
    out: list[str] = []
    fence: str | None = None
    skip = False
    for line in text.split("\n"):
        stripped = line.lstrip()
        if stripped.startswith("```"):
            if fence is None:
                rest = stripped[3:].strip()
                tag = rest.split()[0].lower() if rest else ""
                fence = tag
                skip = tag in FENCE_LANG
                continue
            fence = None
            skip = False
            continue
        if fence is not None and skip:
            continue
        if stripped.startswith("|"):
            continue
        out.append(line)
    return "\n".join(out)


def allowed(lang: str, visible: str, start: int, end: int) -> bool:
    for alang, pat, _why in ALLOWLIST:
        if alang != lang:
            continue
        for m in re.finditer(pat, visible):
            if m.start() <= start and m.end() >= end:
                return True
    return False


def scan(label: str, text: str, lang: str, hits: list[str], extra: list[str] | None = None) -> None:
    visible = visible_text(text, lang)
    lines = visible.split("\n")
    for pat in FORBIDDEN[lang] + (extra or []):
        for m in re.finditer(pat, visible):
            if allowed(lang, visible, m.start(), m.end()):
                continue
            line_no = visible.count("\n", 0, m.start()) + 1
            snippet = lines[line_no - 1].strip()
            hits.append(f"{label} [{lang}] line {line_no}: {m.group(0)!r} in: {snippet[:200]}")


def scan_raw(label: str, text: str, lang: str, hits: list[str], extra: list[str] | None = None) -> None:
    """Like scan, but code fences stay in the text so samples are checked too."""
    lines = text.split("\n")
    for pat in FORBIDDEN[lang] + (extra or []):
        for m in re.finditer(pat, text):
            if allowed(lang, text, m.start(), m.end()):
                continue
            line_no = text.count("\n", 0, m.start()) + 1
            snippet = lines[line_no - 1].strip()
            hits.append(f"{label} [{lang}] line {line_no}: {m.group(0)!r} in: {snippet[:200]}")


def unit_blob(unit) -> str:
    parts = [unit.intro]
    for ex in unit.exercises:
        for key in ("prompt", "why", "code", "solution"):
            if ex.get(key):
                parts.append(str(ex[key]))
        parts.extend(ex.get("options") or [])
        parts.extend(ex.get("lines") or [])
        for alts in ex.get("blanks") or []:
            parts.extend(alts)
    return "\n".join(parts)


def main() -> int:
    hits: list[str] = []

    for n in range(1, 7):
        path = os.path.join(ROOT, "src", "content", "docs", f"phase{n}.md")
        with open(path, encoding="utf-8") as f:
            doc = f.read()
        for lang in LANGS:
            scan(os.path.relpath(path, ROOT), doc, lang, hits)

    with open(os.path.join(ROOT, "src", "content", "phases.json"), encoding="utf-8") as f:
        phases = json.load(f)
    for phase in phases:
        for lang in LANGS:
            questions = [q for q in phase["quiz"] if not q.get("lang") or q["lang"] == lang]
            if len(questions) != 5:
                hits.append(f"phases.json phase {phase['id']} [{lang}]: {len(questions)} questions, want 5")
            blob = "\n".join(
                "\n".join([q["q"], *q["options"], q["why"]]) for q in questions
            )
            scan(f"phases.json phase {phase['id']} quiz", blob, lang, hits)

    for n in range(1, 7):
        importlib.import_module(f"phase{n}")
    for p in core.REGISTRY:
        hints = core.normalize_hints(p.hints)
        for lang in LANGS:
            scan(f"{p.id} {p.title} hints", "\n".join(hints[lang]), lang, hits)
            scan(f"{p.id} {p.title} statement", p.statement, lang, hits)

    sys.path.insert(0, os.path.join(HERE, "basecamp"))
    import bc  # noqa: E402

    oop_n = 0
    for lang in LANGS:
        importlib.import_module(f"{lang}_oop")
    for lang in LANGS:
        for unit in bc.UNITS[lang]:
            if unit.section != "oop":
                continue
            oop_n += 1
            scan_raw(f"basecamp {unit.id} {unit.title}", unit_blob(unit), lang, hits, OOP_EXTRA[lang])

    if hits:
        print(f"{len(hits)} language-marker hit(s):")
        for h in hits:
            print(h)
        return 1
    print(f"language lint ok ({len(core.REGISTRY)} problems, 6 guides, 6 quizzes, {oop_n} OOP units)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
