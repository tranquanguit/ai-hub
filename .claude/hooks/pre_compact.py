#!/usr/bin/env python3
"""PreCompact: page working state out to the task LEDGER before compaction (DESIGN.md#compaction-ledger).

Stdout becomes instructions for the compaction summary (doc:cc-hooks, PreCompact output).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402


def changed_files() -> list[str]:
    try:
        out = subprocess.run(["git", "status", "--porcelain"], cwd=c.ROOT, capture_output=True, text=True, timeout=10).stdout
        return [l[3:] for l in out.splitlines()][:20]
    except Exception:
        return []


def main() -> int:
    data = c.read_input()
    task = c.current_task()
    if not task:
        print("No open task. Keep the user's latest request and any decisions made in the summary.")
        return 0
    ledger = task / "LEDGER.md"
    last = [l for l in ledger.read_text().splitlines() if l.startswith("- ")][-3:] if ledger.exists() else []
    files = changed_files()
    with ledger.open("a", encoding="utf-8") as fh:
        fh.write(f"\n### Compaction checkpoint {c.now()} ({data.get('trigger', '?')})\n")
        fh.write(f"- state: compaction; uncommitted files: {', '.join(files) or 'none'}\n")
    rel = task.relative_to(c.ROOT).as_posix()
    print(f"Keep in the summary: the open task is {rel} (read {rel}/TASK.md for goal and done-criteria). "
          f"Last ledger steps: {' | '.join(last) or 'none'}. Continue from {rel}/LEDGER.md after compaction.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
