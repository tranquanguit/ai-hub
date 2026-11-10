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
