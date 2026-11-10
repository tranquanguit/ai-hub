---
key: ads.targets.cpa_roas_consistency
claim: Ad targets are consistent only if cpa_max >= AOV / roas_min; otherwise CPA
  flags fire on campaigns that meet the ROAS target
value: cpa_max >= AOV/roas_min
source: tasks/2026-11-10-ops-review-w45/evidence/target_consistency.txt
confidence: high
created: '2026-11-10'
last_verified: '2026-11-10'
used_count: 0
helpful: 0
harmful: 0
tags:
- ads
- target
- ops-review
links: []
verification:
  kind: tool
  evidence: tasks/2026-11-10-ops-review-w45/evidence/target_consistency.txt
roles:
- all
---
Ad targets are consistent only if cpa_max >= AOV / roas_min; otherwise CPA flags fire on campaigns that meet the ROAS target
