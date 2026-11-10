---
task: 2026-11-10-cs-training-pack
task_type: cs-training
role: founder
date: 2026-11-10
verification_passed: True
skills: ["cs-training", "task-close", "task-start"]
---
# Reflection: 2026-11-10-cs-training-pack

## What worked
- `build_pack.py` generated the product facts and a 16-question quiz with an answer key straight from the sheet (evidence/pack/), so the quiz can't contradict the sheet; check_training confirmed every answer appears (evidence/check_training.txt).
- Answering FAQs only from the sheet exposed three real gaps instead of inventing answers.

## What failed
- 2 reworks. (1) Hand-assembling the pack in an inline shell+python one-off lost 4 sections (missing f-prefix, unquoted heredoc expanded backticks). (2) The negated phrase 'không phải sản phẩm điều trị mụn' still trips the banned-claims check.

## Root cause
- No script for the deterministic assembly step (R7 candidate): the skill says 'paste unchanged' but gives no tool.
- No canonical compliant phrasing for acne questions; the checker is intentionally strict, but the repo did not tell me which phrasing passes.

## Tokens and turns
steps: scripted 3, reasoned 1, rework 2; tokens_in=None, tokens_out=None, cost=None, turns=None (empty = backfilled at SessionEnd)

## Questions I had to ask
- none
No live questions were asked. Three customer FAQs could not be answered from the repo (retinol pairing, lip-tint longevity/shade guide, combo discounts). The repo should hold these, so they are filed as question items for the Founder.

## Candidate facts
claims phrasing for acne questions (tool: checker output), free-shipping threshold [SAMPLE] (tool), 3 founder questions, and a cs-training skill-delta (assemble script).

## Candidate skill changes
- cs-training: add scripts/assemble_pack.py (facts + reasoned sections + quiz + answer key + summary → deliverable) and call it in step 3.
- cs-training references: a compliant-phrasing list for acne, whitening and tone-up questions.

Evidence: tasks/2026-11-10-cs-training-pack/evidence/check_training.txt, tasks/2026-11-10-cs-training-pack/evidence/pack
