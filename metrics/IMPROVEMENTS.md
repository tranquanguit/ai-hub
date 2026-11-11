# Improvements log

Every self-improvement attempt (R6) and every RULES.md change (R14).

## 2026-11-10 — skill-forge: task-close/task-start v1.1.0 (draft stats, draft listing)
- Metric: stats completeness (runs recorded / real runs)
- Hypothesis: Recording stats for drafts used in real tasks makes stats.json complete; listing drafts in task-start removes 'none found' for draft task types
- Change: close_task.py records draft stats; start_task.py lists drafts; re.sub count= keyword
- Eval before: 3 real domain runs, 0 recorded (stats 0/3)
- Eval after: backfilled 3/3; new test_close_records_stats_for_draft_skill passes
- Decision: **kept**
- Evidence: tasks/2026-11-10-ops-review-w45/LEDGER.md, .claude/skills/task-close/CHANGELOG.md

## 2026-11-10 — skill-forge: skill-forge v1.0.1 (archive consumed deltas as applied)
- Metric: audit-trail accuracy
- Hypothesis: Separating applied from rejected inbox items keeps the curation log truthful
- Change: new promote.py applied; skill-forge step 7 uses it
- Eval before: consumed delta filed under archive/rejected
- Eval after: filed under archive/applied with applied_in
- Decision: **kept**
- Evidence: memory/curation-log.jsonl

## 2026-11-11 — skill-forge: curate-learning v1.0.1 (headless curation)
- Metric: questions_asked
- Hypothesis: Running curate.py in the main session in unattended runs removes the curator-permission question
- Change: curate-learning step 6 distinguishes interactive vs headless
- Eval before: evals/runs/2026-11-11/005246-baseline-drafts-v1.0.0/results.json: cs-training 1 question
- Eval after: next weekly eval (no golden change attributable yet)
- Decision: **kept**
- Evidence: .claude/skills/curate-learning/CHANGELOG.md

## 2026-11-11 — hook: guard shell redirects to $VAR paths near protected stores
- Metric: R3 enforcement coverage
- Hypothesis: A redirect whose target is a shell variable cannot be resolved by the hook; asking a human closes the bypass seen on 2026-11-10 (printf > $R/INVALID.md into evals/runs)
- Change: pre_tool_use.py: VARIABLE_GUARD_STORES -> ask; runner gets --invalidate so INVALID markers are script-written
- Eval before: bypass possible (observed)
- Eval after: hook tests 35/35 incl. variable-redirect ask + normal skill redirect allowed
- Decision: **kept**
- Evidence: .claude/hooks/tests/test_hooks.py

## 2026-11-11 — improve: domain skills v1.1.0 (worst metric: rework rate)
- Metric: rework_rate (ledger 3/3 tasks reworked; first_pass_rate 0)
- Hypothesis: Reworks come from (a) quoting banned phrases, (b) hand-done deterministic steps (assembly, retyping, ad-hoc arithmetic); scripting them and an explicit claims rule lowers rework without hurting pass rate
- Change: skill-forge v1.1.0 of ops-review, cs-training, phase-plan (one change per golden task, attributable)
- Eval before: evals/runs/2026-11-11/005246-baseline-drafts-v1.0.0/results.json
- Eval after: evals/runs/2026-11-11/010710-forge-v1.1.0-drafts/results.json
- Decision: **kept**
- Evidence: evals/runs/2026-11-11/010710-forge-v1.1.0-drafts/results.json

## Week 2026-W46 — build week summary
- Evals: clean baseline (005246) 3/3 PASS; v1.1.0 drafts (010710) 3/3 PASS, no regression. Three runs marked INVALID (workspace contamination, usage limit, container restart).
- Trends (cold-start, baseline → v1.1.0): ops-review cost 0.557 → 0.396 USD, tokens −80,654, rework 1 → 0; phase-plan turns 40 → 35; cs-training first check now passes (baseline failed on claims).
- Ledger (build session): 4 tasks, first-pass rate 0.0, rework rate 1.0, scripted-step ratio 0.83. Every build task needed at least one rework; the v1.1.0 skills target the causes.
- Kept: task-close/task-start v1.1.0, skill-forge v1.0.1, curate-learning v1.0.1, ops-review/cs-training/phase-plan v1.1.0, hook variable-redirect guard. Reverted: none.
- Prune: nothing to prune (all items < 1 day old).
- Papers: Mem0 (2504.19413) ingested as extra source 4/8; it informs DESIGN.md#conflicts (we keep set-aside instead of model-decided DELETE).
- Open for the founder: 2 incidents, 1 memory conflict (TikTok ROAS), 8 decisions in data/founder/decision-log.md, 2 skill deltas in memory/inbox/.
