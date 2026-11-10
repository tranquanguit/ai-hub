# skill-forge changelog

## 1.0.0 — 2026-11-10
- Why: initial meta-skill for the LunoBeau learning loop (Phase 4.2 of the build).
- Evidence: script tests in scripts/ pass at promotion (tools/promote.py skill gate); first real run recorded in stats.json.

## 1.0.1 — 2026-11-10
- Why: Consumed skill-deltas were archived via 'reject', which reads as refused in the audit trail (learning-cycle-1). Step 7 now uses the new 'promote.py applied'.
- Trajectory evidence: memory/curation-log.jsonl (re-filed entry), tasks/2026-11-10-learning-cycle-1/LEDGER.md
- Eval before: no golden task; script tests 2/2
- Eval after: script tests 2/2; validator 0 problems
