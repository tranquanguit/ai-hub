#!/usr/bin/env python3
"""Episodic reflection for the current task (Reflexion 2303.11366, ExpeL 2308.10144).

  reflect.py new                      write memory/episodic/<task>.md template, pre-filled with facts
  reflect.py candidate --key K --claim C [--value V] --source S --kind test|tool|eval|human|self
             --evidence PATH [--tags a,b] [--type fact|skill-delta|question] [--confidence high]
                                      write one inbox candidate (memory/inbox/) in the promote format
  reflect.py finish                   check the note has no TODO left, mark task done, clear pointer
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

import yaml


def find_root() -> Path:
    if os.environ.get("LUNO_ROOT"):
        return Path(os.environ["LUNO_ROOT"])
    for parent in Path(__file__).resolve().parents:
        if (parent / "AGENTS.md").exists() and (parent / ".claude").exists():
            return parent
    return Path.cwd()


ROOT = find_root()
SECTIONS = ["What worked", "What failed", "Root cause", "Tokens and turns", "Questions I had to ask",
            "Candidate facts", "Candidate skill changes"]


def current() -> Path:
    p = ROOT / ".claude" / "state" / "current_task"
    if not p.exists():
        raise SystemExit("no current task")
    return ROOT / p.read_text().strip()


def fm(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    return yaml.safe_load(m.group(1)) if m else {}


def cmd_new(_a) -> int:
    d = current()
    meta = fm((d / "TASK.md").read_text())
    led = (d / "LEDGER.md").read_text()
    tags = {t: len(re.findall(rf"\[{t}\]", led)) for t in ("scripted", "reasoned", "question", "rework")}
    row = {}
    lp = ROOT / "metrics" / "ledger.jsonl"
    if lp.exists():
        for l in lp.read_text().splitlines():
            r = json.loads(l)
            if r.get("task") == d.name:
                row = r
    ev = sorted(p.name for p in (d / "evidence").glob("*"))
    questions = [l for l in led.splitlines() if "[question]" in l]
    out = ROOT / "memory" / "episodic" / f"{d.name}.md"
    if out.exists():
        print(f"exists: {out.relative_to(ROOT)}")
        return 0
    body = (f"---\ntask: {d.name}\ntask_type: {meta.get('task_type')}\nrole: {meta.get('role')}\ndate: {date.today()}\n"
            f"verification_passed: {row.get('verification_passed')}\nskills: {json.dumps(row.get('skills_used', []))}\n---\n"
            f"# Reflection: {d.name}\n\n"
            "## What worked\nTODO: concrete steps or scripts that produced a verified result (cite evidence/ files).\n\n"
            "## What failed\nTODO: checks that failed, rework, wrong assumptions. Write 'nothing' if nothing failed.\n\n"
            "## Root cause\nTODO: why it failed or why it was slow (missing fact? unclear skill step? no script?).\n\n"
            f"## Tokens and turns\nsteps: scripted {tags['scripted']}, reasoned {tags['reasoned']}, rework {tags['rework']}; "
            f"tokens_in={row.get('tokens_in')}, tokens_out={row.get('tokens_out')}, cost={row.get('cost')}, "
            f"turns={row.get('turns')} (empty = backfilled at SessionEnd)\n\n"
            "## Questions I had to ask\n" + ("\n".join(f"- {q.split('] ', 1)[-1]}" for q in questions) or "- none") +
            "\nTODO: for each question, should the repo have known the answer? If yes, add a candidate below.\n\n"
            "## Candidate facts\nTODO: list inbox files written with `reflect.py candidate` (each needs source + external verification).\n\n"
            "## Candidate skill changes\nTODO: concrete deltas (add step / script a repeated step / fix wording) as type: skill-delta candidates.\n\n"
            f"Evidence: {', '.join('tasks/' + d.name + '/evidence/' + e for e in ev)}\n")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}: fill every TODO, then `reflect.py finish`")
    return 0


def cmd_candidate(a) -> int:
    d = current()
    slug = re.sub(r"[^a-z0-9]+", "-", a.key.lower()).strip("-")[:60]
    p = ROOT / "memory" / "inbox" / f"{date.today()}-{slug}.md"
    i = 2
    while p.exists():
        p = p.with_name(f"{date.today()}-{slug}-{i}.md")
        i += 1
    item = {"type": a.type, "key": a.key, "claim": a.claim, "value": a.value, "source": a.source,
            "confidence": a.confidence, "tags": [t for t in a.tags.split(",") if t], "task": d.name,
            "verification": {"kind": a.kind, "evidence": a.evidence}, "created": str(date.today())}
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("---\n" + yaml.safe_dump(item, allow_unicode=True, sort_keys=False) + "---\n" + (a.detail or a.claim) + "\n",
                 encoding="utf-8")
    print(f"inbox: {p.relative_to(ROOT)}")
    return 0


def cmd_finish(_a) -> int:
    d = current()
    note = ROOT / "memory" / "episodic" / f"{d.name}.md"
    if not note.exists():
        print("no reflection yet: run `reflect.py new`")
        return 1
    text = note.read_text()
    todo = [s for s in SECTIONS if re.search(rf"## {s}[^\n]*\n(?:(?!## ).)*TODO", text, re.S)]
    missing = [s for s in SECTIONS if f"## {s}" not in text]
    if todo or missing:
        print(f"reflection incomplete: TODO in {todo}, missing {missing}")
        return 1
    t = (d / "TASK.md").read_text()
    (d / "TASK.md").write_text(re.sub(r"status: (open|closed)", "status: done", t, 1))
    (ROOT / ".claude" / "state" / "current_task").unlink()
    print(f"task {d.name} done; next: curate-learning")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("new").set_defaults(f=cmd_new)
    sp.add_parser("finish").set_defaults(f=cmd_finish)
    c = sp.add_parser("candidate")
    c.add_argument("--key", required=True); c.add_argument("--claim", required=True); c.add_argument("--value")
    c.add_argument("--source", required=True); c.add_argument("--kind", required=True,
                                                              choices=["test", "tool", "eval", "human", "self"])
    c.add_argument("--evidence", default=""); c.add_argument("--tags", default="")
    c.add_argument("--type", default="fact", choices=["fact", "skill-delta", "question"])
    c.add_argument("--confidence", default="medium", choices=["high", "medium", "low", "assumption"])
    c.add_argument("--detail", default="")
    c.set_defaults(f=cmd_candidate)
    a = ap.parse_args(argv)
    return a.f(a)


if __name__ == "__main__":
    sys.exit(main())
