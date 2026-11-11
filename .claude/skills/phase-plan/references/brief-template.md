# Brief template for phase-plan

Copy into `inputs/<phase>-brief.md` and fill in. Benchmarks should come from the last ops-review
(`tasks/*/evidence/kpis.json`) or from verified memory facts, not guesses.

```yaml
phase: Q?-YYYY
months: ["YYYY-MM", "YYYY-MM", "YYYY-MM"]
month_weights: [0.30, 0.33, 0.37]   # must sum to 1
total_budget_vnd: 0
reserve_pct: 0.10
channels:
  facebook_ads:  {cpa: 0, roas: 0, weight: 1.0, min_share: 0.0, max_share: 1.0}
  tiktok_ads:    {cpa: 0, roas: 0, weight: 1.0, min_share: 0.0, max_share: 1.0}
regions:
  ho_chi_minh: {share_of_orders_last_q: 0}
audiences_last_q:
  segment_name: {share: 0, aov_vnd: 0}
```

Goals section: revenue (VND), orders, any retention target. Constraints: channels that must or must not be used.
