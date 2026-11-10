#!/usr/bin/env python3
"""Update a skill's stats.json (never loaded into context). RULES R7 tracking.

  python tools/skill_stats.py record <skill> --result pass|fail [--failure TEXT]
         [--scripted "step1,step2"] [--reasoned "stepA,stepB"]
  python tools/skill_stats.py show [<skill>]
  python tools/skill_stats.py candidates      # reasoned steps seen >= 3 times -> script candidates (R7)

stats.json keys: runs, passes, failures, last_failure, version, last_run, scripted_steps,
reasoned_steps, step_counts {reasoned step name: count}.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".claude" / "skills"
DEFAULT = {"runs": 0, "passes": 0, "failures": 0, "last_failure": None, "version": "0.1.0", "last_run": None,
           "scripted_steps": 0, "reasoned_steps": 0, "step_counts": {}}


def load(skill: str) -> tuple[Path, dict]:
    p = SKILLS / skill / "stats.json"
    if not p.parent.exists():
        raise SystemExit(f"unknown skill: {skill}")
    d = {**DEFAULT, **(json.loads(p.read_text()) if p.exists() else {})}
    return p, d


def split(s: str | None) -> list[str]:
    return [x.strip() for x in (s or "").split(",") if x.strip()]


def record(skill: str, result: str, failure: str | None = None, scripted: str = "", reasoned: str = "") -> dict:
    p, d = load(skill)
    d["runs"] += 1
    if result == "pass":
        d["passes"] += 1
    else:
        d["failures"] += 1
        d["last_failure"] = {"at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "why": failure or "unspecified"}
    d["last_run"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    sc, rs = split(scripted), split(reasoned)
    d["scripted_steps"] += len(sc)
    d["reasoned_steps"] += len(rs)
    for s in rs:
        d["step_counts"][s] = d["step_counts"].get(s, 0) + 1
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
    return d


def candidates() -> list[tuple[str, str, int]]:
    out = []
    for p in sorted(SKILLS.glob("*/stats.json")):
        d = json.loads(p.read_text())
        for step, n in (d.get("step_counts") or {}).items():
            if n >= 3:
                out.append((p.parent.name, step, n))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    r = sp.add_parser("record")
    r.add_argument("skill"); r.add_argument("--result", choices=["pass", "fail"], required=True)
    r.add_argument("--failure"); r.add_argument("--scripted", default=""); r.add_argument("--reasoned", default="")
    s = sp.add_parser("show"); s.add_argument("skill", nargs="?")
    sp.add_parser("candidates")
    a = ap.parse_args(argv)
    if a.cmd == "record":
        d = record(a.skill, a.result, a.failure, a.scripted, a.reasoned)
        print(f"{a.skill}: runs={d['runs']} passes={d['passes']} failures={d['failures']} v{d['version']}")
    elif a.cmd == "show":
        for p in sorted(SKILLS.glob(f"{a.skill or '*'}/stats.json")):
            d = json.loads(p.read_text())
            print(f"{p.parent.name:<18} runs={d.get('runs')} pass={d.get('passes')} fail={d.get('failures')} "
                  f"v{d.get('version')} scripted={d.get('scripted_steps', 0)} reasoned={d.get('reasoned_steps', 0)}")
    else:
        c = candidates()
        for sk, st, n in c:
            print(f"script candidate (R7): {sk}: '{st}' reasoned {n} times")
        if not c:
            print("no script candidates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
