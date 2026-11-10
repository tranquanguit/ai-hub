---
name: reflect
description: Writes the episodic reflection for a closed task (what worked, what failed, root cause, cost, questions) and files candidate facts and skill deltas into memory/inbox. Use right after task-close.
---
# reflect

## When to use
- Right after `task-close`, success or failure. Failed tasks teach the most (2308.10144).
- Not for open tasks. Close first so the ledger line exists.

## Inputs
- The current task folder (TASK.md, LEDGER.md, evidence/).
- Its line in `metrics/ledger.jsonl` (written by task-close).

## Steps
1. `python3 .claude/skills/reflect/scripts/reflect.py new` writes `memory/episodic/<task>.md` with facts pre-filled (steps, tags, tokens, questions, evidence list).
2. Fill each TODO briefly and concretely, citing evidence files. Root cause names a **mechanism** (missing fact, unclear step, no script, wrong input), not "be more careful" (2303.11366).
3. For each reusable lesson, write a candidate. Use one fact per candidate and a stable `key` (e.g. `ads.tiktok.cpa_target`):
   `reflect.py candidate --key <k> --claim "<one sentence>" --value <v> --source <path|url> --kind test|tool|eval|human --evidence <path> --tags a,b`.
   - `--kind self` is allowed but will be **rejected** at curation (R2). Use it only to record an idea worth testing later.
   - Questions the repo should have answered → `--type question`.
   - Procedure changes → `--type skill-delta` with the skill name in `--tags` and the concrete delta in `--detail`.
4. List the inbox files you wrote under "Candidate facts" / "Candidate skill changes".
5. `reflect.py finish` checks no TODO is left, marks the task `done` and clears the current-task pointer.

## Memory facts used
- None; this skill produces candidates. Never write `memory/semantic/` (R3, the hook blocks it).

## Verification
- `reflect.py finish` exits 0 only when all seven sections are filled. Every candidate with `kind` other than `self` points to an existing evidence file (checked again by `tools/promote.py`).

## Close
- `python3 tools/skill_stats.py record reflect --result pass`
- Next: `curate-learning`.
