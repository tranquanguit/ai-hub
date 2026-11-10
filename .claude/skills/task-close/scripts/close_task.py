#!/usr/bin/env python3
"""Close the current task: check evidence (R1), append metrics/ledger.jsonl, record skill stats.

  close_task.py --passed true|false [--skills a,b] [--tokens-in N --tokens-out N --cost USD --turns N]
                [--duration SEC] [--failure "why"]

Counts from LEDGER.md tags: [scripted] / [reasoned] steps, [question] lines, rework_count from TASK.md.
Token fields may be left empty; the SessionEnd hook backfills them from the transcript
(tools/session_stats.py) and headless runs pass them from `claude -p` JSON.
Exit 1 when evidence is missing or not referenced in LEDGER.md.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path


def find_root() -> Path:
    if os.environ.get("LUNO_ROOT"):
        return Path(os.environ["LUNO_ROOT"])
    for parent in Path(__file__).resolve().parents:
        if (parent / "AGENTS.md").exists() and (parent / ".claude").exists():
            return parent
    return Path.cwd()


ROOT = find_root()


def current() -> Path:
    p = ROOT / ".claude" / "state" / "current_task"
    if not p.exists():
        raise SystemExit("no current task")
    return ROOT / p.read_text().strip()


def fm(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    out = {}
    for line in (m.group(1).splitlines() if m else []):
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def evidence_ok(d: Path) -> tuple[bool, list[str], str]:
    ev = sorted(p.name for p in (d / "evidence").glob("*") if p.is_file() and p.stat().st_size > 0)
    led = (d / "LEDGER.md").read_text()
    if not ev:
        return False, ev, "evidence/ is empty"
    if not any(e in led for e in ev):
        return False, ev, "LEDGER.md does not reference any evidence file"
    return True, ev, ""


def counts(d: Path) -> dict:
    led = (d / "LEDGER.md").read_text()
    return {"scripted": len(re.findall(r"\[scripted\]", led)), "reasoned": len(re.findall(r"\[reasoned\]", led)),
            "questions": len(re.findall(r"\[question\]", led))}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--passed", choices=["true", "false"], required=True)
    ap.add_argument("--skills", default="")
    ap.add_argument("--tokens-in", type=int); ap.add_argument("--tokens-out", type=int)
    ap.add_argument("--cost", type=float); ap.add_argument("--turns", type=int); ap.add_argument("--duration", type=float)
    ap.add_argument("--failure", default="")
    ap.add_argument("--token-source", default="")
    a = ap.parse_args(argv)
    d = current()
    ok, ev, why = evidence_ok(d)
    if not ok:
        print(f"cannot close {d.name}: {why} (R1)")
        return 1
    t = (d / "TASK.md").read_text()
    meta = fm(t)
    c = counts(d)
    skills = [s for s in (a.skills or "").split(",") if s] or json.loads(meta.get("skills", "[]") or "[]")
    skills = sorted(set(skills) | {"task-start", "task-close"})
    args = [sys.executable, str(ROOT / "tools" / "metrics.py"), "append", "--task", d.name,
            "--task-type", meta.get("task_type", "?"), "--role", meta.get("role", "?"), "--skills-used", ",".join(skills),
            "--verification-passed", a.passed, "--rework-count", meta.get("rework_count", "0"),
            "--questions-asked", str(c["questions"]), "--scripted-steps", str(c["scripted"]),
            "--reasoned-steps", str(c["reasoned"]), "--date", date.today().isoformat()]
    for flag, v in (("--tokens-in", a.tokens_in), ("--tokens-out", a.tokens_out), ("--cost", a.cost),
                    ("--turns", a.turns), ("--duration", a.duration), ("--token-source", a.token_source)):
        if v not in (None, ""):
            args += [flag, str(v)]
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr)
        return 1
    for s in skills:
        if (ROOT / ".claude" / "skills" / s).exists():
            sargs = [sys.executable, str(ROOT / "tools" / "skill_stats.py"), "record", s,
                     "--result", "pass" if a.passed == "true" else "fail"]
            if a.passed != "true":
                sargs += ["--failure", a.failure or "verification failed"]
            subprocess.run(sargs, capture_output=True, text=True)
    (d / "TASK.md").write_text(re.sub(r"status: open", "status: closed", t, 1))
    with (d / "LEDGER.md").open("a") as fh:
        fh.write(f"- close [scripted] task-close -> metrics/ledger.jsonl appended -> passed={a.passed}, evidence={', '.join(ev)}\n")
    print(f"closed {d.name}: passed={a.passed} scripted={c['scripted']} reasoned={c['reasoned']} "
          f"questions={c['questions']} skills={','.join(skills)}")
    print("next: reflect skill (episodic note + inbox candidates)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
