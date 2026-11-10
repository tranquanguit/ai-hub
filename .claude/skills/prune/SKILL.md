---
name: prune
description: Proposes archiving facts unused 90 days or more harmful than helpful, and skills unused 60 days; archives only after human approval, with reasons. Use in the weekly routine.
---
# prune

## When to use
- Weekly routine step 2, or when `memory/INDEX.md` grows past roughly 150 lines.
- Not to "clean up" facts you disagree with. Contradictions go through conflicts (R4).

## Inputs
- `memory/semantic/` counters (`used_count`, `helpful`, `harmful`, `last_used`, `last_verified`).
- `.claude/skills/*/stats.json` (`last_run`).

## Steps
1. `python3 tools/prune.py propose` writes `metrics/prune-proposal.md`, a checklist of facts and skills with reasons.
2. Show the proposal to the human and ask which items to archive. Archive nothing without an explicit yes.
3. On approval: `python3 tools/prune.py apply --facts a,b --skills x --reason "weekly prune <date>, approved by <role>"`. Facts move to `memory/archive/` with the reason; skills move to `.claude/skills-archive/`.
4. `python3 tools/promote.py index` (apply already re-indexes; this confirms).

## Memory facts used
- All facts' counters (read by the script, not by you).

## Verification
- `memory/INDEX.md` no longer lists the archived facts, and each archived file carries `archive_reason`. Save the proposal and the apply output to `evidence/`.

## Close
- `python3 tools/skill_stats.py record prune --result pass --scripted "propose,apply"`
