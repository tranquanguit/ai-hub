#!/usr/bin/env python3
"""Prune proposals (the prune skill). Propose first; archive only what a human approved.

  python tools/prune.py propose [--today YYYY-MM-DD]   # writes metrics/prune-proposal.md
  python tools/prune.py apply --facts a,b --skills x   # archive approved items with reasons

Facts: not used or re-verified in 90 days, or harmful > helpful. Skills: no run in 60 days
(never-run skills count from their CHANGELOG creation date).
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import promote  # noqa: E402

FACT_DAYS, SKILL_DAYS = 90, 60


def _d(s) -> date | None:
    try:
        return date.fromisoformat(str(s)[:10])
    except Exception:
        return None


def propose(today: date) -> dict:
    out = {"facts": [], "skills": []}
    for slug, (p, f) in promote.facts().items():
        last = max([d for d in (_d(f.get("last_used")), _d(f.get("last_verified")), _d(f.get("created"))) if d], default=None)
        if int(f.get("harmful", 0)) > int(f.get("helpful", 0)):
            out["facts"].append((slug, f"harmful {f.get('harmful')} > helpful {f.get('helpful')}"))
        elif last and (today - last).days > FACT_DAYS:
            out["facts"].append((slug, f"not used or verified for {(today - last).days} days"))
    for st in sorted((ROOT / ".claude" / "skills").glob("*/stats.json")):
        d = json.loads(st.read_text())
        last = _d(d.get("last_run"))
        if not last:
            cl = st.parent / "CHANGELOG.md"
            m = re.search(r"20\d\d-\d\d-\d\d", cl.read_text()) if cl.exists() else None
            last = _d(m.group(0)) if m else None
        if last and (today - last).days > SKILL_DAYS:
            out["skills"].append((st.parent.name, f"no run for {(today - last).days} days"))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("propose"); p.add_argument("--today")
    p = sp.add_parser("apply"); p.add_argument("--facts", default=""); p.add_argument("--skills", default="")
    p.add_argument("--reason", default="approved prune proposal")
    a = ap.parse_args(argv)
    if a.cmd == "propose":
        today = _d(a.today) or date.today()
        prop = propose(today)
        lines = [f"# Prune proposal ({today})", "", "Approve by running `python3 tools/prune.py apply --facts ... --skills ...`.", "",
                 "## Facts"] + [f"- [ ] `{s}` — {why}" for s, why in prop["facts"]] + ["", "## Skills"] + \
                [f"- [ ] `{s}` — {why}" for s, why in prop["skills"]]
        if not prop["facts"] and not prop["skills"]:
            lines.append("\nNothing to prune.")
        (ROOT / "metrics" / "prune-proposal.md").write_text("\n".join(lines) + "\n")
        print("\n".join(lines))
        return 0
    for slug in [s for s in a.facts.split(",") if s]:
        promote.main(["archive", slug, "--reason", a.reason])
    for sk in [s for s in a.skills.split(",") if s]:
        src = ROOT / ".claude" / "skills" / sk
        dst = ROOT / ".claude" / "skills-archive" / sk
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        (dst / "ARCHIVED.md").write_text(f"Archived {date.today()}: {a.reason}\n")
        print(f"archived skill {sk}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
