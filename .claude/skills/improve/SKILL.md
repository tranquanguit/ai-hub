---
name: improve
description: One measured self-improvement step. Picks the worst metric, states a hypothesis, makes one change, runs evals before and after, keeps or reverts, and logs it in IMPROVEMENTS.md.
---
# improve

## When to use
- Weekly routine step 4, or when the human asks to make the repo faster, cheaper or more accurate.
- Exactly one change per run, so the effect can be attributed (2310.03714: optimise against a metric).

## Inputs
- `python3 tools/metrics.py --worst` (JSON: metric, gap, target).
- `python3 tools/metrics.py` (full report) and `python3 tools/skill_stats.py candidates` (R7 script candidates).

## Steps
1. Get the target: `python3 tools/metrics.py --worst`. If there is an R7 script candidate, it takes priority (it is cheap and deterministic).
2. Read the evidence behind it: the last 3 episodic notes of the affected task type and their LEDGER lines. Delegate to `researcher` if there are more than 3.
3. Write a hypothesis: "<change> will move <metric> from X toward <target> because <mechanism from the evidence>".
4. Baseline: `python3 evals/run_cold_start.py --task <affected golden task>` (or `--all`). Note the results path.
5. Make **one** change through the proper channel:
   - Skill change → the `skill-forge` flow (draft, test, changelog, eval, promote).
   - Fact change → a candidate plus `curate-learning`.
   - Rule change → propose it to the human; the hook asks for approval (R14).
6. After: re-run the same evals. Any regression → revert (delete the draft, or `promote.py archive` the fact). Never keep a regression (R6).
7. Log it: `python3 .claude/skills/improve/scripts/log_attempt.py --title ... --metric ... --hypothesis ... --change ... --before <path> --after <path> --decision kept|reverted --evidence <paths>`.

## Memory facts used
- Facts cited by the hypothesis (bump them `--used`).

## Verification
- `metrics/IMPROVEMENTS.md` has the new entry with before and after eval paths that exist. For a kept change, the after-run has no `REGRESSION` line.

## Close
- `python3 tools/skill_stats.py record improve --result pass|fail`
