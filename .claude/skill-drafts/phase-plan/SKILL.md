---
name: phase-plan
description: Builds a phase business plan for LunoBeau (channels, focus regions, audiences, budget by channel and month, channel strategies, KPIs, timeline, risks) from a brief. Use for planning a sales phase.
---
# phase-plan

## When to use
- The founder or marketing asks for a plan for a sales phase: launch, scale-up, a seasonal campaign (Tết, 11.11, 12.12).
- Not for daily optimisation of running campaigns (use `ops-review`) or for one post or ad (content work).

## Inputs
- A brief with goals and a ```yaml params block: `total_budget_vnd`, `reserve_pct`, `months`, `month_weights`, `channels` with benchmark `cpa`/`roas`/`weight`/`min_share`/`max_share`, `regions`, `audiences_last_q`. Template: `references/brief-template.md`. If the brief has no params block, ask once for budget, months and last-quarter benchmarks, then write the block.
- `canon/company.md` (products, prices, channels, claims policy).

## Steps
1. Run `task-start` with `--type phase-plan`. Copy the brief into `evidence/` when it comes from chat.
2. Allocate the budget **by script**: `python3 .claude/skills/phase-plan/scripts/allocate_budget.py <brief> --json tasks/<task>/evidence/allocation.json --md tasks/<task>/evidence/allocation.md`. Log it `--scripted`. Never redo this arithmetic by hand.
3. Compare the script's expected revenue and orders with the brief's goals. If there is a gap, the plan must say so and give 2–3 concrete levers with their numeric effect (e.g. AOV via combos, repeat purchase, shifting reserve to the best-ROAS channel). Never stretch benchmarks to hide a gap.
4. Write the plan to `tasks/<task>/deliverables/phase-plan.md` in Vietnamese, with these headings (the checker looks for them):
   `## Kênh bán hàng`, `## Khu vực trọng điểm`, `## Khách hàng mục tiêu`, `## Ngân sách` (paste `allocation.md` unchanged), `## Chiến lược theo kênh` (one `###` per allocated channel: objective, audience, offer, creative angle, KPI), `## KPI` (numeric targets per month), `## Lịch triển khai`, `## Rủi ro`, `## Giả định & nguồn` (every benchmark → its source; SAMPLE inputs disclosed), `## English summary` (5–8 lines).
   - Regions and audiences: rank them with the brief's shares, and cite the share you used.
   - Claims follow `canon/company.md#claims`.
5. Check: `python3 .claude/skills/phase-plan/scripts/check_plan.py tasks/<task>/deliverables/phase-plan.md --alloc tasks/<task>/evidence/allocation.json > tasks/<task>/evidence/check_plan.txt`. Fix any FAIL, log `--rework`, re-run.
6. For a real (non-SAMPLE) plan, ask the `reviewer` subagent to check strategy coherence against done-criteria; save the result to `evidence/review.md`.

## Memory facts used
- Facts tagged `phase-plan`, `channel` or `benchmark` in `memory/INDEX.md` (benchmarks verified by past ops-reviews beat brief guesses; cite them).

## Verification
- `evidence/check_plan.txt` ends with `=> PASS`, and LEDGER.md references it. The budget total equals the brief total exactly (scripted).

## Close
- `task-close --skills phase-plan`, then `reflect`. Good candidates: benchmark corrections (`--kind tool` with ops-review evidence), questions you had to ask (`--type question`).
- `python3 tools/skill_stats.py record` is done by task-close. Name reasoned steps in the LEDGER so R7 can spot repeats.
