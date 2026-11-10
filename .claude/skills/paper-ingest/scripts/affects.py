#!/usr/bin/env python3
"""Propose which DESIGN.md decisions a (new) paper card affects, by tag/keyword overlap.

  affects.py <card-id> [--top 4]

Prints ranked DESIGN.md anchors with the shared terms. This is a proposal for the human; it never
edits DESIGN.md (untrusted content never changes rules, R10).
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

import yaml


def find_root() -> Path:
    if os.environ.get("LUNO_ROOT"):
        return Path(os.environ["LUNO_ROOT"])
    for parent in Path(__file__).resolve().parents:
        if (parent / "AGENTS.md").exists() and (parent / ".claude").exists():
            return parent
    return Path.cwd()


ROOT = find_root()
STOP = set("the and for with that this from into are not our its use uses used when which their than more less over "
           "only also they them have has been each what where about will can".split())


def terms(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z][a-z-]{3,}", text.lower()) if w not in STOP}


def sections(design: str) -> dict[str, str]:
    parts = re.split(r"^## ", design, flags=re.M)
    return {p.split("\n", 1)[0].strip(): p for p in parts[1:]}


def rank(card_id: str, top: int = 4) -> list[tuple[str, int, list[str]]]:
    card = (ROOT / "library" / "cards" / f"{card_id}.md").read_text()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", card, re.S)
    fm = yaml.safe_load(m.group(1))
    body = m.group(2)
    key = terms(" ".join(fm.get("tags") or []) + " " + body.split("## We reject")[0])
    out = []
    for anchor, text in sections((ROOT / "DESIGN.md").read_text()).items():
        shared = sorted(key & terms(text))
        if shared:
            out.append((anchor, len(shared), shared[:8]))
    return sorted(out, key=lambda x: -x[1])[:top]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("card")
    ap.add_argument("--top", type=int, default=4)
    a = ap.parse_args(argv)
    print(f"Proposal: card {a.card} may affect these DESIGN.md decisions (human decides):")
    for anchor, n, shared in rank(a.card, a.top):
        print(f"- DESIGN.md#{anchor}  (overlap {n}: {', '.join(shared)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
