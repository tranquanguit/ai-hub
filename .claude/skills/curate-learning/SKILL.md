---
name: curate-learning
description: ACE curator pass over memory/inbox. Dedupes, checks verification, promotes facts as deltas, sets conflicts aside, rejects unverified items with reasons, rebuilds memory/INDEX.md. Use after reflect.
---
# curate-learning

## When to use
- After `reflect`, whenever `memory/inbox/` has items (SessionStart shows the count).
- In the weekly routine (OPERATIONS.md) to clear leftovers.
- Not to resolve conflicts. That needs the human (`promote.py resolve`).

## Inputs
- `memory/inbox/*.md` candidates in the promote format (written by `reflect.py candidate`).
- Existing `memory/semantic/` facts.

## Steps
1. Preview: `python3 tools/promote.py plan`. Each line shows the verdict the rules give: add, merge, conflict, reject, defer.
2. Check the preview for **false merges**: the same key used for different things. If you find one, give the candidate a more specific key with `reflect.py candidate` and reject the old item with `promote.py reject <item> --reason "re-keyed as <k>"`.
3. If a candidate reports that an existing fact **misled** a task (with evidence), run `promote.py bump <fact> --harmful --reason "<task>"`.
4. Run the pass: `python3 .claude/skills/curate-learning/scripts/curate.py --out tasks/<task>/evidence/curation.md`. If no task is open, use `--out metrics/curation-<date>.md`.
5. Read the report's Decisions table. For deferred `skill-delta` items, run `skill-forge`. For `question` items, answer them in `canon/` (human-owned) or turn them into a fact, then delete the question item.
6. For a large or contested batch, delegate steps 1–3 to the `curator` subagent.

## Memory facts used
- All of `memory/semantic/` via `memory/INDEX.md` (the script reads them; you only read the report).

## Verification
- The report's Lint section says `0 problems`. `memory/INDEX.md` lists every fact in `memory/semantic/`. Every rejection and conflict has a reason in `memory/curation-log.jsonl`.

## Close
- `python3 tools/skill_stats.py record curate-learning --result pass --scripted "curate.py"`
- If a fact used by a golden eval changed, run `eval-run`.
