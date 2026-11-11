# OPERATIONS — weekly routine

Run this when the founder asks ("chạy weekly routine"), or on a schedule if one is set. Run it as a task (`task-start --type weekly-routine`) so it gets evidence, a ledger line and a reflection like any other work. Each step saves its output to the task's `evidence/`.

| # | Step | Command / skill | Evidence file |
|---|---|---|---|
| 1 | Eval all golden tasks | `eval-run`: `python3 evals/run_cold_start.py --all --label weekly` | `evals/runs/<date>/<time>-weekly/summary.md` → copy to `evidence/eval-summary.md` |
| 2 | Prune proposal | `prune`: `python3 tools/prune.py propose` → ask the founder → `prune.py apply ...` only for approved items | `evidence/prune-proposal.md` |
| 3 | Weekly metrics report | `python3 tools/metrics.py > evidence/metrics-report.md` | `evidence/metrics-report.md` |
| 4 | One improvement | `improve`: `python3 tools/metrics.py --worst` → hypothesis → one change → evals before and after → keep or revert | entry in `metrics/IMPROVEMENTS.md` |
| 5 | Research watch | Search arXiv (export API, `search_query=cat:cs.CL+OR+cat:cs.AI` with terms *agent memory*, *agent skills*, *context engineering*, *self-improving agents*, last 30 days). Propose **at most 3** papers, one sentence each on the gap they would fill. Ingest only what the founder approves (`paper-ingest`). | `evidence/research-watch.md` |
| 6 | Weekly summary | Append a `## Week <ISO week>` block to `metrics/IMPROVEMENTS.md`: eval deltas, metric trends (tokens, turns and questions should fall; pass rate and scripted ratio should rise), prune decisions, improvement kept or reverted, papers proposed and approved | `metrics/IMPROVEMENTS.md` |

Close with `task-close --skills eval-run,prune,improve`, then `reflect` and `curate-learning`.

## Ground rules for the routine
- Nothing outward-facing happens here. Ad budgets, posts and customer messages are proposals for the founder (R13).
- Any regression in step 1 is handled before step 4 (R6: revert first, improve later).
- Question items from evals (`memory/inbox/*eval-question*`) are gaps the repo should answer. Bring them to the founder in the summary.
- Open conflicts in `memory/conflicts/` and open incidents in `incidents/INCIDENTS.md` go at the top of the summary; only the founder resolves them.

## Scheduling (optional)
If the founder wants this to run automatically, create a scheduled task with this prompt:
"Run the weekly routine in OPERATIONS.md as role founder, and stop before any step that needs approval."
Suggested schedule: Monday morning, Vietnam time. The founder still approves prune and paper ingestion.
