#!/usr/bin/env python3
"""Validate paper cards and (re)generate library/INDEX.md.

  python tools/library_index.py check   # validate every card against the template; exit 1 on problems
  python tools/library_index.py build   # write library/INDEX.md (cards + doc pages from MANIFEST)

Card template (Phase 1.2): frontmatter id/title/year/tags/adopted_in, sections Claim, Mechanism,
Evidence, Limits, We adopt, We reject; <= 400 words; every adopted_in anchor must exist.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import libcommon as lc  # noqa: E402

SECTIONS = ["Claim", "Mechanism", "Evidence", "Limits", "We adopt", "We reject"]
FRONT = ["id", "title", "year", "tags", "adopted_in"]
MAX_WORDS = 400


def parse_card(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise ValueError("missing frontmatter")
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def section(body: str, name: str) -> str:
    m = re.search(rf"^## {re.escape(name)}[^\n]*\n(.*?)(?=^## |\Z)", body, re.S | re.M)
    return m.group(1).strip() if m else ""


def anchors_in(md_path: Path) -> set[str]:
    if not md_path.exists():
        return set()
    return {re.sub(r"[^a-z0-9-]", "", h.strip().lower().replace(" ", "-"))
            for h in re.findall(r"^#{2,3} (.+)$", md_path.read_text(), re.M)}


def check_card(path: Path, root: Path = lc.ROOT) -> list[str]:
    errs = []
    try:
        fm, body = parse_card(path)
    except Exception as e:
        return [f"{path.name}: {e}"]
    for k in FRONT:
        if k not in fm or fm[k] in (None, "", []):
            errs.append(f"{path.name}: frontmatter '{k}' missing or empty")
    if str(fm.get("id")) != path.stem:
        errs.append(f"{path.name}: id '{fm.get('id')}' != filename")
    for s in SECTIONS:
        if not section(body, s):
            errs.append(f"{path.name}: section '## {s}' missing or empty")
    words = len(path.read_text().split())
    if words > MAX_WORDS:
        errs.append(f"{path.name}: {words} words > {MAX_WORDS}")
    for ref in fm.get("adopted_in") or []:
        ref = str(ref)
        file_part, _, anchor = ref.partition("#")
        target = root / file_part
        if not target.exists():
            errs.append(f"{path.name}: adopted_in target missing: {ref}")
        elif anchor and anchor not in anchors_in(target):
            errs.append(f"{path.name}: anchor not found: {ref}")
    return errs


def cmd_check(strict_targets: bool = True) -> int:
    papers = [r for r in lc.read_manifest() if r.get("kind") == "paper"]
    errs = []
    for r in papers:
        p = lc.CARDS / f"{r['id']}.md"
        if not p.exists():
            errs.append(f"{r['id']}: no card")
            continue
        e = check_card(p)
        if not strict_targets:
            e = [x for x in e if "adopted_in target missing" not in x]
        errs += e
    for e in errs:
        print("FAIL", e)
    print(f"cards checked: {len(papers)}, problems: {len(errs)}")
    return 1 if errs else 0


def cmd_build() -> int:
    takeaways = {d["id"]: d.get("takeaway", "") for d in
                 json.loads((lc.LIB / "sources.json").read_text()).get("docs", [])}
    lines = ["# Library index", "",
             "The only library file other parts of the repo point to. Cards are summaries (hot enough to read);",
             "`library/full/` is cold storage, opened only by the paper-ingest skill or on request.", "",
             "## Papers (cards in `library/cards/`)", ""]
    for r in sorted((r for r in lc.read_manifest() if r["kind"] == "paper"), key=lambda r: r["id"]):
        p = lc.CARDS / f"{r['id']}.md"
        claim = ""
        if p.exists():
            fm, body = parse_card(p)
            claim = re.sub(r"\s+", " ", section(body, "Claim"))
        lines.append(f"- [{r['id']}](cards/{r['id']}.md) **{fm.get('title', r['title'])}** — {claim}")
    lines += ["", "## Documentation (cite as `doc:<id>`; URLs in MANIFEST.csv)", ""]
    for r in sorted((r for r in lc.read_manifest() if r["kind"] == "doc"), key=lambda r: r["id"]):
        lines.append(f"- `doc:{r['id']}` [{r['title'].split(' \\ ')[0].split(' - Claude')[0]}]({r['source_url']}) — "
                     f"{takeaways.get(r['id'], '')}")
    (lc.LIB / "INDEX.md").write_text("\n".join(lines) + "\n")
    print(f"wrote library/INDEX.md ({len(lines)} lines)")
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    sys.exit(cmd_build() if cmd == "build" else cmd_check(strict_targets="--loose" not in sys.argv))
