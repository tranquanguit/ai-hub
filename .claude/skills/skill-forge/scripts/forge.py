#!/usr/bin/env python3
"""Create or update skills from real trajectories (Voyager 2305.16291, AWM 2409.07429).

  forge.py candidates                      what deserves a new or updated skill, with evidence
  forge.py draft <name> [--new]            copy the active skill to .claude/skill-drafts/<name>/ (or scaffold)
  forge.py changelog <name> --version X.Y.Z --why "..." --evidence PATH [--eval-before P --eval-after P]

Rules: draft a NEW skill when a task_type succeeded >= 2 times without its own skill; UPDATE a skill
for skill-delta inbox items and R7 script candidates. Activation goes through
`tools/promote.py skill <name> --eval <results.json>` (gates: validator, script tests, golden eval).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from collections import Counter
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
SKILLS = ROOT / ".claude" / "skills"
DRAFTS = ROOT / ".claude" / "skill-drafts"
TEMPLATE = """---
name: {name}
description: TODO what it does and when to use it (under 200 chars).
---
# {name}

## When to use
- TODO (and when not to)

## Inputs
- TODO

## Steps
1. TODO: numbered steps; deterministic steps call scripts/<x>.py

## Memory facts used
- TODO links to memory/semantic facts

## Verification
- TODO: a check whose output goes to tasks/<task>/evidence/

## Close
- Write the reflection with the reflect skill.
- `python3 tools/skill_stats.py record {name} --result pass|fail`
"""


def candidates() -> dict:
    out = {"new_skills": [], "skill_deltas": [], "script_candidates": []}
    led = ROOT / "metrics" / "ledger.jsonl"
    if led.exists():
        rows = [json.loads(l) for l in led.read_text().splitlines() if l.strip()]
        ok = Counter(r.get("task_type") for r in rows if r.get("verification_passed"))
        for t, n in ok.items():
            if n >= 2 and t and not (SKILLS / t).exists():
                tasks = [r["task"] for r in rows if r.get("task_type") == t and r.get("verification_passed")]
                out["new_skills"].append({"task_type": t, "successes": n, "trajectories": tasks})
    for p in sorted((ROOT / "memory" / "inbox").glob("*.md")):
        m = re.match(r"^---\n(.*?)\n---\n?(.*)$", p.read_text(), re.S)
        fm = yaml.safe_load(m.group(1)) if m else {}
        if fm.get("type") == "skill-delta":
            out["skill_deltas"].append({"item": p.relative_to(ROOT).as_posix(), "tags": fm.get("tags"),
                                        "claim": fm.get("claim"), "evidence": (fm.get("verification") or {}).get("evidence")})
    for st in sorted(SKILLS.glob("*/stats.json")):
        d = json.loads(st.read_text())
        for step, n in (d.get("step_counts") or {}).items():
            if n >= 3:
                out["script_candidates"].append({"skill": st.parent.name, "step": step, "times": n})
    return out


def draft(name: str, new: bool) -> Path:
    dst = DRAFTS / name
    if dst.exists():
        raise SystemExit(f"draft exists: {dst.relative_to(ROOT)}")
    if new:
        dst.mkdir(parents=True)
        (dst / "scripts").mkdir()
        (dst / "references").mkdir()
        (dst / "SKILL.md").write_text(TEMPLATE.format(name=name))
        (dst / "stats.json").write_text(json.dumps({"runs": 0, "passes": 0, "failures": 0, "last_failure": None,
                                                    "version": "0.1.0"}, indent=2) + "\n")
        (dst / "CHANGELOG.md").write_text(f"# {name} changelog\n")
    else:
        src = SKILLS / name
        if not src.exists():
            raise SystemExit(f"no active skill {name}; use --new")
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
    return dst


def changelog(a) -> int:
    d = DRAFTS / a.name
    if not d.exists():
        raise SystemExit("draft first")
    st = json.loads((d / "stats.json").read_text())
    st["version"] = a.version
    (d / "stats.json").write_text(json.dumps(st, indent=2) + "\n")
    entry = [f"\n## {a.version} — {date.today()}", f"- Why: {a.why}", f"- Trajectory evidence: {a.evidence}"]
    if a.eval_before:
        entry.append(f"- Eval before: {a.eval_before}")
    if a.eval_after:
        entry.append(f"- Eval after: {a.eval_after}")
    with (d / "CHANGELOG.md").open("a") as fh:
        fh.write("\n".join(entry) + "\n")
    print(f"{a.name} draft -> v{a.version}; CHANGELOG updated")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("candidates")
    p = sp.add_parser("draft"); p.add_argument("name"); p.add_argument("--new", action="store_true")
    p = sp.add_parser("changelog"); p.add_argument("name"); p.add_argument("--version", required=True)
    p.add_argument("--why", required=True); p.add_argument("--evidence", required=True)
    p.add_argument("--eval-before"); p.add_argument("--eval-after")
    a = ap.parse_args(argv)
    if a.cmd == "candidates":
        print(json.dumps(candidates(), indent=2, ensure_ascii=False))
        return 0
    if a.cmd == "draft":
        d = draft(a.name, a.new)
        print(f"draft at {d.relative_to(ROOT)}: edit as small deltas (R5), then changelog, eval, promote")
        return 0
    return changelog(a)


if __name__ == "__main__":
    sys.exit(main())
