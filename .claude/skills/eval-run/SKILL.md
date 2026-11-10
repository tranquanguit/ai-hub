---
name: eval-run
description: Runs golden tasks in fresh headless sessions (evals/run_cold_start.py), records pass, tokens, cost, turns and questions, and compares with the previous run. Use after a skill or fact change.
---
# eval-run

## When to use
- After a skill or memory fact used by a golden task changed (pipeline step 5), in the weekly routine, and before promoting a skill draft (R6).
- Not as a substitute for the task's own verification. Golden tasks are fixed regression checks.

## Inputs
- Which golden tasks: one name from `evals/golden/` or `--all`.
- Optional `--use-draft <skill>` to test a skill draft in place of the active skill.

## Steps
1. Run `python3 evals/run_cold_start.py --all` (or `--task <name>`). Each task runs in a throwaway git worktree of HEAD with `claude -p --output-format json`, no history, role from `LUNO_ROLE`. Deterministic graders (`evals/golden/<name>/grade.py`) score the output.
2. The script writes `evals/runs/<date>/results.json` and `summary.md`, then compares with the previous run (`--compare` is on by default). Any pass→fail or score drop prints `REGRESSION` and exits 1.
3. Questions the agent asked during a run are written as `type: question` inbox items. They mark gaps the repo should have answered. Curate them.
4. If a grader needs judgement (tone, persuasiveness), use the judge protocol in `references/judge-protocol.md`: rubric plus reference answer, both orders, and a tie when the orders disagree (2306.05685).
5. On regression: revert the change that caused it (R6) and log the attempt in `metrics/IMPROVEMENTS.md`.

## Memory facts used
- None directly. Golden inputs live in `evals/golden/<name>/`.

## Verification
- `evals/runs/<date>/results.json` exists with one result per task (passed, score, tokens_in/out, cost, turns, questions). Copy `summary.md` to the current task's `evidence/`.

## Close
- `python3 tools/skill_stats.py record eval-run --result pass|fail --scripted "run_cold_start,grade,compare"`
