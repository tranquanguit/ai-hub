#!/usr/bin/env python3
"""Deterministic grader for a phase plan (used by the phase-plan skill and its golden eval).

  check_plan.py <plan.md> --alloc <allocation.json> [--brief <brief.md>]

Checks (each prints PASS/FAIL): required bilingual sections; budget total row equals the brief
total; every allocated channel has a strategy subsection; KPI section has numbers; assumptions
section exists and SAMPLE inputs are disclosed; no banned cosmetic claims; no customer PII;
English summary present. Exit 1 if any check fails.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SECTIONS = {
    "channels": r"kênh bán|sales channel",
    "regions": r"khu vực|region",
    "audiences": r"khách hàng mục tiêu|target audience",
    "budget": r"ngân sách|budget",
    "channel_strategy": r"chiến lược.*kênh|channel strateg",
    "kpi": r"\bkpi",
    "timeline": r"lịch triển khai|timeline",
    "risks": r"rủi ro|risk",
    "assumptions": r"giả định|assumption",
    "english_summary": r"english summary",
}
BANNED = [r"\btrị\s+(mụn|nám|thâm)", r"\bchữa\b", r"đặc trị", r"khỏi hẳn", r"\b100\s*%\s*(hiệu quả|an toàn|tự nhiên)",
          r"tốt nhất", r"số\s*1\b"]
PII = [r"(?<![\d.,])(?:\+?84|0)(?:3|5|7|8|9)\d{8}(?![\d.,])",
       r"\b[A-Za-z0-9._%+-]+@(?!(?:example\.(?:com|vn)|lunobeau\.vn)\b)[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"]


def headings(md: str) -> list[str]:
    return [h.lower() for h in re.findall(r"^#{1,4}\s+(.+)$", md, re.M)]


def section_text(md: str, pattern: str) -> str:
    """Text of every section whose heading matches, including its nested subsections."""
    out, level = [], None
    for line in md.splitlines():
        m = re.match(r"^(#{1,6})\s+(.+)$", line)
        if m:
            if level is not None and len(m.group(1)) <= level:
                level = None
            if level is None and re.search(pattern, m.group(2).lower()):
                level = len(m.group(1))
                continue
        if level is not None:
            out.append(line)
    return "\n".join(out)


def num(s: str) -> int:
    return int(re.sub(r"[^\d]", "", s) or 0)


def checks(md: str, alloc: dict) -> list[tuple[str, bool, str]]:
    res = []
    hs = headings(md)
    for k, pat in SECTIONS.items():
        res.append((f"section:{k}", any(re.search(pat, h) for h in hs), pat))
    total_rows = [l for l in md.splitlines() if l.startswith("|") and re.search(r"tổng|total", l, re.I)]
    totals = [num(c) for l in total_rows for c in l.split("|") if re.search(r"\d{1,3}([.,]\d{3}){2,}", c)]
    ok_total = alloc["total_budget_vnd"] in totals
    res.append(("budget_total_matches_brief", ok_total, f"expected {alloc['total_budget_vnd']:,}, found {totals[:6]}"))
    strat = section_text(md, SECTIONS["channel_strategy"]).lower()
    missing = [r["channel"] for r in alloc["rows"] if r["channel"].split("_")[0] not in strat]
    res.append(("strategy_per_channel", not missing, f"missing: {missing}"))
    kpi = section_text(md, SECTIONS["kpi"])
    res.append(("kpi_has_numbers", len(re.findall(r"\d", kpi)) >= 6, "KPI section needs numeric targets"))
    res.append(("sample_disclosed", "sample" in md.lower(), "deliverable built on SAMPLE input must say so"))
    hits = [p for p in BANNED if re.search(p, md, re.I)]
    res.append(("no_banned_claims", not hits, f"found {hits}"))
    pii = [p for p in PII if re.search(p, md)]
    res.append(("no_pii", not pii, "customer personal data found"))
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("plan"); ap.add_argument("--alloc", required=True); ap.add_argument("--brief")
    a = ap.parse_args(argv)
    md = Path(a.plan).read_text(encoding="utf-8")
    alloc = json.loads(Path(a.alloc).read_text())
    res = checks(md, alloc)
    for name, ok, info in res:
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + ("" if ok else f"  ({info})"))
    passed = sum(ok for _, ok, _ in res)
    print(f"score {passed}/{len(res)}  =>  {'PASS' if passed == len(res) else 'FAIL'}")
    return 0 if passed == len(res) else 1


if __name__ == "__main__":
    sys.exit(main())
