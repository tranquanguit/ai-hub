#!/usr/bin/env python3
"""Set the confirmed role for the current Claude Code session (RULES R17).

  python tools/set_role.py <founder|sales|marketing|cs> [--session ID]

The session id comes from --session or $CLAUDE_CODE_SESSION_ID / $CLAUDE_SESSION_ID. The role is
stored in .claude/state/roles/<session> (gitignored) and read by the PreToolUse hook.
Only the human states the role; the agent runs this after the user confirms it.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main(argv=None) -> int:
    roles = json.loads((ROOT / "canon" / "roles" / "ROLES.json").read_text())["roles"]
    ap = argparse.ArgumentParser()
    ap.add_argument("role", choices=sorted(roles))
    ap.add_argument("--session", default=os.environ.get("CLAUDE_CODE_SESSION_ID") or os.environ.get("CLAUDE_SESSION_ID"))
    a = ap.parse_args(argv)
    if not a.session:
        print("No session id found; pass --session <id> (shown in hook input) or set LUNO_ROLE for headless runs.")
        return 2
    d = ROOT / ".claude" / "state" / "roles"
    d.mkdir(parents=True, exist_ok=True)
    (d / a.session).write_text(a.role)
    r = roles[a.role]
    print(f"role={a.role} data_areas={','.join(r['data_areas'])} private={r.get('private', False)} canon=canon/roles/{a.role}.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
