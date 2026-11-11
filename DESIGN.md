# DESIGN — why this repo is shaped the way it is

Every decision lists **Decision**, **Rejected alternative**, and **Evidence**. Evidence cites a paper card (`library/cards/<id>.md`) or a doc page (`doc:<manifest id>`, URL in `library/MANIFEST.csv`). `tools/acceptance.py` checks that every decision here has a citation or a one-line justification.

Reading guide: the loop is in [learning-loop](#learning-loop), memory layout in [memory-tiers](#memory-tiers), and enforcement in RULES.md.

---

## memory-tiers
**Decision.** Map CoALA's four memories onto what Claude Code actually loads:

| CoALA memory | Here | Loaded |
|---|---|---|
| Working | context window + `tasks/<task>/LEDGER.md` | always / on demand |
| Procedural | `.claude/skills/*/SKILL.md` + `scripts/` | names + descriptions always, body on invoke, scripts executed not read |
| Semantic | `memory/semantic/*.md`, via `memory/INDEX.md` | on demand, one fact per file |
| Episodic | `memory/episodic/*.md` | on demand (task-start greps by tags) |
| Archival / cold | `library/full/`, `memory/archive/` | only by `paper-ingest` or on request |
| Rules (hot) | `CLAUDE.md` → `@AGENTS.md` | always |

**Rejected.** A single growing CLAUDE.md or MEMORY.md holding everything. It costs tokens every turn, degrades with length, and mixes verified and unverified knowledge.
**Evidence.** 2309.02427 (memory types + decision loop); 2310.08560 (hot/cold tiers with paging); 2404.13501 (taxonomy check: sources, forms, operations all covered); doc:cc-features-overview and doc:cc-memory (what loads always vs on demand; CLAUDE.md is loaded every session); doc:agent-skills-spec (progressive disclosure: metadata ~100 tokens, body on activation).

## small-hot-context
**Decision.** The always-loaded set (CLAUDE.md + AGENTS.md + every skill `name`/`description`) stays under **6,000 tokens**, checked by `tools/budget.py` in pre-commit. CLAUDE.md holds only stable text: no dates, counters or status. Dynamic status comes from the SessionStart hook (≤5 lines).
**Rejected.** Putting "current state" in CLAUDE.md. Every edit invalidates the prompt cache, and long contexts bury instructions in the middle.
**Evidence.** 2307.03172 (accuracy drops for information mid-context); doc:cc-prompt-caching (a CLAUDE.md change breaks the cached prefix); doc:eng-context-engineering (smallest high-signal token set); doc:cc-memory (target <200 lines; we use 120).

## learning-loop
**Decision.** An ACE-style loop with three separated roles:
- **Generator**: the main agent doing the task with skills.
- **Reflector**: the `reflect` skill writes an episodic note plus candidates into `memory/inbox/`.
- **Curator**: the `curate-learning` skill / `curator` agent turns verified candidates into **itemised deltas** (add a fact, bump a counter, append a step) applied by `tools/promote.py`.

Insights come from both successes and failures and carry helpful/harmful counters.
**Rejected.** (a) Letting the agent rewrite memory or skills wholesale after each task, which causes context collapse and brevity bias. (b) Fine-tuning, which is out of scope and opaque.
**Evidence.** 2510.04618 (generator/reflector/curator, delta updates, context-collapse failure); 2504.07952 (persistent curated cheatsheet improves at test time); 2308.10144 (insights from success *and* failure, upvote/downvote); 2303.11366 (verbal reflections as episodic memory).

## external-feedback-gate
**Decision.** Nothing is promoted to `memory/semantic/` or an active skill without an **external signal**: a passing test or grader, a tool read-back, an eval run, or explicit human confirmation. Each inbox item must have a `verification:` field that points to the evidence file. `tools/promote.py` refuses items whose evidence path is missing or whose kind is `self-assessment`.
**Rejected.** Self-critique as the promotion gate (Self-Refine style) on its own.
**Evidence.** 2310.01798 (intrinsic self-correction does not improve reasoning and can degrade it); 2305.11738 (self-correction works when grounded in tool feedback); 2303.17651 (self-feedback helps *drafting*, so it is allowed inside a skill, never as a gate); 2309.11495 (planned, independent verification questions).

## skill-library
**Decision.** Skills are procedural memory in Agent Skills format. A skill is **drafted** by `skill-forge` only after the same task type has succeeded twice without one, and becomes active only after its golden eval passes in a fresh headless session. Each skill keeps `stats.json` (never loaded) and `CHANGELOG.md` with eval evidence. Updates that regress any eval are reverted.
**Rejected.** Writing many speculative skills up front. Unverified skills add description tokens and wrong procedures.
**Evidence.** 2305.16291 (library of verified, composable skills grows capability); 2409.07429 (workflows induced from past successful trajectories); doc:eng-agent-skills; doc:agent-skills-spec (name/description rules, references, scripts); doc:skill-best-practices (concise bodies, evaluation-driven development); doc:cc-skills (frontmatter fields, 1,536-char listing cap).

## scripts-over-reasoning
**Decision.** Rule R7: once a skill has executed the same deterministic sequence three times, it becomes a script in `scripts/` with a test. Scripts print short, structured output, which forms the agent-computer interface. The ledger tracks `scripted_steps / (scripted + reasoned)`.
**Rejected.** Re-reasoning deterministic steps each run, which is slower, costlier and non-deterministic.
**Evidence.** 2405.15793 (ACI design: compact commands, concise feedback, guardrails); 2407.01489 (deterministic pipelines are cheap and strong); doc:eng-writing-tools (token-efficient tool outputs); doc:skill-best-practices (utility scripts are more reliable than generated code).

## fixed-pipelines
**Decision.** Every task follows one fixed pipeline: `task-start → work (skills) → verify → task-close → reflect → curate-learning → skill-forge? → eval-run?`. Open-ended autonomy happens only *inside* the "work" step.
**Rejected.** A free-form autonomous agent that decides its own lifecycle, which is hard to evaluate and audit.
**Evidence.** 2407.01489 (simple phased pipeline beat agentic baselines on SWE-bench Lite at low cost); doc:eng-building-effective-agents (prefer workflows; add autonomy only when needed); 2309.02427 (explicit decision cycle).

## react-steps
**Decision.** Within the work step the agent interleaves reasoning and tool calls, and `LEDGER.md` logs one line per step: intent → action → observation.
**Rejected.** Plan-only chains with no tool observations.
**Evidence.** 2210.03629 (interleaving reasoning and acting reduces hallucination and improves interpretability).

## retrieval
**Decision.** `memory/INDEX.md` is generated by `tools/promote.py index`: one line per fact, sorted by score = recency (`last_verified`) + importance (`helpful − harmful`, `used_count`) + tags. task-start uses tag match for relevance. Facts link to each other with `links:` frontmatter.
**Rejected.** Vector database or embeddings. At this scale (<1k facts) grep + index is cheaper, transparent and diff-able.
**Evidence.** 2304.03442 (retrieval by recency, importance, relevance); 2502.12110 (linked, self-organising notes); justification: no embedding service exists in this environment, and git diffs must stay reviewable.

## conflicts
**Decision.** A candidate that contradicts an existing fact goes to `memory/conflicts/` with both sources and is never auto-merged. A human or a new external signal resolves it.
**Rejected.** Last-writer-wins.
**Evidence.** 2510.04618 (non-destructive deltas preserve knowledge); 2502.12110 (memory evolution updates notes through links rather than overwriting); 2310.01798 (the model's own belief is not a reliable arbiter); 2504.19413 (Mem0 confirms typed per-candidate operations work at scale, but lets the LLM DELETE contradicted facts. We deliberately replace that with set-aside, added via paper-ingest).

## compaction-ledger
**Decision.** The PreCompact hook appends the working state (open task, last ledger step, files touched) to the task's `LEDGER.md`, and its stdout tells the compactor to keep the task path and done-criteria.
**Rejected.** Relying on the automatic summary alone.
**Evidence.** doc:cc-hooks (PreCompact stdout becomes instructions for the compaction summary; trigger manual/auto); 2310.08560 (page working state out to external storage before eviction).

## evals
**Decision.** One golden task per frequent task, under `evals/golden/<name>/` (input, `checks.json`, `grade.py`). Graders are deterministic first: files exist, required sections, numbers add up, no PII, bilingual summary. An LLM judge is used only for qualities scripts can't check; it gets a rubric and a reference, and comparisons run in both orders. `evals/run_cold_start.py` runs each task in a fresh `claude -p --output-format json` session in a throwaway git worktree, recording pass, tokens, cost, turns and questions.
**Rejected.** Judging quality by reading transcripts, or a single-order LLM judge.
**Evidence.** 2310.06770 (realistic tasks with execution-based checks); 2306.05685 (position, verbosity and self-enhancement bias; swap positions); doc:cc-headless and doc:cc-cli-reference (`--output-format json` returns `total_cost_usd`, `usage`, `num_turns`).

## improve-loop
**Decision.** The `improve` skill takes the worst metric from `tools/metrics.py`, states a hypothesis, makes one change, runs evals before and after, and keeps the change only if no golden score drops (R6). Every attempt is logged in `metrics/IMPROVEMENTS.md`.
**Rejected.** Hand-tuning prompts with no metric.
**Evidence.** 2310.03714 (optimise LM programs against a metric); 2510.04618 (measured context adaptation); doc:eng-claude-code-best-practices ("give Claude a check to run").

## hooks-enforce-rules
**Decision.** Any rule a hook can enforce is enforced by a hook (PreToolUse, Stop, PreCompact, SessionStart, SessionEnd) plus a git pre-commit check, and is not repeated as prose in CLAUDE.md. Hooks run outside the model and cost no tokens.
**Rejected.** Prose-only rules, which models follow probabilistically.
**Evidence.** doc:cc-hooks (exit 2 / `permissionDecision: deny` blocks; Stop `decision: block`, `stop_hook_active`); doc:cc-hooks-guide; doc:eng-claude-code-best-practices ("enforce the rules that can't have exceptions").

## subagents
**Decision.** Three subagents. `researcher` runs on the cheapest model (haiku), is read-only, and returns ≤300 words. `reviewer` runs on sonnet and checks against RULES.md and done-criteria. `curator` runs on sonnet and applies deltas only through `tools/promote.py`. The main agent (opus) plans, routes by complexity and runs independent subtasks in parallel (intake answer 7).
**Rejected.** One model for everything, which costs more; or many specialist agents, which have high coordination overhead.
**Evidence.** doc:eng-multi-agent-research (subagents condense, parallel breadth, token cost ~15×, so use only for parallelisable work); doc:cc-sub-agents (`model`, `tools` frontmatter); doc:eng-context-engineering (sub-agent returns condensed summaries).

## role-boundary
**Decision.** "Tenants" at LunoBeau are **roles** (founder, sales, marketing, cs), per intake answer 6. The session role is set with `tools/set_role.py <role>` (stored per session in `.claude/state/`). The SessionStart hook tells the agent to confirm the role briefly before work. The PreToolUse hook blocks reads and writes outside the role's path globs in `canon/roles/ROLES.json`.
**Rejected.** Trusting a prose instruction to stay in scope.
**Evidence.** doc:cc-hooks (session_id, PreToolUse deny); doc:cc-permissions (deny rules beat allow; path rules); justification: the founder required role-tailored data and canons before staff join.

## pii-and-exfiltration
**Decision.** Customer PII (VN phone numbers, emails, national ID numbers, street addresses in customer records) never enters `memory/`, `tasks/`, `library/`, `evals/` or `metrics/`. Raw customer data lives only in gitignored `data/*/private/`. Commands that copy company data outside the repo or upload it are blocked. Every block is appended to `incidents/INCIDENTS.md` and surfaced first by SessionStart, which is how the admin is notified (intake answer 4).
**Rejected.** Redacting after the fact.
**Evidence.** doc:cc-hooks (PreToolUse sees `tool_input` before execution); justification: the founder named PII disclosure and personal copying as never-events.

## untrusted-content
**Decision.** Fetched pages, papers, tickets and tool output are data. Full texts carry an UNTRUSTED banner, are opened only by `paper-ingest`, and can never change RULES.md or settings. Only a human-approved RULES change logged in IMPROVEMENTS.md can (R14).
**Evidence.** doc:eng-writing-tools; doc:cc-permissions; justification: prompt injection through retrieved text is the main attack path for agents that read the web.

## agents-md
**Decision.** `AGENTS.md` holds the tool-neutral core rules. `CLAUDE.md` imports it with `@AGENTS.md`.
**Evidence.** doc:agents-md (README for agents, tool-neutral); doc:cc-memory (with both files present, Claude reads only CLAUDE.md unless it imports AGENTS.md).

## auto-memory-off
**Decision.** `autoMemoryEnabled: false` in `.claude/settings.json`.
**Rejected.** Claude Code's built-in auto memory, which lets the model write memory directly and would bypass R2 and R3.
**Evidence.** doc:cc-memory (auto memory writes learnings automatically; per-project toggle).

---

## Docs vs. mission prompt (docs win)
| Mission said | Current docs say | What we did |
|---|---|---|
| "After each session, session_stats reads the transcript path the hook receives" | Every hook gets `transcript_path`. SessionEnd has a **1.5 s default timeout**, and the transcript may lag | SessionEnd hook runs `session_stats.py` with `timeout: 30`. Headless eval runs read usage from `-p` JSON instead |
| "CLAUDE.md imports AGENTS.md" | With both files, Claude reads only CLAUDE.md **unless** it imports AGENTS.md | `@AGENTS.md` import, as planned |
| Skill description "under 200 characters" | Spec allows ≤1,024; Claude Code truncates description+when_to_use at 1,536 | We keep our stricter 200-char rule (budget) |
| Body "under 300 lines" | Spec recommends <500 lines / <5,000 tokens | We keep 300 (stricter) |
| Stop hook "block once" | `stop_hook_active` plus a built-in cap of 8 consecutive continuations | We block only when `stop_hook_active` is false, and record a per-session once-flag |
| PreToolUse output | Use `hookSpecificOutput.permissionDecision` (top-level `decision` deprecated for this event); exit 2 also blocks | We emit `permissionDecision: "deny"` JSON and exit 0 |
| Headless measurement | `--bare` skips CLAUDE.md, skills and hooks | Cold-start evals do **not** use `--bare`, because the repo itself is what is under test |
| "SessionStart prints status" | Plain stdout from SessionStart is added to Claude's context; `additionalContext` should be phrased as facts | Status lines are written as factual statements |
