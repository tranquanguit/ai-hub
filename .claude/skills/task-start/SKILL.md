---
name: task-start
description: Opens a task folder with goal, scope, checkable done-criteria, relevant skills, facts and past episodes. Use at the start of any request that should produce a deliverable.
---
# task-start

## When to use
- Any request that produces a deliverable (plan, training pack, report, content, analysis).
- Not for quick questions answered in one reply, or when a task for this request is already open (check SessionStart status).

## Inputs
- The user's request, restated as one goal sentence.
- Task type: the name of the domain skill that fits (`phase-plan`, `cs-training`, `ops-review`), or a new short type.
- Confirmed session role (R17). If the role is not set, ask first.
- Input files the user named, under `inputs/` or `data/<role>/`.

## Steps
1. Turn the request into 2–5 **checkable** done-criteria. Each must be verifiable by a script, a file check or the human. Example: "budget table sums to the brief total" rather than "good plan".
2. Run `python3 .claude/skills/task-start/scripts/start_task.py --slug <short-slug> --type <type> --goal "<goal>" --criterion "<c1>" --criterion "<c2>" --input <path>`. It creates `tasks/<date>-<slug>/` (TASK.md, LEDGER.md, evidence/), sets the current-task pointer, and lists relevant skills, facts and past episodes.
3. Read only the listed fact files and the most recent past episode. Each one you use: `python3 tools/promote.py bump <slug> --used`.
4. If something the task needs is missing (budget, date range, audience), ask the user **one** grouped question and log it: `start_task.py log "clarify" "asked user: <q>" "<answer>" --question`.
5. Log every later step with `start_task.py log "<intent>" "<action>" "<observation>"`, adding `--scripted` when a script did it.

## Memory facts used
- `memory/INDEX.md` (generated; ranked by recency + importance).
- Past episodes in `memory/episodic/` with the same `task_type`.

## Verification
- `TASK.md` exists with at least one done-criterion and `role:` set; LEDGER.md exists. The script exits non-zero otherwise.

## Close
- Nothing to close here. The pipeline continues with the domain skill, then `task-close`. Skill stats for task-start are recorded by task-close (`skills_used`).
