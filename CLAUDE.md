@AGENTS.md

# Claude Code operating notes

This file is loaded in every session. Keep it short and stable (no dates, counts or status); the SessionStart hook supplies live status. Hooks enforce most rules, so this file only says what the hooks cannot.

## Start of a session
- The first status line may say there are open incidents. If so, tell the user first.
- If the session role is not confirmed, ask once, briefly and warmly, inside your first reply before touching data. For example: "Để mình lấy đúng dữ liệu và quy trình — hôm nay bạn làm việc với vai trò nào: Founder, Sales, Marketing hay CSKH?" Then run `python3 tools/set_role.py <role>` and read `canon/roles/<role>.md`.
- Never guess the role from a name or writing style.

## Every piece of work follows one pipeline
1. `task-start` skill: creates `tasks/<date>-<slug>/`, done-criteria, relevant skills and facts.
2. Do the work with the matching domain skill (`phase-plan`, `cs-training`, `ops-review`, or others listed by the Skill tool). Log each step in LEDGER.md as `- intent -> action -> observation`.
3. Verify with a tool, script or grader, never by self-assessment alone. Save the output to `evidence/`.
4. `task-close` skill, then `reflect` (episodic note plus inbox candidates), then `curate-learning`.
5. If the trajectory repeats a pattern, run `skill-forge`. If a skill or fact changed, run `eval-run`.
Skip the pipeline only for quick questions that produce no deliverable.

## Finding knowledge (progressive disclosure)
- Facts: read `memory/INDEX.md`, then only the fact files you need.
- Company and products: `canon/company.md`. Role scope: `canon/roles/<role>.md`.
- Research behind the design: `library/INDEX.md` and cards in `library/cards/`. Never open `library/full/` unless running `paper-ingest` or the user asks.
- Rules with reasons: `RULES.md`. Design decisions: `DESIGN.md`. Weekly routine: `OPERATIONS.md`.
- Read nothing "just in case".

## Delegation and models
- Broad reading or searching: the `researcher` subagent (cheapest model). It returns a conclusion of at most 300 words.
- Checking a result against rules and done-criteria: the `reviewer` subagent.
- Merging learnings into memory: the `curator` subagent.
- Run independent subtasks in parallel. Keep planning, strategy and final synthesis in the main session.

## Prefer scripts
If a skill has a script for a step, run it instead of reasoning through the step. A deterministic sequence you have done three times becomes a script with a test (R7), proposed through `skill-forge`.

## Domain defaults
- Market: Vietnam. Currency: VND. Channels: Facebook/Instagram, TikTok (and TikTok Shop), Google (Search, YouTube), Shopee, Lazada, website.
- Product claims follow `canon/company.md#claims` (no treatment or medical claims). Flag doubtful claims for human review.
- Inputs marked SAMPLE are synthetic. Say so in any deliverable built on them.
