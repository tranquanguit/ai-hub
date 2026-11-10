#!/usr/bin/env python3
"""SessionEnd: record tokens/turns/tool calls from the transcript (tools/session_stats.py).

SessionEnd has a 1.5 s default timeout (doc:cc-hooks); settings.json raises it for this hook.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402


def main() -> int:
    data = c.read_input()
    tp = data.get("transcript_path")
    if not tp:
        return 0
    task = c.current_task()
    cmd = [sys.executable, str(c.ROOT / "tools" / "session_stats.py"), "--transcript", tp,
           "--session", str(data.get("session_id", "")), "--reason", str(data.get("reason", ""))]
    if task:
        cmd += ["--task", task.name]
    r = subprocess.run(cmd, cwd=c.ROOT, capture_output=True, text=True, timeout=25)
    if r.returncode:
        print(r.stderr[-300:], file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
