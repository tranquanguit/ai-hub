# curate-learning changelog

## 1.0.0 — 2026-11-10
- Why: initial meta-skill for the LunoBeau learning loop (Phase 4.2 of the build).
- Evidence: script tests in scripts/ pass at promotion (tools/promote.py skill gate); first real run recorded in stats.json.

## 1.0.1 — 2026-11-11
- Why: Cold-start run evals/runs/2026-11-11/005246-baseline-drafts-v1.0.0 (cs-training): the curator subagent was denied Bash in headless mode, curation stalled and the agent asked the user (1 question). Step 6 now runs curate.py in the main session when unattended.
- Trajectory evidence: evals/runs/2026-11-11/005246-baseline-drafts-v1.0.0/cs-training/claude_output.json
- Eval before: evals/runs/2026-11-11/005246-baseline-drafts-v1.0.0/results.json (cs-training questions=1)
