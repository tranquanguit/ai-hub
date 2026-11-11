---
type: skill-delta
key: skill.phase-plan.implied-aov
claim: 'phase-plan: allocate_budget.py should output implied AOV per channel and the
  expected-vs-goal revenue/orders gap'
value: null
source: tasks/2026-11-10-q1-2027-phase-plan/LEDGER.md
confidence: medium
tags:
- phase-plan
task: 2026-11-10-q1-2027-phase-plan
verification:
  kind: tool
  evidence: tasks/2026-11-10-q1-2027-phase-plan/evidence/implied_aov.txt
created: '2026-11-10'
applied: '2026-11-11'
applied_in: phase-plan v1.1.0
---
Computed ad hoc with python -c in this task; same arithmetic as ops-review target consistency.
