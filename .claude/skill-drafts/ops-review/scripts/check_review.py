#!/usr/bin/env python3
"""Deterministic grader for an ops review.

  check_review.py <review.md> --kpis <kpis.json>

Checks: required sections; every flagged campaign / SEO drop / CS-flagged channel is named in the
recommendations; every recommendation line has an owner role and a measurable next check; the
ROAS quoted for each flagged campaign matches kpis.json (±0.05); skin-reaction reports are
escalated when > 0; SAMPLE disclosed; no banned claims; no PII; English summary.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SECTIONS = {"summary": r"tóm tắt|summary", "ads": r"quảng cáo|ads", "seo": r"\bseo\b", "cs": r"cskh|customer service",
            "recommendations": r"đề xuất|khuyến nghị|recommendation", "english_summary": r"english summary"}
ROLES = r"\b(founder|marketing|sales|cs|cskh)\b"
BANNED = [r"\btrị\s+(mụn|nám|thâm)", r"\bchữa\b", r"đặc trị", r"khỏi hẳn", r"tốt nhất", r"số\s*1\b"]
PII = [r"(?<![\d.,])(?:\+?84|0)(?:3|5|7|8|9)\d{8}(?![\d.,])",
       r"\b[A-Za-z0-9._%+-]+@(?!(?:example\.(?:com|vn)|lunobeau\.vn)\b)[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"]


def section_text(md: str, pattern: str) -> str:
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


def table_values(md: str, column: str) -> dict[str, list[float]]:
    """{first-cell: [values in the column named `column`]} over every markdown table in md."""
    out: dict[str, list[float]] = {}
    header = None
    for line in md.splitlines():
        if not line.startswith("|"):
            header = None
            continue
        cells = [c.strip().strip("*") for c in line.strip().strip("|").split("|")]
        if header is None:
            header = [c.lower() for c in cells]
            continue
        if set("".join(cells)) <= set("-: "):
            continue
        if column in header and len(cells) == len(header):
            v = cells[header.index(column)].replace(",", "")
            try:
                out.setdefault(cells[0], []).append(float(v))
            except ValueError:
                pass
    return out


def checks(md: str, k: dict) -> list[tuple[str, bool, str]]:
    res = []
    hs = [h.lower() for h in re.findall(r"^#{1,4}\s+(.+)$", md, re.M)]
    for name, pat in SECTIONS.items():
        res.append((f"section:{name}", any(re.search(pat, h) for h in hs), pat))
    rec = section_text(md, SECTIONS["recommendations"])
    need = k.get("ads", {}).get("flagged", []) + k.get("seo", {}).get("drops", []) + k.get("cs", {}).get("flagged", [])
    miss = [n for n in need if n.lower() not in rec.lower()]
    res.append(("every_flag_has_recommendation", not miss, f"not addressed: {miss}"))
    items = [l for l in rec.splitlines() if re.match(r"\s*(\d+\.|-|\|)\s", l) and not re.match(r"\s*\|[-\s|]+\|?$", l)
             and not re.search(r"\|\s*(#|owner|người|việc)\b", l, re.I)]
    bad = [l[:60] for l in items if not re.search(ROLES, l, re.I) or not re.search(r"\d", l)]
    res.append(("recommendations_have_owner_and_metric", bool(items) and not bad, f"{len(bad)} lines lack owner or number: {bad[:3]}"))
    wrong = []
    roas_cells = table_values(md, "roas")
    for c in k.get("ads", {}).get("campaigns", []):
        if c["flags"] and c["roas"] is not None:
            quoted = roas_cells.get(c["campaign"], []) + [
                float(x.replace(",", ".")) for x in
                re.findall(rf"{re.escape(c['campaign'])}[^\n]*?\bROAS\s*[:=]?\s*(\d+(?:[.,]\d+)?)\b(?!\s*(?:ngày|day|%))", md)]
            if quoted and all(abs(q - c["roas"]) > 0.05 for q in quoted):
                wrong.append(f"{c['campaign']} quoted {quoted} vs {c['roas']}")
    res.append(("quoted_roas_matches_kpis", not wrong, f"{wrong}"))
    if k.get("cs", {}).get("skin_reaction_reports", 0) > 0:
        res.append(("skin_reaction_escalated", bool(re.search(r"kích ứng.*founder|founder.*kích ứng", md, re.I | re.S)),
                    "skin-reaction reports must be escalated to the founder"))
    res.append(("sample_disclosed", "sample" in md.lower() or "SAMPLE" not in json.dumps(k), "SAMPLE data must be disclosed"))
    res.append(("no_banned_claims", not any(re.search(p, md, re.I) for p in BANNED), "banned claim found"))
    res.append(("no_pii", not any(re.search(p, md) for p in PII), "customer personal data found"))
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("review"); ap.add_argument("--kpis", required=True)
    a = ap.parse_args(argv)
    md = Path(a.review).read_text(encoding="utf-8")
    k = json.loads(Path(a.kpis).read_text())
    res = checks(md, k)
    for name, ok, info in res:
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + ("" if ok else f"  ({info})"))
    passed = sum(ok for _, ok, _ in res)
    print(f"score {passed}/{len(res)}  =>  {'PASS' if passed == len(res) else 'FAIL'}")
    return 0 if passed == len(res) else 1


if __name__ == "__main__":
    sys.exit(main())
