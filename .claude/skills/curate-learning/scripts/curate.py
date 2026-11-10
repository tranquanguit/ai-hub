#!/usr/bin/env python3
"""One curation pass (ACE curator, 2510.04618): plan -> apply rules -> index -> report.

  curate.py [--out tasks/<task>/evidence/curation.md] [--dry-run]

Rules live in tools/promote.py (verdict): add verified new facts, merge duplicates (helpful+1),
set conflicts aside (R4), reject self-assessed/unsourced/PII items (R2, R9, R15), defer skill
deltas to skill-forge. The report is the evidence that curation happened.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def find_root() -> Path:
    if os.environ.get("LUNO_ROOT"):
        return Path(os.environ["LUNO_ROOT"])
    for parent in Path(__file__).resolve().parents:
        if (parent / "AGENTS.md").exists() and (parent / ".claude").exists():
            return parent
    return Path.cwd()


ROOT = find_root()


def run(*args) -> str:
    return subprocess.run([sys.executable, str(ROOT / "tools" / "promote.py"), *args], capture_output=True, text=True,
                          cwd=ROOT).stdout


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    log = ROOT / "memory" / "curation-log.jsonl"
    before = len(log.read_text().splitlines()) if log.exists() else 0
    plan = run("plan")
    lines = ["# Curation report", "", "## Plan (before)", "```", plan.strip(), "```"]
    if not a.dry_run:
        run("auto")
        new = [json.loads(l) for l in (log.read_text().splitlines()[before:] if log.exists() else [])]
        lines += ["", "## Decisions", "", "| item | action | reason | fact |", "|---|---|---|---|"]
        lines += [f"| {r['item']} | {r['action']} | {r['reason']} | {r.get('fact', '')} |" for r in new]
        counts = {k: sum(1 for r in new if r["action"] == k) for k in ("add", "merge", "conflict", "reject")}
        lines += ["", "Totals: " + ", ".join(f"{k}={v}" for k, v in counts.items())]
        deferred = [l for l in plan.splitlines() if l.startswith("defer")]
        if deferred:
            lines += ["", "## Deferred to skill-forge / human", ""] + [f"- {l}" for l in deferred]
        lint = run("lint")
        lines += ["", "## Lint", "```", lint.strip(), "```"]
    report = "\n".join(lines) + "\n"
    print(report)
    if a.out:
        out = ROOT / a.out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
