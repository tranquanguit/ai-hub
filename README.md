# ai-hub — LunoBeau's AI operating repo

LunoBeau (Vietnamese cosmetics brand: outsourced manufacturing, in-house distribution and sales) hands real work to Claude Code agents from this repo: phase plans, customer-service training and daily ops reviews of ads, SEO and CS. The repo is built to get **more accurate, faster and cheaper with use**. Every task leaves evidence, a reflection and verified lessons, and skills and memory improve only when an external check proves the change helps.

## Five-minute tour

| You want to… | Look at |
|---|---|
| Know the rules and why they exist | `RULES.md` (each rule: why, how it's enforced, exception) |
| Know why the repo is shaped this way | `DESIGN.md` (each decision cites a paper card or doc page) |
| See what the agent knows | `memory/INDEX.md` (verified facts), `canon/company.md` (company facts, human-owned) |
| See past work | `tasks/<date>-<slug>/` (TASK.md, LEDGER.md, evidence/, deliverables/) |
| See what it learned | `memory/episodic/` (reflections), `memory/curation-log.jsonl`, `metrics/IMPROVEMENTS.md` |
| See whether it is improving | `python3 tools/metrics.py`, `evals/runs/*/*/summary.md` |
| Run the weekly routine | `OPERATIONS.md` |
| Read the research | `library/INDEX.md` → `library/cards/` |

## How a session works
1. **SessionStart hook** prints at most 5 status lines: open incidents (first), session role, inbox and conflict counts, failing evals, open task.
2. **Role first.** The agent asks once which role you work in (Founder, Sales, Marketing, CS), then runs `tools/set_role.py`. `data/` stays closed until then, and each role sees only its own `data/<area>/` (`canon/roles/ROLES.json`).
3. **Every deliverable follows one pipeline:** `task-start → domain skill → verify → task-close → reflect → curate-learning → (skill-forge) → (eval-run)`.
4. **Hooks enforce the hard rules**; they don't depend on the model's memory:
   - PreToolUse blocks destructive commands, data leaving the repo, secrets, customer PII outside `data/*/private/`, cross-role paths and direct writes to memory or skills.
   - Stop won't let a task end without evidence and a reflection.
   - PreCompact saves state to the task ledger.
   - SessionEnd records token usage.

## Skills (`.claude/skills/`)
- **Domain:** `phase-plan`, `cs-training`, `ops-review`. Arithmetic and checks are scripts; strategy and writing are the model's job.
- **Meta:** `task-start`, `task-close`, `reflect`, `curate-learning`, `skill-forge`, `eval-run`, `prune`, `improve`, `paper-ingest`.
- Each skill has `SKILL.md`, `scripts/` (with tests), `references/`, `stats.json` (runs and failures, never loaded into context) and `CHANGELOG.md` (why each version changed, with eval evidence).
- New or changed skills are written in `.claude/skill-drafts/` and activated only by `tools/promote.py skill`. That command runs the validator and the script tests, and requires a passing golden eval when the skill has one.

## Memory (`memory/`)
- `semantic/`: one verified fact per file. Written only by `tools/promote.py` after an external check (test, tool, eval or human).
- `episodic/`: one reflection per task.
- `inbox/`: candidates. `conflicts/`: contradictions, never auto-resolved. `archive/`: rejected, applied or pruned items, each with a reason.

## Quick commands

```bash
python3 -m pytest -q tools .claude/hooks .claude/skills
```

```bash
python3 tools/budget.py
```

```bash
python3 tools/metrics.py
```

```bash
python3 evals/run_cold_start.py --all
```

```bash
python3 tools/acceptance.py
```

One-time setup per clone (pre-commit gate):

```bash
git config core.hooksPath .githooks
```

## Inputs and data
- Drop exports and briefs in `inputs/`. Files named `SAMPLE-*` are synthetic and were created during the build; replace them with real ones.
- Raw customer data goes **only** in `data/cs/private/` (gitignored). Use pseudonyms (`KH-0012`) everywhere else.

## Blocked or pending (needs the founder)
- Real inputs for the three frequent tasks (currently SAMPLE).
- Answers to the open questions in `memory/inbox/` (`type: question`), and the open conflict in `memory/conflicts/`.
- Review of `incidents/INCIDENTS.md` (one build-time incident is open).
