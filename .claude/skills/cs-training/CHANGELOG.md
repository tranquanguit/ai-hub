# cs-training changelog

## 1.0.0 — 2026-11-10
- Why: domain skill for one of the founder's three most frequent tasks (intake answer 3).
- Evidence: script tests pass; first real run on the SAMPLE input recorded in tasks/; activated only after its golden eval passed in a fresh headless session (see evals/runs/).

## 1.1.0 — 2026-11-11
- Why: Trajectory 2026-11-10-cs-training-pack: hand assembly lost 4 sections; banned phrases quoted in negations failed the claims check (also in phase-plan and the cold baseline). Change: assemble_pack.py + never write banned phrases + acne phrasing fact. Result: first check 15/15 PASS (baseline first check failed on claims); remaining rework was a voluntary reviewer refinement; pass 1.0->1.0.
- Trajectory evidence: tasks/2026-11-10-cs-training-pack/LEDGER.md, memory/inbox/2026-11-10-skill-cs-training-assemble-script.md
- Eval before: evals/runs/2026-11-11/005246-baseline-drafts-v1.0.0/results.json
- Eval after: evals/runs/2026-11-11/010710-forge-v1.1.0-drafts/results.json
