---
task: 2026-11-10-learning-cycle-1
task_type: learning-cycle
role: founder
date: 2026-11-11
verification_passed: True
skills: ["curate-learning", "eval-run", "improve", "paper-ingest", "prune", "skill-forge", "task-close", "task-start"]
---
# Reflection: 2026-11-10-learning-cycle-1

## What worked
- curate.py promoted 6 tool-verified facts, set aside the TikTok ROAS contradiction (3.6 brief vs 1.2 measured) with both sources, and rejected a self-assessed hypothesis (evidence/curation.md).
- Frozen graders + cold-start runs gave an external signal for every skill change: baseline 3/3 PASS, v1.1.0 3/3 PASS with ops-review rework 1->0 and cost -29% (evidence/eval-*-summary.md).
- Cold sessions found things I missed: a retyped number (87.5% vs 86.7%) and a headless curator permission gap.

## What failed
- Two eval runs were invalid: the first had old task folders in the workspace (contamination), the second hit the usage limit; a third was killed by a container restart. All are marked INVALID and excluded from comparisons.
- My own hook edit (missing `import os`) made Write/Edit guards fail open for a few minutes; caught on the next check and covered by a test.
- close_task.py recorded stats for skills whose own Close step had already recorded them, so some runs are double-counted.

## Root cause
- Eval isolation was under-specified (no rule that tasks/ must be empty), and errored sessions were not distinguished from skill failures. Both are now in run_cold_start.py.
- Stats recording has two owners (each skill's Close step and task-close) and no dedupe.
- Hook code had no test for the outside-repo branch until it broke.

## Tokens and turns
steps: scripted 10, reasoned 0, rework 1; tokens_in=None, tokens_out=None, cost=None, turns=None (empty = backfilled at SessionEnd)

## Questions I had to ask
- none
The only cold-start question came from the headless curator denial, which the repo should handle itself. Fixed in curate-learning v1.0.1. Product questions are routed to data/founder/decision-log.md.

## Candidate facts
ops.headless.subagent-bash-denied (tool), skill-delta for task-close stats dedupe, skill-delta for paper-ingest affects.py ranking.

## Candidate skill changes
- task-close: record stats only for skills whose stats were not already updated during this task (check last_run >= task created), or drop self-recording from skill Close steps.
- paper-ingest: affects.py should weight a card's adopted_in anchors and ignore generic words (memory, evidence, fact); it ranked memory-tiers above the adopted conflicts decision for Mem0.

Evidence: tasks/2026-11-10-learning-cycle-1/evidence/curation.md, tasks/2026-11-10-learning-cycle-1/evidence/eval-baseline-summary.md, tasks/2026-11-10-learning-cycle-1/evidence/eval-forge-v1.1.0-summary.md, tasks/2026-11-10-learning-cycle-1/evidence/forge_candidates.json, tasks/2026-11-10-learning-cycle-1/evidence/paper-ingest-affects.txt, tasks/2026-11-10-learning-cycle-1/evidence/paper-ingest-check.txt, tasks/2026-11-10-learning-cycle-1/evidence/prune-proposal.txt
