#!/usr/bin/env python3
"""SessionStart: at most 5 lines of dynamic status, phrased as facts (doc:cc-hooks "Add context").

Dynamic text lives here, never in CLAUDE.md, so CLAUDE.md stays byte-stable for the prompt cache
(DESIGN.md#small-hot-context). Plain stdout from SessionStart is added to Claude's context.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402


def failing_evals() -> list[str]:
    runs = sorted((c.ROOT / "evals" / "runs").glob("*/results.json"))
    if not runs:
        return []
    try:
        res = json.loads(runs[-1].read_text())
        return [r["task"] for r in res.get("results", []) if not r.get("passed")]
    except Exception:
        return []


def status_lines(data: dict) -> list[str]:
    sid = data.get("session_id")
    lines = []
    inc = c.open_incidents()
    if inc:
        lines.append(f"ADMIN ALERT: {inc} open incident(s) in incidents/INCIDENTS.md; tell the user at the start of the reply.")
    role = c.session_role(sid)
    if role:
        lines.append(f"Session role: {role} (canon: canon/roles/{role}.md).")
    else:
        lines.append("Session role: not confirmed yet (data/ is closed until it is set with tools/set_role.py).")
    inbox = len([p for p in (c.ROOT / "memory" / "inbox").glob("*.md")])
    conflicts = len([p for p in (c.ROOT / "memory" / "conflicts").glob("*.md")])
    lines.append(f"Memory queue: {inbox} inbox item(s), {conflicts} open conflict(s).")
    fails = failing_evals()
    if fails:
        lines.append(f"Failing golden evals in the last run: {', '.join(fails)}.")
    t = c.current_task()
    if t:
        lines.append(f"Open task: {t.relative_to(c.ROOT).as_posix()}/TASK.md.")
    return lines[:5]


def main() -> int:
    data = c.read_input()
    try:
        print("\n".join(status_lines(data)))
    except Exception as e:
        print(f"session_start hook error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
