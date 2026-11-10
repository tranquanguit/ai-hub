#!/usr/bin/env python3
"""Hot-context budget check (RULES R8, DESIGN.md#small-hot-context).

  python tools/budget.py              # estimate, print every always-loaded item, fail above budget
  python tools/budget.py --measure    # also MEASURE: headless run in the repo vs an empty dir (costs ~$0.01)

Always loaded by Claude Code (doc:cc-features-overview, doc:cc-skills): CLAUDE.md with @imports,
the name + description (+ when_to_use) of every skill, and every subagent's description.
Estimate: tokens ~= max(chars / 3.2, words * 1.5); Vietnamese diacritics make text token-dense,
so the estimate errs high. --measure gives the real number from the API usage fields.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
BUDGET = 6000
MAX_CLAUDE_LINES = 120
MAX_DESC = 200
DATE_RE = re.compile(r"\b20\d\d-\d\d-\d\d\b|\b\d{1,2}/\d{1,2}/20\d\d\b")


def est_tokens(text: str) -> int:
    return int(max(len(text) / 3.2, len(text.split()) * 1.5))


def expand_imports(path: Path, depth: int = 0) -> str:
    text = path.read_text(encoding="utf-8")
    if depth >= 4:
        return text
    out = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
        m = re.fullmatch(r"@(\S+)", line.strip())
        if m and not in_fence and (path.parent / m.group(1)).exists():
            out.append(expand_imports(path.parent / m.group(1), depth + 1))
        else:
            out.append(line)
    return "\n".join(out)


def frontmatter(path: Path) -> dict:
    m = re.match(r"^---\n(.*?)\n---", path.read_text(encoding="utf-8"), re.S)
    try:
        return yaml.safe_load(m.group(1)) or {} if m else {}
    except Exception:
        return {}


def items(root: Path = ROOT) -> list[tuple[str, int, str]]:
    rows = []
    cm = root / "CLAUDE.md"
    if cm.exists():
        rows.append(("CLAUDE.md (+@AGENTS.md)", est_tokens(expand_imports(cm)), ""))
    for sk in sorted((root / ".claude" / "skills").glob("*/SKILL.md")):
        fm = frontmatter(sk)
        text = f"{fm.get('name', sk.parent.name)}: {fm.get('description', '')} {fm.get('when_to_use', '')}"
        rows.append((f"skill:{sk.parent.name}", est_tokens(text), str(fm.get("description", ""))))
    for ag in sorted((root / ".claude" / "agents").glob("*.md")):
        fm = frontmatter(ag)
        rows.append((f"agent:{ag.stem}", est_tokens(f"{fm.get('name', '')}: {fm.get('description', '')}"), ""))
    return rows


def checks(root: Path = ROOT) -> list[str]:
    errs = []
    cm = root / "CLAUDE.md"
    if cm.exists():
        lines = cm.read_text().splitlines()
        if len(lines) > MAX_CLAUDE_LINES:
            errs.append(f"CLAUDE.md has {len(lines)} lines > {MAX_CLAUDE_LINES}")
        for f in (cm, root / "AGENTS.md"):
            if f.exists() and DATE_RE.search(f.read_text()):
                errs.append(f"{f.name} contains a date; keep hot files byte-stable (dynamic status belongs in SessionStart)")
    for sk in sorted((root / ".claude" / "skills").glob("*/SKILL.md")):
        d = str(frontmatter(sk).get("description", ""))
        if len(d) > MAX_DESC:
            errs.append(f"skill {sk.parent.name}: description {len(d)} chars > {MAX_DESC}")
    return errs


def measure(root: Path = ROOT, model: str = "haiku") -> dict:
    """Real always-loaded cost: input tokens of a 1-turn headless run in the repo minus in an empty dir."""
    def run(cwd: Path) -> int:
        r = subprocess.run(["claude", "-p", "Reply with OK.", "--output-format", "json", "--max-turns", "1",
                            "--model", model, "--no-session-persistence"],
                           cwd=cwd, capture_output=True, text=True, timeout=180, env=_env())
        u = json.loads(r.stdout)["usage"]
        return u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)
    with tempfile.TemporaryDirectory() as empty:
        base = run(Path(empty))
    repo = run(root)
    res = {"date": datetime.now(timezone.utc).isoformat(timespec="seconds"), "model": model, "repo_input_tokens": repo,
           "empty_dir_input_tokens": base, "always_loaded_measured": repo - base}
    out = root / "metrics" / "budget_measured.jsonl"
    with out.open("a") as fh:
        fh.write(json.dumps(res) + "\n")
    return res


def _env():
    import os
    e = dict(os.environ)
    e["LUNO_ROLE"] = e.get("LUNO_ROLE", "founder")
    return e


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--measure", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)
    rows = items()
    total = sum(t for _, t, _ in rows)
    if not a.quiet:
        for name, t, _ in rows:
            print(f"{t:>6}  {name}")
    print(f"{total:>6}  TOTAL always-loaded (estimate) / budget {BUDGET}")
    errs = checks()
    if total > BUDGET:
        errs.append(f"always-loaded estimate {total} > budget {BUDGET}")
    if a.measure:
        m = measure()
        print(f"{m['always_loaded_measured']:>6}  MEASURED always-loaded (repo {m['repo_input_tokens']} - empty {m['empty_dir_input_tokens']})")
        if m["always_loaded_measured"] > BUDGET:
            print("note: the measured number includes hook output and tool schemas for project subagents; "
                  "the budget applies to the estimate of authored text")
    for e in errs:
        print("FAIL", e)
    print("budget: PASS" if not errs else "budget: FAIL")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
