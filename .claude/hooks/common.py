"""Shared helpers for LunoBeau hooks. Hooks run outside the model and cost no tokens (DESIGN.md#hooks-enforce-rules).

Hook I/O follows doc:cc-hooks: JSON on stdin; PreToolUse answers with
hookSpecificOutput.permissionDecision; Stop answers with decision/reason.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2]).resolve()
STATE = ROOT / ".claude" / "state"
ROLES_FILE = ROOT / "canon" / "roles" / "ROLES.json"
INCIDENTS = ROOT / "incidents" / "INCIDENTS.md"


def read_input() -> dict:
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


# ---------- roles ----------
def roles_config() -> dict:
    try:
        return json.loads(ROLES_FILE.read_text())
    except Exception:
        return {"roles": {}}


def session_role(session_id: str | None) -> str | None:
    """Role for this session: env LUNO_ROLE (headless evals) > per-session state file."""
    env = os.environ.get("LUNO_ROLE")
    if env:
        return env
    if session_id:
        p = STATE / "roles" / f"{session_id}"
        if p.exists():
            return p.read_text().strip() or None
    return None


# ---------- tasks ----------
def frontmatter(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return {}
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    out = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                out[k.strip()] = v.strip().strip("'\"")
    return out


def current_task() -> Path | None:
    """The task this checkout is working on (pointer written by task-start, cleared by reflect).
    Lifecycle: open -> closed (task-close, evidence saved) -> done (reflect, episodic note written)."""
    p = STATE / "current_task"
    if p.exists():
        d = ROOT / p.read_text().strip()
        if (d / "TASK.md").exists() and frontmatter(d / "TASK.md").get("status", "open") in ("open", "closed"):
            return d
    return None


def task_of_path(rel: str) -> Path | None:
    m = re.match(r"tasks/([^/]+)/", rel)
    return ROOT / "tasks" / m.group(1) if m else None


# ---------- paths ----------
def rel_path(p: str, cwd: str | None = None) -> str | None:
    """Repo-relative POSIX path, or None when outside the repo."""
    if not p:
        return None
    base = Path(cwd) if cwd else ROOT
    try:
        full = (base / os.path.expanduser(p)).resolve()
        return full.relative_to(ROOT).as_posix()
    except Exception:
        return None


def log_incident(kind: str, detail: str, session_id: str | None, role: str | None) -> None:
    """Append an incident (never the offending content itself). Admin sees it first at SessionStart."""
    INCIDENTS.parent.mkdir(parents=True, exist_ok=True)
    if not INCIDENTS.exists():
        INCIDENTS.write_text("# Incidents\n\nAppended by hooks. Admin reviews and changes `open` to `resolved: <note>`.\n\n")
    detail = detail.replace("\n", " ")[:240]
    with INCIDENTS.open("a", encoding="utf-8") as fh:
        fh.write(f"- {now()} | open | {kind} | role={role or 'unset'} | session={str(session_id)[:8]} | {detail}\n")


def open_incidents() -> int:
    if not INCIDENTS.exists():
        return 0
    return sum(1 for l in INCIDENTS.read_text().splitlines() if l.startswith("- ") and "| open |" in l)
