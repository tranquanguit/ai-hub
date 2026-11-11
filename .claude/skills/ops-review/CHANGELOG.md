# ops-review changelog

## 1.0.0 — 2026-11-10
- Why: domain skill for one of the founder's three most frequent tasks (intake answer 3).
- Evidence: script tests pass; first real run on the SAMPLE input recorded in tasks/; activated only after its golden eval passed in a fresh headless session (see evals/runs/).

## 1.1.0 — 2026-11-11
- Why: Trajectory 2026-11-10-ops-review-w45: CPA/ROAS target inconsistency found only by reasoning; a retyped CS rate was wrong (87.5% vs 86.7%, caught by a cold-start read-back); cold baseline reworked on skin-escalation wording. Change: target_consistency scripted in compute_kpis.py, paste kpis.md unchanged, literal escalation phrase. Result: rework 1->0, cost 0.557->0.396 USD, tokens -80,654, pass 1.0->1.0.
- Trajectory evidence: tasks/2026-11-10-ops-review-w45/LEDGER.md, memory/inbox/2026-11-10-skill-ops-review-target-consistency.md, memory/inbox/2026-11-10-skill-ops-review-no-retyping.md
- Eval before: evals/runs/2026-11-11/005246-baseline-drafts-v1.0.0/results.json
- Eval after: evals/runs/2026-11-11/010710-forge-v1.1.0-drafts/results.json
