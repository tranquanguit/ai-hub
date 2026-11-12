#!/usr/bin/env python3
"""Scan files for secrets (R12) and customer PII (R15). Used by .githooks/pre-commit.

  python tools/secret_scan.py --staged        # staged files only (pre-commit)
  python tools/secret_scan.py PATH...         # given files
  python tools/secret_scan.py --all           # every tracked file

Patterns are shared with the PreToolUse hook (single source of truth). PII is not checked in
library/full (author emails in papers), test files (synthetic fixtures), or data/*/private/.
"""
from __future__ import annotations

import fnmatch
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("ptu", ROOT / ".claude" / "hooks" / "pre_tool_use.py")
ptu = importlib.util.module_from_spec(_spec)
sys.path.insert(0, str(ROOT / ".claude" / "hooks"))
_spec.loader.exec_module(ptu)

PII_EXEMPT = ["library/full/*", "*/tests/*", "tests/*", "data/*/private/*", "library/MANIFEST.csv", "library/cards/*"]
SECRET_EXEMPT = ["*/tests/*"]


def git_files(staged: bool) -> list[str]:
    args = ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"] if staged else ["git", "ls-files"]
    return [l for l in subprocess.run(args, cwd=ROOT, capture_output=True, text=True).stdout.splitlines() if l]


def scan_file(rel: str) -> list[str]:
    p = ROOT / rel
    if not p.is_file() or p.stat().st_size > 2_000_000:
        return []
    try:
        text = p.read_text(encoding="utf-8")
    except Exception:
        return []
    hits = []
    if not any(fnmatch.fnmatch(rel, g) for g in SECRET_EXEMPT):
        for pat, label in ptu.SECRETS:
            if re.search(pat, text):
                hits.append(f"{rel}: secret ({label})")
    if not any(fnmatch.fnmatch(rel, g) for g in PII_EXEMPT):
        label = ptu.pii_scan(text)  # same rules as the hook: spaced numbers joined, business allowlist honoured
        if label:
            hits.append(f"{rel}: PII ({label})")
    return hits


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if "--staged" in argv:
        files = git_files(True)
    elif "--all" in argv:
        files = git_files(False)
    else:
        files = [str(Path(a).resolve().relative_to(ROOT)) for a in argv]
    hits = [h for f in files for h in scan_file(f)]
    for h in hits:
        print("FAIL", h)
    print(f"scanned {len(files)} file(s): {'PASS' if not hits else 'FAIL'}")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
