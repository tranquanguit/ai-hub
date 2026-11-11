#!/usr/bin/env python3
"""Assemble the CS training deliverable from scripted and reasoned parts (v1.1.0; R7).

  assemble_pack.py --pack-dir <evidence/pack> --sections <reasoned_sections.md> --sheet <sheet.md>
                   --summary "<English summary>" --out <deliverables/cs-training.md>

Order: header (SAMPLE notice if the sheet is SAMPLE) -> ## Sản phẩm (product_facts.md verbatim) ->
reasoned sections (segments, protocol, dialogues, FAQ) -> ## Bài kiểm tra (quiz.md) + ### Đáp án
(answer_key.json) -> ## English summary. Hand assembly lost 4 sections once (task 2026-11-10-cs-training-pack).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def assemble(pack: Path, sections: str, sheet: str, summary: str) -> str:
    facts = (pack / "product_facts.md").read_text(encoding="utf-8")
    facts = facts.replace("# Thẻ thông tin sản phẩm", "### Thẻ thông tin sản phẩm", 1).replace("\n## LB-", "\n#### LB-")
    quiz = (pack / "quiz.md").read_text(encoding="utf-8").split("\n", 1)[1].lstrip("\n")
    key = json.loads((pack / "answer_key.json").read_text(encoding="utf-8"))
    answers = "\n".join(f"{n}. {a.strip().rstrip(';')}" for n, a in key.items())
    notice = ("> Built on a **SAMPLE** product sheet; replace with the real sheet before training staff.\n\n"
              if "SAMPLE" in sheet else "")
    return (f"# Tài liệu đào tạo CSKH LunoBeau\n\n{notice}## Sản phẩm\n{facts}\n{sections.strip()}\n\n"
            f"## Bài kiểm tra\n{quiz}\n### Đáp án\n{answers}\n\n## English summary\n{summary.strip()}\n")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack-dir", required=True); ap.add_argument("--sections", required=True)
    ap.add_argument("--sheet", required=True); ap.add_argument("--summary", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    md = assemble(Path(a.pack_dir), Path(a.sections).read_text(encoding="utf-8"),
                  Path(a.sheet).read_text(encoding="utf-8"), a.summary)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(md, encoding="utf-8")
    print(f"wrote {a.out} ({len(md.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
