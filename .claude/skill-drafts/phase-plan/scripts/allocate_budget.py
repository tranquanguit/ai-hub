#!/usr/bin/env python3
"""Deterministic budget allocation for a phase plan (the arithmetic is scripted, not reasoned; R7).

  allocate_budget.py <brief.md> [--json out.json] [--md out.md]

Reads the ```yaml params block in the brief: total_budget_vnd, reserve_pct, months, month_weights,
channels {cpa, roas, weight, min_share, max_share}, regions, audiences_last_q.
Rule: working budget = total * (1 - reserve). Channel score = roas * weight; shares proportional to
score, clamped to [min_share, max_share] with the excess redistributed (water-filling). Amounts are
rounded to 1,000 VND and the rounding remainder goes to the largest channel, so the table sums
exactly to the total. Expected orders = amount / cpa; expected revenue = amount * roas.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml


def params(brief: Path) -> dict:
    m = re.search(r"```yaml\n(.*?)```", brief.read_text(encoding="utf-8"), re.S)
    if not m:
        raise SystemExit("brief has no ```yaml params block")
    return yaml.safe_load(m.group(1))


def shares(ch: dict) -> dict[str, float]:
    score = {k: v["roas"] * v.get("weight", 1.0) for k, v in ch.items()}
    fixed: dict[str, float] = {}
    for _ in range(len(ch) + 1):
        free = [k for k in ch if k not in fixed]
        left = 1.0 - sum(fixed.values())
        tot = sum(score[k] for k in free) or 1
        prop = {k: left * score[k] / tot for k in free}
        viol = {k: (ch[k].get("min_share", 0) if p < ch[k].get("min_share", 0) else ch[k].get("max_share", 1))
                for k, p in prop.items() if p < ch[k].get("min_share", 0) or p > ch[k].get("max_share", 1)}
        if not viol:
            return {**fixed, **prop}
        fixed.update(viol)
    return {**fixed}


def allocate(p: dict) -> dict:
    total = int(p["total_budget_vnd"])
    reserve = int(round(total * p.get("reserve_pct", 0) / 1000.0)) * 1000
    work = total - reserve
    sh = shares(p["channels"])
    amt = {k: int(work * s / 1000) * 1000 for k, s in sh.items()}
    amt[max(amt, key=amt.get)] += work - sum(amt.values())
    months, mw = p["months"], p["month_weights"]
    rows = []
    for k, a in sorted(amt.items(), key=lambda kv: -kv[1]):
        c = p["channels"][k]
        per_month = [int(a * w / 1000) * 1000 for w in mw]
        per_month[-1] += a - sum(per_month)
        rows.append({"channel": k, "share": round(a / total, 4), "amount_vnd": a, "per_month_vnd": per_month,
                     "expected_orders": int(a / c["cpa"]), "expected_revenue_vnd": int(a * c["roas"]),
                     "cpa_benchmark": c["cpa"], "roas_benchmark": c["roas"],
                     "implied_aov_vnd": int(c["cpa"] * c["roas"])})
    res_month = [int(reserve * w / 1000) * 1000 for w in mw]
    res_month[-1] += reserve - sum(res_month)
    exp_orders = sum(r["expected_orders"] for r in rows)
    exp_rev = sum(r["expected_revenue_vnd"] for r in rows)
    goals = p.get("goals") or {}
    gap = {"implied_aov_vnd": int(exp_rev / exp_orders) if exp_orders else None,
           "revenue_goal_vnd": goals.get("revenue_vnd"), "orders_goal": goals.get("orders"),
           "revenue_gap_vnd": (exp_rev - goals["revenue_vnd"]) if goals.get("revenue_vnd") else None,
           "orders_gap": (exp_orders - goals["orders"]) if goals.get("orders") else None}
    return {"phase": p.get("phase"), "goal_gap": gap, "total_budget_vnd": total, "reserve_vnd": reserve, "reserve_per_month_vnd": res_month,
            "months": months, "rows": rows,
            "expected_orders": sum(r["expected_orders"] for r in rows),
            "expected_revenue_vnd": sum(r["expected_revenue_vnd"] for r in rows)}


def vnd(n: int) -> str:
    return f"{n:,}"


def to_md(a: dict) -> str:
    head = "| Kênh / Channel | Tỷ trọng | " + " | ".join(a["months"]) + " | Tổng (VND) | Đơn dự kiến | Doanh thu dự kiến (VND) |"
    lines = [head, "|" + "---|" * (len(a["months"]) + 5)]
    for r in a["rows"]:
        lines.append(f"| {r['channel']} | {r['share']:.1%} | " + " | ".join(vnd(x) for x in r["per_month_vnd"]) +
                     f" | {vnd(r['amount_vnd'])} | {r['expected_orders']:,} | {vnd(r['expected_revenue_vnd'])} |")
    lines.append(f"| reserve (dự phòng/test) | {a['reserve_vnd'] / a['total_budget_vnd']:.1%} | " +
                 " | ".join(vnd(x) for x in a["reserve_per_month_vnd"]) + f" | {vnd(a['reserve_vnd'])} | – | – |")
    lines.append(f"| **Tổng / Total** | 100% | " + " | ".join(
        vnd(sum(r["per_month_vnd"][i] for r in a["rows"]) + a["reserve_per_month_vnd"][i]) for i in range(len(a["months"]))) +
                 f" | **{vnd(a['total_budget_vnd'])}** | {a['expected_orders']:,} | {vnd(a['expected_revenue_vnd'])} |")
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("brief"); ap.add_argument("--json"); ap.add_argument("--md")
    a = ap.parse_args(argv)
    alloc = allocate(params(Path(a.brief)))
    md = to_md(alloc)
    if a.json:
        Path(a.json).write_text(json.dumps(alloc, indent=1, ensure_ascii=False))
    if a.md:
        Path(a.md).write_text(md)
    print(md)
    print(f"expected orders {alloc['expected_orders']:,}; expected revenue {vnd(alloc['expected_revenue_vnd'])} VND "
          "(benchmarks from the brief; label as assumption)")
    g = alloc["goal_gap"]
    print(f"implied AOV (CPA x ROAS) {g['implied_aov_vnd']:,} VND; revenue gap vs goal "
          f"{g['revenue_gap_vnd'] if g['revenue_gap_vnd'] is not None else 'n/a (add goals: to the params block)'}; "
          f"orders gap {g['orders_gap'] if g['orders_gap'] is not None else 'n/a'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
