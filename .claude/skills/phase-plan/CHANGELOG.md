# phase-plan changelog

## 1.0.0 — 2026-11-10
- Why: domain skill for one of the founder's three most frequent tasks (intake answer 3).
- Evidence: script tests pass; first real run on the SAMPLE input recorded in tasks/; activated only after its golden eval passed in a fresh headless session (see evals/runs/).

## 1.1.0 — 2026-11-11
- Why: Trajectory 2026-11-10-q1-2027-phase-plan: implied AOV and revenue gap computed ad hoc with python -c. Change: allocate_budget.py reports implied AOV and goal gap; goals block in brief template; no quoted banned phrases. Result: turns 40->35, tokens -4,838, rework 0->0, pass 1.0->1.0.
- Trajectory evidence: tasks/2026-11-10-q1-2027-phase-plan/LEDGER.md, memory/inbox/2026-11-10-skill-phase-plan-implied-aov.md
- Eval before: evals/runs/2026-11-11/005246-baseline-drafts-v1.0.0/results.json
- Eval after: evals/runs/2026-11-11/010710-forge-v1.1.0-drafts/results.json
