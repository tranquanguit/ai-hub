#!/usr/bin/env python3
"""Append one self-improvement attempt to metrics/IMPROVEMENTS.md (R6, R14).

  log_attempt.py --title T --metric M --hypothesis H --change C --before B --after A
                 --decision kept|reverted [--evidence PATH ...] [--rules-change]
"""
from __future__ import annotations

import argparse
import os
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


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    for f in ("title", "metric", "hypothesis", "change", "before", "after"):
        ap.add_argument(f"--{f}", required=True)
    ap.add_argument("--decision", choices=["kept", "reverted"], required=True)
    ap.add_argument("--evidence", action="append", default=[])
    ap.add_argument("--rules-change", action="store_true")
    a = ap.parse_args(argv)
    p = ROOT / "metrics" / "IMPROVEMENTS.md"
    if not p.exists():
        p.write_text("# Improvements log\n\nEvery self-improvement attempt (R6) and every RULES.md change (R14).\n")
    entry = (f"\n## {date.today()} — {a.title}\n- Metric: {a.metric}\n- Hypothesis: {a.hypothesis}\n- Change: {a.change}\n"
             f"- Eval before: {a.before}\n- Eval after: {a.after}\n- Decision: **{a.decision}**\n"
             + (f"- Evidence: {', '.join(a.evidence)}\n" if a.evidence else "")
             + ("- Type: RULES.md change (R14)\n" if a.rules_change else ""))
    with p.open("a", encoding="utf-8") as fh:
        fh.write(entry)
    print(entry.strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
