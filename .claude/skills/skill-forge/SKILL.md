---
name: skill-forge
description: Creates or updates a skill from real task trajectories, gated by golden evals in a fresh session; regressions are reverted. Use after curation when deltas, repeats or script candidates exist.
---
# skill-forge

## When to use
- `forge.py candidates` lists something:
  - a task type that succeeded twice without its own skill (new skill, 2409.07429),
  - a `skill-delta` inbox item with evidence,
  - an R7 script candidate (a reasoned step repeated 3 or more times).
- Not for speculative skills with no trajectory behind them (2305.16291: only verified skills enter the library).

## Inputs
- `python3 .claude/skills/skill-forge/scripts/forge.py candidates` output.
- The trajectories: `tasks/<id>/LEDGER.md`, `evidence/`, and episodic notes for those tasks.

## Steps
1. Run `forge.py candidates` and pick **one** candidate. Write the hypothesis in one line: "Adding X will make Y pass / cost less".
2. Run `forge.py draft <name>` to copy the active skill, or `forge.py draft <name> --new`. Edit **only the draft** in `.claude/skill-drafts/<name>/`.
   - Make deltas, not rewrites (R5): add or adjust specific steps and keep working steps verbatim.
   - New deterministic step → a script in `scripts/` plus `scripts/test_<x>.py`. Run `python3 -m pytest -q .claude/skill-drafts/<name>/scripts`.
   - New skill: induce steps from the shared actions in its 2 or more successful LEDGERs (workflow induction); `description` under 200 chars.
3. `python3 tools/validate_skills.py .claude/skill-drafts/<name>` must print `problems: 0`.
4. Eval the **draft** cold: `python3 evals/run_cold_start.py --task <name> --use-draft <name>`. Compare with the last run of the active skill (`--compare`). If the skill has no golden task, create one under `evals/golden/<name>/` from a real input first (Phase 7 format).
5. Record it: `forge.py changelog <name> --version <x.y.z> --why "<hypothesis + result>" --evidence <ledger/episode path> --eval-before <results.json> --eval-after <results.json>`.
6. Promote: `python3 tools/promote.py skill <name> --eval <after results.json>`. Promotion refuses on any failing golden result (R6). If refused, delete the draft (`rm -r .claude/skill-drafts/<name>`, which needs human approval), log the attempt in `metrics/IMPROVEMENTS.md` as **reverted**, and stop.
7. Archive the inbox `skill-delta` items you consumed: `python3 tools/promote.py applied <item> --where "<name> v<x.y.z>"` (not `reject`: the delta was used, not refused).

## Memory facts used
- Facts referenced by the skill's own "Memory facts used" section.

## Verification
- Evidence: the after-eval `results.json` plus the CHANGELOG entry that cites it. Save `forge.py candidates` output and the eval comparison to the current task's `evidence/`.

## Close
- `python3 tools/skill_stats.py record skill-forge --result pass|fail`
- Append the attempt to `metrics/IMPROVEMENTS.md` (hypothesis, change, eval before/after, kept or reverted).
