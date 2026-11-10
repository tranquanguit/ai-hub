# LLM-judge protocol (only for what scripts cannot check)

Source: 2306.05685 (position bias, verbosity bias, self-enhancement; mitigations: swap positions,
reference-guided grading, few-shot rubric). Deterministic graders always run first; the judge
never overrides a deterministic FAIL.

1. **Rubric**: 3–5 criteria, each scored 1–5 with an anchor sentence for 1, 3 and 5.
2. **Reference**: a reference answer written or approved by the human (`evals/golden/<task>/reference.md`).
3. **Pairwise, both orders**: compare candidate vs reference as (A=candidate, B=reference) and (A=reference, B=candidate).
   - If the two verdicts disagree → record a tie (position bias detected).
   - Score = mean over both orders.
4. **Judge model**: a different model tier from the one that produced the answer (reduces self-enhancement), via
   `claude -p --model sonnet --output-format json` with the rubric, reference and candidate in the prompt.
5. **Length control**: tell the judge that length is not a criterion; record the candidate's word count next to the score.
6. Store the raw judge JSON for both orders in `evals/runs/<date>/<task>/judge-*.json`.
