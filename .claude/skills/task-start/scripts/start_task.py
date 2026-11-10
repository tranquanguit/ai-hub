#!/usr/bin/env python3
"""Create a task folder and point the session at it (task-start skill; DESIGN.md#fixed-pipelines).

  start_task.py --slug q1-plan --type phase-plan --goal "..." --criterion "..." [--criterion ...]
                [--input inputs/x.md] [--role founder] [--date YYYY-MM-DD]
  start_task.py log "<intent>" "<action>" "<observation>" [--scripted|--question|--rework]

`log` appends one ReAct line to the open task's LEDGER.md (DESIGN.md#react-steps). Tags:
[scripted] a script did the step, [reasoned] the model did it, [question] the user was asked,
[rework] a step was redone after a failed check. task-close counts these tags for the ledger.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path


def find_root() -> Path:
    if os.environ.get("LUNO_ROOT"):
        return Path(os.environ["LUNO_ROOT"])
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / "AGENTS.md").exists() and (parent / ".claude").exists():
            return parent
    return Path.cwd()


ROOT = find_root()
STATE = ROOT / ".claude" / "state"


def session_role() -> str | None:
    if os.environ.get("LUNO_ROLE"):
        return os.environ["LUNO_ROLE"]
    sid = os.environ.get("CLAUDE_CODE_SESSION_ID") or os.environ.get("CLAUDE_SESSION_ID")
    f = STATE / "roles" / str(sid)
    return f.read_text().strip() if sid and f.exists() else None


def words(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9à-ỹ]{4,}", s.lower())}


def relevant(goal: str, ttype: str) -> dict:
    kw = words(goal + " " + ttype.replace("-", " "))
    skills = []
    # v1.1.0: also list skill drafts (marked), so a task run on a draft is recorded (trajectory 2026-11-10-ops-review-w45)
    for base, mark in (("skills", ""), ("skill-drafts", " (draft)")):
        for sk in sorted((ROOT / ".claude" / base).glob("*/SKILL.md")):
            m = re.search(r"^description:\s*(.+)$", sk.read_text(), re.M)
            desc = m.group(1) if m else ""
            if sk.parent.name == ttype or len(kw & words(desc + " " + sk.parent.name.replace("-", " "))) >= 2:
                if sk.parent.name not in skills:
                    skills.append(sk.parent.name + mark)
    facts = []
    idx = ROOT / "memory" / "INDEX.md"
    if idx.exists():
        for line in idx.read_text().splitlines():
            if line.startswith("- `") and (ttype in line or len(kw & words(line)) >= 2):
                facts.append(line[2:].split("`")[1])
    episodes = []
    for e in sorted((ROOT / "memory" / "episodic").glob("*.md")):
        head = e.read_text()[:600]
        if f"task_type: {ttype}" in head:
            episodes.append(e.relative_to(ROOT).as_posix())
    return {"skills": skills, "facts": facts[:10], "episodes": episodes[-3:]}


def start(a) -> Path:
    role = a.role or session_role()
    if not role:
        raise SystemExit("Role not confirmed: ask the user, then run tools/set_role.py <role> (RULES R17).")
    slug = re.sub(r"[^a-z0-9-]+", "-", a.slug.lower()).strip("-")
    tid = f"{a.date or date.today().isoformat()}-{slug}"
    d = ROOT / "tasks" / tid
    if d.exists():
        raise SystemExit(f"task exists: tasks/{tid}")
    (d / "evidence").mkdir(parents=True)
    rel = relevant(a.goal, a.type)
    crit = "\n".join(f"- [ ] {c}" for c in a.criterion) or "- [ ] (define at least one checkable criterion)"
    inputs = "\n".join(f"- `{i}`" for i in a.input) or "- (none)"
    (d / "TASK.md").write_text(
        f"---\ntask: {tid}\ntask_type: {a.type}\nrole: {role}\nstatus: open\ncreated: {date.today().isoformat()}\n"
        f"rework_count: 0\nskills: {json.dumps([x.split(' ')[0] for x in rel['skills']])}\n---\n"
        f"# {a.goal}\n\n## Scope\n{a.scope or 'As stated in the goal; anything else needs the user.'}\n\n"
        f"## Inputs\n{inputs}\n\n## Done-criteria (each needs a file in evidence/)\n{crit}\n\n"
        f"## Relevant skills\n" + ("\n".join(f"- {s}" for s in rel["skills"]) or "- none found: candidate for skill-forge") +
        "\n\n## Relevant facts (memory/INDEX.md)\n" + ("\n".join(f"- `{f}`" for f in rel["facts"]) or "- none") +
        "\n\n## Past episodes of this task type\n" + ("\n".join(f"- {e}" for e in rel["episodes"]) or "- none") + "\n",
        encoding="utf-8")
    (d / "LEDGER.md").write_text(f"# LEDGER {tid}\n\nFormat: `- time [tag] intent -> action -> observation`\n\n")
    STATE.mkdir(parents=True, exist_ok=True)
    (STATE / "current_task").write_text(f"tasks/{tid}")
    return d


def log_step(a) -> str:
    p = STATE / "current_task"
    if not p.exists():
        raise SystemExit("no open task")
    d = ROOT / p.read_text().strip()
    tag = "scripted" if a.scripted else "question" if a.question else "rework" if a.rework else "reasoned"
    line = f"- {datetime.now(timezone.utc).strftime('%H:%M:%S')} [{tag}] {a.intent} -> {a.action} -> {a.observation}\n"
    with (d / "LEDGER.md").open("a", encoding="utf-8") as fh:
        fh.write(line)
    if a.rework:
        t = (d / "TASK.md").read_text()
        n = int(re.search(r"rework_count: (\d+)", t).group(1)) + 1
        (d / "TASK.md").write_text(re.sub(r"rework_count: \d+", f"rework_count: {n}", t, count=1))
    return line


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] == "log":
        ap = argparse.ArgumentParser()
        ap.add_argument("cmd"); ap.add_argument("intent"); ap.add_argument("action"); ap.add_argument("observation")
        g = ap.add_mutually_exclusive_group()
        g.add_argument("--scripted", action="store_true"); g.add_argument("--question", action="store_true")
        g.add_argument("--rework", action="store_true")
        print(log_step(ap.parse_args(argv)), end="")
        return 0
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True); ap.add_argument("--type", required=True); ap.add_argument("--goal", required=True)
    ap.add_argument("--criterion", action="append", default=[]); ap.add_argument("--input", action="append", default=[])
    ap.add_argument("--scope"); ap.add_argument("--role"); ap.add_argument("--date")
    d = start(ap.parse_args(argv))
    print(f"created {d.relative_to(ROOT)}/ (TASK.md, LEDGER.md, evidence/); current task set")
    print((d / "TASK.md").read_text().split("## Relevant skills")[1])
    return 0


if __name__ == "__main__":
    sys.exit(main())
