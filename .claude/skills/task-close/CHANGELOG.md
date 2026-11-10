# task-close changelog

## 1.0.0 — 2026-11-10
- Why: initial meta-skill for the LunoBeau learning loop (Phase 4.2 of the build).
- Evidence: script tests in scripts/ pass at promotion (tools/promote.py skill gate); first real run recorded in stats.json.

## 1.1.0 — 2026-11-10
- Why: Trajectory 2026-11-10-ops-review-w45: close_task reported skills=ops-review but stats were not recorded because ops-review was a draft; Python 3.13 DeprecationWarning on re.sub count. Fix: record draft stats, count= keyword. Hypothesis: every real run is counted (stats complete).
- Trajectory evidence: tasks/2026-11-10-ops-review-w45/LEDGER.md, memory/inbox/2026-11-10-skill-task-close-draft-stats.md
- Eval before: no golden task for task-close; script tests 3/3
- Eval after: script tests 4/4 incl. new test_close_records_stats_for_draft_skill; no-regression golden run recorded in CHANGELOG of ops-review v1.1.0
