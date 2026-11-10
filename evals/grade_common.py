"""Shared grading helpers for golden tasks (deterministic first; 2310.06770, 2306.05685).

A golden grader receives the eval workspace (a throwaway worktree where a fresh headless session
ran) and returns {passed, score, checks:[{name, ok, info}]}. Checker logic is a FROZEN copy in
evals/golden/<task>/grader_lib/, so a skill change cannot weaken its own grader (R6).
"""
from __future__ import annotations

import importlib.util
import io
import re
from contextlib import redirect_stdout
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def find_task(ws: Path, task_type: str) -> Path | None:
    """Newest task folder of this type created in the workspace."""
    cands = []
    for t in (ws / "tasks").glob("*/TASK.md"):
        if re.search(rf"^task_type:\s*{re.escape(task_type)}\s*$", t.read_text(), re.M):
            cands.append(t.parent)
    return max(cands, key=lambda p: p.stat().st_mtime) if cands else None


def pipeline_checks(task: Path | None, deliverable_name: str) -> tuple[list[dict], Path | None]:
    checks = []
    checks.append({"name": "task_folder_created", "ok": task is not None, "info": "task-start was used"})
    if task is None:
        return checks, None
    deliv = next(iter(sorted(task.glob(f"**/{deliverable_name}"))), None)
    checks.append({"name": "deliverable_exists", "ok": deliv is not None, "info": deliverable_name})
    ev = [p for p in (task / "evidence").glob("**/*") if p.is_file()] if (task / "evidence").exists() else []
    checks.append({"name": "evidence_saved", "ok": bool(ev), "info": f"{len(ev)} evidence files"})
    led = (task / "LEDGER.md").read_text() if (task / "LEDGER.md").exists() else ""
    checks.append({"name": "scripted_step_logged", "ok": "[scripted]" in led, "info": "deterministic step ran as a script"})
    return checks, deliv


def run_checker(fn, *args) -> tuple[list[dict], str]:
    buf = io.StringIO()
    with redirect_stdout(buf):
        res = fn(*args)
    return [{"name": f"content:{n}", "ok": bool(ok), "info": info} for n, ok, info in res], buf.getvalue()


def summarize(checks: list[dict], critical_prefixes=("task_folder", "deliverable", "content:")) -> dict:
    score = round(sum(c["ok"] for c in checks) / len(checks), 3) if checks else 0.0
    critical_ok = all(c["ok"] for c in checks if c["name"].startswith(critical_prefixes))
    return {"passed": critical_ok, "score": score, "checks": checks}
