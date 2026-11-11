#!/usr/bin/env python3
"""Learning metrics from metrics/ledger.jsonl (Phase 5).

  python tools/metrics.py                # report per task type and per ISO week
  python tools/metrics.py --worst        # the single worst metric (input to the improve skill)
  python tools/metrics.py append --task T --task-type X ... (used by task-close; see --help)

Targets: median tokens, turns and questions fall over time; first-time pass rate and
scripted-step ratio rise. Ledger fields: date, task, task_type, role, skills_used, tokens_in,
tokens_out, cost, turns, questions_asked, verification_passed, rework_count, duration,
scripted_steps, reasoned_steps, token_source.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "metrics" / "ledger.jsonl"
FIELDS = ["date", "task", "task_type", "role", "skills_used", "tokens_in", "tokens_out", "cost", "turns",
          "questions_asked", "verification_passed", "rework_count", "duration", "scripted_steps", "reasoned_steps",
          "token_source"]
TARGETS = {"first_pass_rate": 0.9, "rework_rate": 0.1, "scripted_ratio": 0.5, "questions_per_task": 0.5}


def rows() -> list[dict]:
    if not LEDGER.exists():
        return []
    return [json.loads(l) for l in LEDGER.read_text().splitlines() if l.strip()]


def week(d: str) -> str:
    y, w, _ = date.fromisoformat(d[:10]).isocalendar()
    return f"{y}-W{w:02d}"


def med(xs):
    xs = [x for x in xs if isinstance(x, (int, float))]
    return statistics.median(xs) if xs else None


def summarize(rs: list[dict]) -> dict:
    n = len(rs)
    sc = sum(r.get("scripted_steps") or 0 for r in rs)
    rsn = sum(r.get("reasoned_steps") or 0 for r in rs)
    tok = [((r.get("tokens_in") or 0) + (r.get("tokens_out") or 0)) or None for r in rs]
    return {
        "n": n,
        "median_tokens": med(tok),
        "median_turns": med([r.get("turns") for r in rs]),
        "questions": sum(r.get("questions_asked") or 0 for r in rs),
        "first_pass_rate": round(sum(1 for r in rs if r.get("verification_passed") and not r.get("rework_count")) / n, 2) if n else None,
        "rework_rate": round(sum(1 for r in rs if (r.get("rework_count") or 0) > 0) / n, 2) if n else None,
        "scripted_ratio": round(sc / (sc + rsn), 2) if sc + rsn else None,
        "median_cost": med([r.get("cost") for r in rs]),
    }


def fmt(v):
    if v is None:
        return "–"
    return f"{v:,.0f}" if isinstance(v, (int, float)) and v >= 100 else str(v)


def report() -> str:
    rs = rows()
    if not rs:
        return "metrics/ledger.jsonl is empty"
    out = ["# Metrics report", "", f"tasks: {len(rs)}  |  overall: " +
           ", ".join(f"{k}={fmt(v)}" for k, v in summarize(rs).items()), "",
           "## By task type", "", "| task_type | n | median tokens | median turns | questions | first-pass | rework | scripted ratio | median cost $ |",
           "|---|---|---|---|---|---|---|---|---|"]
    by_type = defaultdict(list)
    by_week = defaultdict(list)
    for r in rs:
        by_type[r.get("task_type", "?")].append(r)
        by_week[week(r["date"])].append(r)
    for t, g in sorted(by_type.items()):
        s = summarize(g)
        out.append(f"| {t} | {s['n']} | {fmt(s['median_tokens'])} | {fmt(s['median_turns'])} | {s['questions']} | "
                   f"{fmt(s['first_pass_rate'])} | {fmt(s['rework_rate'])} | {fmt(s['scripted_ratio'])} | {fmt(s['median_cost'])} |")
    out += ["", "## By week (trend: tokens/turns/questions should fall; pass rate and scripted ratio should rise)", "",
            "| week | n | median tokens | median turns | questions | first-pass | scripted ratio |", "|---|---|---|---|---|---|---|"]
    for w, g in sorted(by_week.items()):
        s = summarize(g)
        out.append(f"| {w} | {s['n']} | {fmt(s['median_tokens'])} | {fmt(s['median_turns'])} | {s['questions']} | "
                   f"{fmt(s['first_pass_rate'])} | {fmt(s['scripted_ratio'])} |")
    evals = sorted(p for p in (ROOT / "evals" / "runs").glob("*/*/results.json") if not (p.parent / "INVALID.md").exists())
    if evals:
        out += ["", "## Cold-start evals (fresh headless sessions; the cleanest per-task numbers)", "",
                "| run | task | pass | tokens | cost $ | turns | rework | questions |", "|---|---|---|---|---|---|---|---|"]
        for p in evals:
            for r in json.loads(p.read_text())["results"]:
                tok = (r.get("tokens_in") or 0) + (r.get("tokens_out") or 0)
                out.append(f"| {p.parent.name} | {r['task']} | {'PASS' if r['passed'] else 'FAIL'} | {tok:,} | "
                           f"{round(r['cost_usd'], 3) if r.get('cost_usd') is not None else '–'} | {r.get('turns')} | "
                           f"{r.get('rework', '–')} | {r.get('questions_asked')} |")
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import skill_stats
        c = skill_stats.candidates()
        if c:
            out += ["", "## Script candidates (R7)", ""] + [f"- {sk}: '{st}' reasoned {n}×" for sk, st, n in c]
    except Exception:
        pass
    return "\n".join(out)


def worst() -> dict:
    rs = rows()
    if not rs:
        return {"metric": None, "why": "no data"}
    s = summarize(rs)
    gaps = []
    if s["first_pass_rate"] is not None:
        gaps.append(("first_pass_rate", max(0, TARGETS["first_pass_rate"] - s["first_pass_rate"]) / TARGETS["first_pass_rate"]))
    if s["rework_rate"] is not None:
        gaps.append(("rework_rate", max(0, s["rework_rate"] - TARGETS["rework_rate"]) / (1 - TARGETS["rework_rate"])))
    if s["scripted_ratio"] is not None:
        gaps.append(("scripted_ratio", max(0, TARGETS["scripted_ratio"] - s["scripted_ratio"]) / TARGETS["scripted_ratio"]))
    q = s["questions"] / s["n"]
    gaps.append(("questions_per_task", max(0, q - TARGETS["questions_per_task"]) / max(q, 1)))
    by_type = defaultdict(list)
    for r in rs:
        by_type[r.get("task_type")].append(r)
    tok = {t: summarize(g)["median_tokens"] or 0 for t, g in by_type.items()}
    name, gap = max(gaps, key=lambda g: g[1])
    if gap == 0:
        t = max(tok, key=tok.get)
        return {"metric": "median_tokens", "task_type": t, "value": tok[t],
                "why": "all rate targets met; the costliest task type is the next target"}
    return {"metric": name, "gap": round(gap, 2), "value": s[name] if name in s else q, "target": TARGETS[name]}


def append(a) -> dict:
    row = {k: getattr(a, k, None) for k in FIELDS}
    row["date"] = row["date"] or date.today().isoformat()
    row["skills_used"] = [s for s in (a.skills_used or "").split(",") if s]
    row["verification_passed"] = a.verification_passed == "true"
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    existing = [r for r in rows() if r.get("task") != row["task"]]
    if len(existing) != len(rows()):
        LEDGER.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in existing))
    with LEDGER.open("a") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] == "append":
        ap = argparse.ArgumentParser()
        ap.add_argument("cmd")
        for f in FIELDS:
            t = float if f in ("cost", "duration") else int if f in ("tokens_in", "tokens_out", "turns", "questions_asked",
                                                                        "rework_count", "scripted_steps", "reasoned_steps") else str
            ap.add_argument(f"--{f.replace('_', '-')}", dest=f, type=t)
        a = ap.parse_args(argv)
        print(json.dumps(append(a), ensure_ascii=False))
        return 0
    if "--worst" in argv:
        print(json.dumps(worst()))
        return 0
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
