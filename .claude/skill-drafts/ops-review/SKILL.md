---
name: ops-review
description: Reviews ads, SEO and customer-service exports for a period, computes KPIs and flags by script, and writes owned recommendations for strategy changes. Use for daily or weekly ops reviews.
---
# ops-review

## When to use
- Daily or weekly monitoring of ad campaigns (Facebook, TikTok, Google, Shopee), SEO rankings and CS effectiveness. Also before a phase-plan, to refresh benchmarks.
- Not for building a new phase plan (`phase-plan`) or for training (`cs-training`).

## Inputs
- An export folder (`inputs/<period>-ops-export/`) with `ads.csv`, `seo.csv`, `cs.csv` and `targets.json`. Column formats are in `scripts/compute_kpis.py`. Missing files are reported; review what exists.
- Targets in `targets.json`. If it is missing, use facts tagged `target` from `memory/INDEX.md`, otherwise ask once.

## Steps
1. Run `task-start --type ops-review`.
2. Compute **by script**: `python3 .claude/skills/ops-review/scripts/compute_kpis.py <export-dir> --out-json tasks/<task>/evidence/kpis.json --out-md tasks/<task>/evidence/kpis.md`. Log it `--scripted`. Never recompute KPIs by hand; quote numbers from `kpis.json`.
3. Diagnose each flag. For each flagged campaign, SEO drop and CS-flagged channel, state the most likely cause from the data (e.g. CTR low → creative or audience; CTR fine but CPA high → landing page or offer; weekend FRT spike → staffing). Mark causes you can't confirm from the data as hypotheses.
4. Write `tasks/<task>/deliverables/ops-review.md` in Vietnamese with these headings:
   `## Tóm tắt` (3–5 bullets), `## Quảng cáo` (paste the `kpis.md` ads table **unchanged** plus diagnosis; never retype numbers, because a retyped CS rate was wrong in w45), `## SEO`, `## CSKH`, `## Đề xuất` (numbered; **each line**: the flagged item's exact name, action, owner role (Founder/Marketing/Sales/CS), a number (budget change, target, deadline in days), and the metric to re-check), `## English summary`. Disclose SAMPLE data if used.
   - Any `skin_reaction_reports > 0` → a recommendation that says literally "báo Founder ca kích ứng da" (channel + date), as a product-safety follow-up.
   - If `kpis.md` shows **Target consistency: INCONSISTENT**, add a recommendation asking the Founder to reset the CPA target (memory: `ads.targets.cpa-roas-consistency`).
   - Budget moves must stay within the period's total unless the Founder approves (R13: outward-facing changes need approval; this report proposes, it doesn't execute).
5. Check: `python3 .claude/skills/ops-review/scripts/check_review.py tasks/<task>/deliverables/ops-review.md --kpis tasks/<task>/evidence/kpis.json > tasks/<task>/evidence/check_review.txt`. Fix any FAIL, log `--rework`, re-run.

## Memory facts used
- `memory/semantic/ads.targets.cpa-roas-consistency.md` (scripted in compute_kpis.py since v1.1.0).
- Facts tagged `ads`, `seo`, `cs`, `target` or `benchmark` in `memory/INDEX.md`. Verified benchmarks from past reviews make good candidates for later phase-plans.

## Verification
- `evidence/check_review.txt` ends with `=> PASS`, and LEDGER.md references it.

## Close
- `task-close --skills ops-review`, then `reflect`. Write benchmark candidates with `--kind tool --evidence tasks/<task>/evidence/kpis.json` (e.g. `ads.tiktok.roas_week`), and causes confirmed in a later review as facts.
