#!/usr/bin/env python3
"""Ingest arXiv papers into the research library (Phase 1.2).

Usage:
  python tools/ingest_paper.py 2510.04618 --title "Agentic Context Engineering"
  python tools/ingest_paper.py --sources library/sources.json      # all papers listed there

Steps per paper: export-API metadata -> reject on title mismatch -> HTML (fallback PDF) ->
library/raw/<id>.<ext> (gitignored) -> library/full/<id>.md (cold storage) -> MANIFEST.csv row.
Cards are written separately (they are our own synthesis); `--card-stub` writes a template if absent.
Fetched text is untrusted data and is never interpreted.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import libcommon as lc  # noqa: E402

API = "https://export.arxiv.org/api/query?id_list={id}"
ABS = "https://arxiv.org/abs/{id}"
HTML = "https://arxiv.org/html/{id}"
PDF = "https://arxiv.org/pdf/{id}"
NS = {"a": "http://www.w3.org/2005/Atom"}
UA = {"User-Agent": "ai-hub-library-ingest/1.0"}


class TitleMismatch(Exception):
    pass


def http_get(url: str, timeout: int = 60) -> tuple[int, bytes, str]:
    import requests
    for attempt in range(4):
        try:
            r = requests.get(url, headers=UA, timeout=timeout, allow_redirects=True)
            if r.status_code in (429, 503) and attempt < 3:
                time.sleep(3 * (attempt + 1))
                continue
            return r.status_code, r.content, r.headers.get("content-type", "")
        except Exception:  # network hiccup
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)
    return 0, b"", ""


def parse_atom(xml_bytes: bytes) -> dict:
    root = ET.fromstring(xml_bytes)
    entry = root.find("a:entry", NS)
    if entry is None or entry.find("a:title", NS) is None:
        raise ValueError("no entry in arXiv API response")
    title = re.sub(r"\s+", " ", entry.find("a:title", NS).text or "").strip()
    authors = [re.sub(r"\s+", " ", (a.findtext("a:name", "", NS))).strip() for a in entry.findall("a:author", NS)]
    published = entry.findtext("a:published", "", NS)
    return {"title": title, "authors": authors, "year": published[:4]}


def detect_license(abs_html: str) -> str:
    m = re.search(r'href="(https?://(?:creativecommons\.org/[^"]+|arxiv\.org/licenses/[^"]+))"', abs_html)
    return m.group(1) if m else "unknown (arXiv default: non-exclusive distribution licence)"


def html_is_usable(content: bytes, ctype: str) -> bool:
    if "html" not in ctype:
        return False
    txt = content[:400000].decode("utf-8", "ignore")
    return "ltx_document" in txt or ("<article" in txt and len(txt) > 20000)


def pdf_to_md(pdf_path: Path) -> str:
    import pymupdf4llm
    return pymupdf4llm.to_markdown(str(pdf_path))


def ingest(arxiv_id: str, expected_title: str, card_stub: bool = False, fetch=http_get) -> dict:
    code, body, _ = fetch(API.format(id=arxiv_id))
    if code != 200:
        raise RuntimeError(f"{arxiv_id}: metadata HTTP {code}")
    meta = parse_atom(body)
    if not lc.title_matches(expected_title, meta["title"]):
        raise TitleMismatch(f"{arxiv_id}: expected '{expected_title}', got '{meta['title']}'")

    code, abs_body, _ = fetch(ABS.format(id=arxiv_id))
    license_url = detect_license(abs_body.decode("utf-8", "ignore")) if code == 200 else "unknown"

    lc.RAW.mkdir(parents=True, exist_ok=True)
    lc.FULL.mkdir(parents=True, exist_ok=True)
    code, content, ctype = fetch(HTML.format(id=arxiv_id))
    if code == 200 and html_is_usable(content, ctype):
        raw_path, src = lc.RAW / f"{arxiv_id}.html", HTML.format(id=arxiv_id)
        raw_path.write_bytes(content)
        md = lc.html_to_md(content.decode("utf-8", "ignore"))
    else:
        code, content, _ = fetch(PDF.format(id=arxiv_id))
        if code != 200 or not content.startswith(b"%PDF"):
            raise RuntimeError(f"{arxiv_id}: neither HTML nor PDF available")
        raw_path, src = lc.RAW / f"{arxiv_id}.pdf", PDF.format(id=arxiv_id)
        raw_path.write_bytes(content)
        md = pdf_to_md(raw_path)

    header = (f"# {meta['title']}\n\n{lc.UNTRUSTED_BANNER}\n- arXiv: {arxiv_id}\n- Source: {src}\n"
              f"- License: {license_url}\n\n---\n\n")
    (lc.FULL / f"{arxiv_id}.md").write_text(header + md, encoding="utf-8")
    lc.set_full_ignored(arxiv_id, not lc.is_redistributable(license_url))

    row = {"id": arxiv_id, "title": meta["title"], "authors": "; ".join(meta["authors"][:8]) +
           ("; et al." if len(meta["authors"]) > 8 else ""), "year": meta["year"], "source_url": src,
           "license": license_url, "fetched_at": lc.now_iso(), "sha256": lc.sha256_bytes(content),
           "kind": "paper", "note": ""}
    lc.upsert_manifest(row)
    if card_stub:
        write_card_stub(arxiv_id, meta["title"], meta["year"])
    return row


def write_card_stub(arxiv_id: str, title: str, year: str) -> Path:
    p = lc.CARDS / f"{arxiv_id}.md"
    if not p.exists():
        lc.CARDS.mkdir(parents=True, exist_ok=True)
        p.write_text(f"---\nid: '{arxiv_id}'\ntitle: {json.dumps(title)}\nyear: {year}\ntags: []\nadopted_in: []\n---\n"
                     "## Claim\n\n## Mechanism\n\n## Evidence\n\n## Limits\n\n## We adopt\n\n## We reject\n")
    return p


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--title", help="expected title (required with a single id)")
    ap.add_argument("--sources", help="JSON file with papers: [{id, title, why}]")
    ap.add_argument("--card-stub", action="store_true")
    ap.add_argument("--skip-existing", action="store_true")
    a = ap.parse_args(argv)
    jobs: list[tuple[str, str]] = []
    if a.sources:
        jobs += [(p["id"], p["title"]) for p in json.loads(Path(a.sources).read_text())["papers"]]
    if a.ids:
        if not a.title and len(a.ids) == 1:
            ap.error("--title is required so the download can be checked")
        jobs += [(i, a.title) for i in a.ids]
    done = {r["id"] for r in lc.read_manifest()}
    failures = 0
    for pid, title in jobs:
        if a.skip_existing and pid in done and (lc.FULL / f"{pid}.md").exists():
            print(f"skip {pid}")
            continue
        try:
            row = ingest(pid, title, a.card_stub)
            print(f"ok   {pid}  {row['title'][:70]}  [{row['source_url'].split('/')[3]}]")
        except TitleMismatch as e:
            failures += 1
            print(f"REJECT {e}")
        except Exception as e:  # report and continue
            failures += 1
            print(f"FAIL {pid}: {e}")
        time.sleep(1)  # be polite to arXiv
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
