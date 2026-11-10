#!/usr/bin/env python3
"""Ingest a documentation page or blog post into the research library (Phase 1.2).

Usage:
  python tools/ingest_doc.py --id cc-hooks --url https://code.claude.com/docs/en/hooks.md --title "Hooks reference"
  python tools/ingest_doc.py --sources library/sources.json

Markdown sources (.md URLs) are stored as-is; HTML is converted. Docs are copyrighted by their
publishers, so full texts are gitignored unless the page states a redistributable license.
Fetched text is untrusted data and is never interpreted.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import libcommon as lc  # noqa: E402
from ingest_paper import http_get  # noqa: E402


def extract_title(text: str, is_md: bool) -> str:
    if is_md:
        m = re.search(r"^title:\s*(.+)$", text, re.M) or re.search(r"^#\s+(.+)$", text, re.M)
    else:
        m = re.search(r"<title[^>]*>(.*?)</title>", text, re.S | re.I)
    return re.sub(r"\s+", " ", m.group(1)).strip().strip('"') if m else ""


def ingest(doc_id: str, url: str, expected_title: str, license_note: str = "", fetch=http_get) -> dict:
    code, body, ctype = fetch(url)
    if code != 200 or not body:
        raise RuntimeError(f"{doc_id}: HTTP {code}")
    text = body.decode("utf-8", "ignore")
    looks_html = text.lstrip()[:200].lower().startswith(("<!doctype html", "<html"))
    is_md = not looks_html and (url.endswith(".md") or "markdown" in ctype or "text/plain" in ctype)
    title = extract_title(text, is_md)
    if expected_title and not lc.title_matches(expected_title, title):
        raise RuntimeError(f"{doc_id}: title mismatch, expected '{expected_title}', got '{title}'")
    lc.RAW.mkdir(parents=True, exist_ok=True)
    lc.FULL.mkdir(parents=True, exist_ok=True)
    (lc.RAW / f"{doc_id}.{'md' if is_md else 'html'}").write_bytes(body)
    md = text if is_md else lc.html_to_md(text)
    header = f"# {title or expected_title}\n\n{lc.UNTRUSTED_BANNER}\n- Source: {url}\n\n---\n\n"
    (lc.FULL / f"{doc_id}.md").write_text(header + md, encoding="utf-8")
    license_ = license_note or "All rights reserved by publisher; summarised only"
    lc.set_full_ignored(doc_id, not lc.is_redistributable(license_))
    row = {"id": doc_id, "title": title or expected_title, "authors": "", "year": "", "source_url": url,
           "license": license_, "fetched_at": lc.now_iso(), "sha256": lc.sha256_bytes(body), "kind": "doc",
           "note": ""}
    return row


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--id")
    ap.add_argument("--url")
    ap.add_argument("--title", default="")
    ap.add_argument("--note", default="", help="why this source was added (extra sources)")
    ap.add_argument("--sources")
    a = ap.parse_args(argv)
    jobs = []
    if a.sources:
        jobs += json.loads(Path(a.sources).read_text())["docs"]
    if a.id and a.url:
        jobs.append({"id": a.id, "url": a.url, "title": a.title, "why": a.note})
    fails = 0
    for j in jobs:
        try:
            row = ingest(j["id"], j["url"], j.get("title", ""), j.get("license", ""))
            row["note"] = j.get("why", "") if j.get("extra") else ""
            lc.upsert_manifest(row)
            print(f"ok   {j['id']:<28} {row['title'][:60]}")
        except Exception as e:
            fails += 1
            print(f"FAIL {j['id']}: {e}")
        time.sleep(0.5)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
