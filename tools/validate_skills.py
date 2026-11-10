#!/usr/bin/env python3
"""Validate skills against the Agent Skills spec (doc:agent-skills-spec) plus repo rules (Phase 4.1).

  python tools/validate_skills.py                 # active skills in .claude/skills/
  python tools/validate_skills.py --drafts        # drafts in .claude/skill-drafts/
  python tools/validate_skills.py PATH [PATH...]  # specific skill dirs

Spec: name 1-64 chars, [a-z0-9-], no leading/trailing/double hyphen, equals directory name;
description 1-1024 chars. Repo (stricter): description <= 200 chars, body <= 300 lines, required
sections, stats.json schema, CHANGELOG.md, every referenced scripts/ or references/ file exists.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REQUIRED_SECTIONS = ["When to use", "Inputs", "Steps", "Memory", "Verification", "Close"]
STATS_KEYS = {"runs", "passes", "failures", "last_failure", "version"}
ALLOWED_FM = {"name", "description", "license", "compatibility", "metadata", "allowed-tools", "when_to_use",
              "argument-hint", "disable-model-invocation", "user-invocable", "model", "effort", "context", "agent",
              "paths", "arguments", "hooks", "disallowed-tools", "background", "shell"}


def validate(skill_dir: Path) -> list[str]:
    errs = []
    n = skill_dir.name
    sk = skill_dir / "SKILL.md"
    if not sk.exists():
        return [f"{n}: SKILL.md missing"]
    text = sk.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return [f"{n}: frontmatter must start on line 1 and be closed by ---"]
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except Exception as e:
        return [f"{n}: frontmatter YAML error: {e}"]
    body = m.group(2)
    name = str(fm.get("name", ""))
    if not (1 <= len(name) <= 64 and NAME_RE.match(name)):
        errs.append(f"{n}: invalid name '{name}' (lowercase letters, digits, single hyphens)")
    if name != n:
        errs.append(f"{n}: name '{name}' must equal directory name")
    desc = str(fm.get("description", "")).strip()
    if not desc:
        errs.append(f"{n}: description missing")
    elif len(desc) > 200:
        errs.append(f"{n}: description {len(desc)} chars > 200 (repo rule; spec max 1024)")
    unknown = set(fm) - ALLOWED_FM
    if unknown:
        errs.append(f"{n}: unknown frontmatter fields {sorted(unknown)}")
    if len(body.splitlines()) > 300:
        errs.append(f"{n}: body {len(body.splitlines())} lines > 300")
    heads = [h.strip().lower() for h in re.findall(r"^##+ (.+)$", body, re.M)]
    for s in REQUIRED_SECTIONS:
        if not any(h.startswith(s.lower()) or s.lower() in h for h in heads):
            errs.append(f"{n}: missing section '## {s}...'")
    for owner, ref in set(re.findall(r"(?:\.claude/skills/([a-z0-9-]+)/)?\b((?:scripts|references|assets)/[A-Za-z0-9_./-]+\.[a-z]{1,4})\b", body)):
        base = skill_dir if not owner or owner == n else ROOT / ".claude" / "skills" / owner
        if not (base / ref).exists() and not (skill_dir.parent / owner / ref).exists():
            errs.append(f"{n}: referenced file missing: {(owner + '/') if owner and owner != n else ''}{ref}")
    st = skill_dir / "stats.json"
    if not st.exists():
        errs.append(f"{n}: stats.json missing")
    else:
        try:
            missing = STATS_KEYS - set(json.loads(st.read_text()))
            if missing:
                errs.append(f"{n}: stats.json missing keys {sorted(missing)}")
        except Exception:
            errs.append(f"{n}: stats.json is not valid JSON")
    if not (skill_dir / "CHANGELOG.md").exists():
        errs.append(f"{n}: CHANGELOG.md missing")
    return errs


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if "--drafts" in argv:
        dirs = sorted(p for p in (ROOT / ".claude" / "skill-drafts").glob("*") if p.is_dir())
    elif argv:
        dirs = [Path(a) for a in argv]
    else:
        dirs = sorted(p for p in (ROOT / ".claude" / "skills").glob("*") if p.is_dir())
    errs = []
    for d in dirs:
        e = validate(d)
        errs += e
        print(f"{'ok  ' if not e else 'FAIL'} {d.name}")
    for e in errs:
        print("  -", e)
    print(f"skills validated: {len(dirs)}, problems: {len(errs)}")
    return 1 if errs or not dirs else 0


if __name__ == "__main__":
    sys.exit(main())
