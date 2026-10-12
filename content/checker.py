"""Python port of src/lib/checker.ts. Keep both in sync."""

import math


def _lines(text: str) -> list[str]:
    lines = [l.rstrip() for l in text.replace("\r\n", "\n").split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return lines


def _num(tok: str):
    try:
        v = float(tok)
        return v if math.isfinite(v) else None
    except ValueError:
        return None


def _tok_eq(a: str, b: str) -> bool:
    if a == b:
        return True
    if a.lower() in ("true", "false") and a.lower() == b.lower():
        return True
    x, y = _num(a), _num(b)
    if x is None or y is None:
        return False
    if "." not in a + b and "e" not in (a + b).lower():
        return False  # integers must match exactly
    return abs(x - y) <= 1e-5 * max(1.0, abs(y))


def check(expected: str, actual: str, strict: bool) -> bool:
    e, a = _lines(expected), _lines(actual)
    if len(e) != len(a):
        return False
    for le, la in zip(e, a):
        if le == la:
            continue
        if strict:
            return False
        te, ta = le.split(), la.split()
        if len(te) != len(ta) or not all(_tok_eq(y, x) for x, y in zip(te, ta)):
            return False
    return True
