---
type: skill-delta
key: skill.ops-review.target-consistency
claim: 'ops-review: script the target-consistency check (implied max CPA = AOV/roas_min)
  in compute_kpis.py and surface it in the report'
value: null
source: tasks/2026-11-10-ops-review-w45/LEDGER.md
confidence: medium
tags:
- ops-review
task: 2026-11-10-ops-review-w45
verification:
  kind: tool
  evidence: tasks/2026-11-10-ops-review-w45/evidence/target_consistency.txt
created: '2026-11-10'
---
Found by reasoning in w45; R7: deterministic arithmetic belongs in a script so later runs cannot miss it.
