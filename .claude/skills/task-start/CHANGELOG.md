# task-start changelog

## 1.0.0 — 2026-11-10
- Why: initial meta-skill for the LunoBeau learning loop (Phase 4.2 of the build).
- Evidence: script tests in scripts/ pass at promotion (tools/promote.py skill gate); first real run recorded in stats.json.

## 1.1.0 — 2026-11-10
- Why: Same trajectory: task-start listed 'none found' for ops-review because it only scanned active skills; DeprecationWarning on re.sub count. Fix: list drafts (marked) and count= keyword.
- Trajectory evidence: tasks/2026-11-10-ops-review-w45/TASK.md (Relevant skills: none found)
- Eval before: script tests 2/2
- Eval after: script tests 2/2
