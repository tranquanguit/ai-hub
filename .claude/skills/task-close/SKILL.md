---
name: task-close
description: Verifies an open task against its done-criteria, saves evidence, appends the metrics ledger and skill stats. Use when the deliverable is ready, before reflect.
---
# task-close

## When to use
- The deliverable for the open task exists and you believe the done-criteria are met.
- Not to abandon a task. In that case log `[rework]` or tell the user, then close with `--passed false`.

## Inputs
- The open task (`.claude/state/current_task`) with TASK.md done-criteria.
- The domain skill's checker script, if it has one (`check_*.py`).

## Steps
1. For each done-criterion, run the check that proves it: the domain checker, a test, or a file read-back. Save its **raw output** to `evidence/<name>.txt`. One file can cover several criteria. Plan the checks as independent verification questions, not a re-read of your own answer (2309.11495).
2. For criteria that need judgement, delegate to the `reviewer` subagent and save its table to `evidence/review.md`.
3. Log the verification: `python3 .claude/skills/task-start/scripts/start_task.py log "verify" "<check command>" "evidence/<file>: PASS|FAIL" --scripted`.
4. If a check fails, fix it, log `--rework`, and re-run steps 1–3. Never edit evidence by hand.
5. Run `python3 .claude/skills/task-close/scripts/close_task.py --passed true|false --skills <domain-skill>`. Add `--tokens-in/--tokens-out/--cost/--turns` when known (headless JSON); otherwise the SessionEnd hook backfills tokens.
6. Tick the done-criteria in TASK.md (`- [x]`).

## Memory facts used
- None directly. This skill produces the evidence that later promotes facts (R2).

## Verification
- `close_task.py` exits 1 if `evidence/` is empty or LEDGER.md doesn't reference an evidence file (R1). On success it appends one line to `metrics/ledger.jsonl` and updates `stats.json` for each skill used.

## Close
- Continue with the `reflect` skill. The Stop hook blocks stopping until the reflection exists.
