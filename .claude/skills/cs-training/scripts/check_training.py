#!/usr/bin/env python3
"""Deterministic grader for a CS training pack.

  check_training.py <training.md> --sheet <product-sheet.md> [--key answer_key.json]

Checks: required sections; every SKU from the sheet covered with its exact price; segments from the
sheet covered; service protocol has greeting, skin-reaction escalation, returns window and SLA;
>= 4 sample dialogues; quiz + answer key consistent with the sheet; FAQ answers avoid banned
claims; no customer PII; SAMPLE disclosed when the sheet is SAMPLE; English summary.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("build_pack", HERE / "build_pack.py")
bp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bp)

SECTIONS = {"products": r"sản phẩm|product", "segments": r"phân khúc|segment", "protocol": r"quy trình|protocol",
            "dialogues": r"kịch bản|hội thoại|dialogue|script", "faq": r"câu hỏi thường gặp|faq",
            "quiz": r"kiểm tra|quiz", "english_summary": r"english summary"}
BANNED = [r"\btrị\s+(mụn|nám|thâm)", r"\bchữa\b", r"đặc trị", r"khỏi hẳn", r"\b100\s*%\s*(hiệu quả|an toàn)", r"tốt nhất",
          r"số\s*1\b"]
PII = [r"(?<![\d.,])(?:\+?84|0)(?:3|5|7|8|9)\d{8}(?![\d.,])",
       r"\b[A-Za-z0-9._%+-]+@(?!(?:example\.(?:com|vn)|lunobeau\.vn)\b)[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"]


def norm(s: str) -> str:
    return re.sub(r"[\s.,]", "", s.lower())


def checks(md: str, sheet: str, key: dict | None) -> list[tuple[str, bool, str]]:
    res = []
    hs = [h.lower() for h in re.findall(r"^#{1,4}\s+(.+)$", md, re.M)]
    for k, pat in SECTIONS.items():
        res.append((f"section:{k}", any(re.search(pat, h) for h in hs), pat))
    prods = bp.parse_products(sheet)
    miss = [p["sku"] for p in prods if p["sku"] not in md or norm(bp.vnd(p["price"])) not in norm(md)]
    res.append(("all_skus_with_price", not miss, f"missing/incorrect: {miss}"))
    segs = re.findall(r"^- ([^:]+):", sheet.split("## Phân khúc", 1)[-1].split("\n## ", 1)[0], re.M)
    seg_miss = [s for s in segs if s.split()[0].lower() not in md.lower() or
                not re.search(re.escape(s.split()[1].lower()) if len(s.split()) > 1 else "", md.lower())]
    res.append(("segments_covered", not seg_miss, f"missing: {seg_miss}"))
    low = md.lower()
    proto = {"greeting": r"chào", "skin_reaction_escalation": r"kích ứng.*(founder|báo|chuyển)|(founder|báo).*kích ứng",
             "returns_7_days": r"7 ngày", "sla_15_min": r"15 phút"}
    pmiss = [k for k, p in proto.items() if not re.search(p, low, re.S)]
    res.append(("protocol_elements", not pmiss, f"missing: {pmiss}"))
    dialogs = len(re.findall(r"^#{3,4}\s+.*(kịch bản|tình huống|dialogue|hội thoại)", md, re.M | re.I))
    res.append(("dialogues>=4", dialogs >= 4, f"found {dialogs}"))
    if key:
        kmiss = [n for n, ans in key.items() if norm(ans)[:25] not in norm(md)]
        res.append(("quiz_answers_match_sheet", not kmiss, f"answers not found for questions {kmiss}"))
    hits = [p for p in BANNED if re.search(p, md, re.I)]
    res.append(("no_banned_claims", not hits, f"found {hits}"))
    res.append(("no_pii", not any(re.search(p, md) for p in PII), "customer personal data found"))
    if "SAMPLE" in sheet:
        res.append(("sample_disclosed", "sample" in low, "built on SAMPLE sheet; must say so"))
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("training"); ap.add_argument("--sheet", required=True); ap.add_argument("--key")
    a = ap.parse_args(argv)
    md = Path(a.training).read_text(encoding="utf-8")
    key = json.loads(Path(a.key).read_text()) if a.key else None
    res = checks(md, Path(a.sheet).read_text(encoding="utf-8"), key)
    for name, ok, info in res:
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + ("" if ok else f"  ({info})"))
    passed = sum(ok for _, ok, _ in res)
    print(f"score {passed}/{len(res)}  =>  {'PASS' if passed == len(res) else 'FAIL'}")
    return 0 if passed == len(res) else 1


if __name__ == "__main__":
    sys.exit(main())
