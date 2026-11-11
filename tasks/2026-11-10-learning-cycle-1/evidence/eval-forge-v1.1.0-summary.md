# Cold-start eval evals/runs/2026-11-11/010710-forge-v1.1.0-drafts

commit 7973c99 | model sonnet

| task | passed | score | tokens in | tokens out | cost $ | turns | rework | questions | failed checks |
|---|---|---|---|---|---|---|---|---|---|
| cs-training (draft) | PASS | 1.0 | 687680 | 7524 | 0.5908213999999999 | 15 | 1 | 0 | – |
| ops-review (draft) | PASS | 1.0 | 1245027 | 13053 | 0.3963467 | 29 | 0 | 0 | – |
| phase-plan (draft) | PASS | 1.0 | 1530196 | 21987 | 0.5662042 | 35 | 0 | 0 | – |

## Comparison

- compared with evals/runs/2026-11-11/005246-baseline-drafts-v1.0.0/results.json
-   cs-training: passed True->True, score 1.0->1.0, turns 1->15, tokens Δ+623,607, cost 0.5001359->0.5908213999999999
-   ops-review: passed True->True, score 1.0->1.0, turns 30->29, tokens Δ-80,654, cost 0.5568337->0.3963467
-   phase-plan: passed True->True, score 1.0->1.0, turns 40->35, tokens Δ-4,838, cost 0.5252125->0.5662042
