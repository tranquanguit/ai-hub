# Glossary: shared metrics (all roles)

Formulas match `.claude/skills/ops-review/scripts/compute_kpis.py`, so everyone uses the same definitions.

| Term | Formula | Note |
|---|---|---|
| CTR | clicks / impressions | below `ctr_min` → creative or audience issue |
| CPC | spend / clicks | VND |
| CPA | spend / conversions | VND per order |
| ROAS | revenue / spend | ≥ `roas_min` target |
| AOV | revenue / orders | a CPA × ROAS benchmark pair implies an AOV (`memory/semantic/ads.benchmarks.implied-aov.md`) |
| Max CPA consistent with ROAS | AOV / roas_min | targets must satisfy cpa_max ≥ AOV / roas_min (`ads.targets.cpa-roas-consistency`) |
| FRT | first response time (minutes) | SLA ≤ 15 min, 8:00–22:00 [SAMPLE policy] |
| CSAT | average satisfaction 1–5 | target ≥ 4.5 [SAMPLE] |
| Resolution rate | resolved / tickets | target ≥ 90% [SAMPLE] |
