#!/usr/bin/env python3
"""Stop: block stopping ONCE when the open task has no evidence or no reflection (RULES R1).

Never loops: honours stop_hook_active (doc:cc-hooks) and keeps a per-session, per-task once-flag.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402


def missing_for(task: Path) -> list[str]:
    missing = []
    ev = [p for p in (task / "evidence").glob("*") if p.is_file() and p.stat().st_size > 0] if (task / "evidence").exists() else []
    ledger = (task / "LEDGER.md").read_text() if (task / "LEDGER.md").exists() else ""
    if not ev:
        missing.append(f"verification output in {task.relative_to(c.ROOT).as_posix()}/evidence/")
    elif not any(p.name in ledger for p in ev):
        missing.append("a LEDGER.md line that references the evidence file")
    epi = c.ROOT / "memory" / "episodic"
    refl = (epi / f"{task.name}.md").exists() or any(
        c.frontmatter(p).get("task") == task.name for p in epi.glob("*.md"))
    if not refl:
        missing.append("a reflection in memory/episodic/ (run the reflect skill)")
    return missing


def main() -> int:
    data = c.read_input()
    if data.get("stop_hook_active"):
        return 0
    task = c.current_task()
    if not task:
        return 0
    sid = str(data.get("session_id") or "nosession")
    flag = c.STATE / "stop_once" / f"{sid}-{task.name}"
    if flag.exists():
        return 0
    missing = missing_for(task)
    if not missing:
        return 0
    flag.parent.mkdir(parents=True, exist_ok=True)
    flag.write_text(c.now())
    reason = (f"Task {task.name} is still open and is missing: " + "; ".join(missing) +
              ". Finish with the task-close skill, or if the user wants to pause, say so and stop again.")
    print(json.dumps({"decision": "block", "reason": reason}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
