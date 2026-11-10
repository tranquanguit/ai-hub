#!/usr/bin/env python3
"""Deterministic parts of a CS training pack, built from the product sheet (no reasoning needed).

  build_pack.py <product-sheet.md> --out-dir <dir>

Writes:
  product_facts.md   one fact card per SKU (price, size, ingredients, skin type, usage, caution, shelf life)
  quiz.md            questions generated from the sheet (prices, sizes, skin types, policies)
  answer_key.json    {question_no: expected answer substring} used by check_training.py
Facts are copied verbatim from the sheet, so the quiz can never contradict it.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def parse_products(md: str) -> list[dict]:
    lines = [l for l in md.splitlines() if l.startswith("|")]
    header = None
    rows = []
    for l in lines:
        cells = [c.strip() for c in l.strip("|").split("|")]
        if header is None and any(c.upper() == "SKU" for c in cells):
            header = cells
            continue
        if header and not set("".join(cells)) <= set("-: ") and len(cells) == len(header):
            rows.append(dict(zip(header, cells)))
    keymap = {"SKU": "sku", "Tên": "name", "Dung tích": "size", "Giá (VND)": "price", "Thành phần chính": "ingredients",
              "Loại da": "skin", "Cách dùng": "usage", "Lưu ý": "caution", "HSD sau mở nắp": "pao"}
    return [{keymap.get(k, k): v for k, v in r.items()} for r in rows]


def parse_policy(md: str) -> dict:
    sec = md.split("## Chính sách", 1)[-1].split("\n## ", 1)[0]
    out = {}
    for line in sec.splitlines():
        m = re.match(r"-\s*([^:]+):\s*(.+)", line)
        if m:
            out[m.group(1).strip()] = m.group(2).strip()
    return out


def vnd(s: str) -> str:
    return f"{int(re.sub(r'[^0-9]', '', s)):,}"


def build(md: str) -> tuple[str, str, dict]:
    prods = parse_products(md)
    pol = parse_policy(md)
    facts = ["# Thẻ thông tin sản phẩm (từ product sheet; không tự thêm công dụng)", ""]
    for p in prods:
        facts += [f"## {p['sku']} — {p['name']}", f"- Dung tích: {p['size']} | Giá: {vnd(p['price'])} VND",
                  f"- Thành phần chính: {p['ingredients']}", f"- Loại da phù hợp: {p['skin']}",
                  f"- Cách dùng: {p['usage']}", f"- Lưu ý: {p['caution']}", f"- HSD sau mở nắp: {p['pao']}", ""]
    q, key = ["# Bài kiểm tra kiến thức (tự động từ product sheet)", ""], {}
    n = 0
    for p in prods:
        n += 1
        q.append(f"{n}. Giá bán lẻ của {p['name']} ({p['sku']}) là bao nhiêu?")
        key[str(n)] = vnd(p["price"])
        n += 1
        q.append(f"{n}. {p['name']} có dung tích/khối lượng bao nhiêu?")
        key[str(n)] = p["size"]
        n += 1
        q.append(f"{n}. Lưu ý quan trọng khi tư vấn {p['name']} là gì?")
        key[str(n)] = p["caution"]
    for label in ("Đổi trả", "Kích ứng da", "SLA", "Giao hàng"):
        if label in pol:
            n += 1
            q.append(f"{n}. Chính sách/quy trình '{label}' là gì?")
            key[str(n)] = pol[label][:60]
    return "\n".join(facts) + "\n", "\n".join(q) + "\n", key


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("sheet"); ap.add_argument("--out-dir", required=True)
    a = ap.parse_args(argv)
    facts, quiz, key = build(Path(a.sheet).read_text(encoding="utf-8"))
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "product_facts.md").write_text(facts, encoding="utf-8")
    (out / "quiz.md").write_text(quiz, encoding="utf-8")
    (out / "answer_key.json").write_text(json.dumps(key, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"wrote product_facts.md ({facts.count('## ')} SKUs), quiz.md ({len(key)} questions), answer_key.json to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
