#!/usr/bin/env python3
"""Read a Claude Code transcript (JSONL) and record tokens, turns and tool calls.

  python tools/session_stats.py --transcript <path> [--session ID] [--task TASKDIR] [--dry-run]

Appends one line to metrics/sessions.jsonl. If --task is given and that task's line in
metrics/ledger.jsonl has no token numbers yet, backfills them (the ledger line is written by
task-close, which runs before the session ends). Usage is de-duplicated by message id because
streamed assistant blocks repeat the same usage object.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SESSIONS = ROOT / "metrics" / "sessions.jsonl"
LEDGER = ROOT / "metrics" / "ledger.jsonl"


def task_window(task_dir: Path) -> tuple[str, str]:
    """(start, end) ISO timestamps from TASK.md `created` date and the first/last LEDGER.md step times (UTC)."""
    t = (task_dir / "TASK.md").read_text()
    day = re.search(r"^created:\s*(\S+)", t, re.M).group(1)
    times = re.findall(r"^- (\d\d:\d\d:\d\d) ", (task_dir / "LEDGER.md").read_text(), re.M)
    if not times:
        raise SystemExit(f"no timed ledger steps in {task_dir}")
    from datetime import date as _d, timedelta
    end_day = day
    if times[-1] < times[0]:  # ledger crossed midnight (UTC)
        end_day = (_d.fromisoformat(day) + timedelta(days=1)).isoformat()
    return f"{day}T{times[0]}", f"{end_day}T{times[-1]}"


def parse_transcript(path: Path, since: str | None = None, until: str | None = None) -> dict:
    usage_by_msg: dict[str, dict] = {}
    tool_calls = 0
    user_prompts = 0
    models = set()
    first_ts = last_ts = None
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            d = json.loads(line)
        except Exception:
            continue
        ts = d.get("timestamp")
        if since and (not ts or ts[:19] < since[:19]):
            continue
        if until and (not ts or ts[:19] > until[:19]):
            continue
        if ts:
            first_ts = first_ts or ts
            last_ts = ts
        if d.get("isSidechain"):
            pass  # subagent traffic is still cost; keep it
        msg = d.get("message") or {}
        if d.get("type") == "assistant":
            mid = msg.get("id") or d.get("uuid")
            if msg.get("usage"):
                usage_by_msg[mid] = msg["usage"]
            if msg.get("model"):
                models.add(msg["model"])
            for b in msg.get("content") or []:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    tool_calls += 1
        elif d.get("type") == "user":
            content = msg.get("content")
            if isinstance(content, str) and not d.get("isMeta"):
                user_prompts += 1
            elif isinstance(content, list) and any(isinstance(b, dict) and b.get("type") == "text" for b in content) \
                    and not any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
                user_prompts += 1
    tin = sum(u.get("input_tokens", 0) for u in usage_by_msg.values())
    cache_w = sum(u.get("cache_creation_input_tokens", 0) for u in usage_by_msg.values())
    cache_r = sum(u.get("cache_read_input_tokens", 0) for u in usage_by_msg.values())
    tout = sum(u.get("output_tokens", 0) for u in usage_by_msg.values())
    dur = None
    if first_ts and last_ts:
        try:
            dur = (datetime.fromisoformat(last_ts.replace("Z", "+00:00")) -
                   datetime.fromisoformat(first_ts.replace("Z", "+00:00"))).total_seconds()
        except Exception:
            pass
    return {"tokens_in": tin + cache_w + cache_r, "tokens_in_uncached": tin + cache_w, "cache_read": cache_r,
            "tokens_out": tout, "api_calls": len(usage_by_msg), "turns": user_prompts, "tool_calls": tool_calls,
            "models": sorted(models), "duration_s": dur}


def backfill_ledger(task: str, stats: dict) -> bool:
    if not LEDGER.exists():
        return False
    rows = [json.loads(l) for l in LEDGER.read_text().splitlines() if l.strip()]
    changed = False
    for r in rows:
        if r.get("task") == task and not r.get("tokens_in"):
            r.update({"tokens_in": stats["tokens_in"], "tokens_out": stats["tokens_out"],
                      "tool_calls": stats["tool_calls"], "turns": r.get("turns") or stats.get("api_calls"),
                      "token_source": "session_transcript"})
            changed = True
    if changed:
        LEDGER.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    return changed


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--transcript", required=True)
    ap.add_argument("--session", default="")
    ap.add_argument("--task", default="")
    ap.add_argument("--reason", default="")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--task-window", action="store_true",
                    help="count only transcript entries between the task's first and last LEDGER step")
    a = ap.parse_args(argv)
    p = Path(a.transcript).expanduser()
    if not p.exists():
        print(f"transcript not found: {p}", file=sys.stderr)
        return 1
    since = until = None
    if a.task_window and a.task:
        since, until = task_window(ROOT / "tasks" / a.task)
    stats = parse_transcript(p, since, until)
    if since:
        stats["window"] = f"{since}..{until}"
    row = {"date": datetime.now(timezone.utc).date().isoformat(), "session": a.session[:12], "task": a.task,
           "end_reason": a.reason, **stats}
    print(json.dumps(row))
    if a.dry_run:
        return 0
    SESSIONS.parent.mkdir(parents=True, exist_ok=True)
    with SESSIONS.open("a") as fh:
        fh.write(json.dumps(row) + "\n")
    if a.task:
        backfill_ledger(a.task, stats)
    return 0


if __name__ == "__main__":
    sys.exit(main())
