# Library index

The only library file other parts of the repo point to. Cards are summaries (hot enough to read);
`library/full/` is cold storage, opened only by the paper-ingest skill or on request.

## Papers (cards in `library/cards/`)

- [2210.03629](cards/2210.03629.md) **ReAct: Synergizing Reasoning and Acting in Language Models** — Interleaving written reasoning with tool actions and their observations makes an LLM agent more grounded, easier to audit and better at interactive tasks than reasoning-only or acting-only prompting.
- [2303.11366](cards/2303.11366.md) **Reflexion: Language Agents with Verbal Reinforcement Learning** — An agent can improve across attempts without weight updates by turning outcome feedback into written reflections stored in an episodic buffer and re-read on the next trial.
- [2303.17651](cards/2303.17651.md) **Self-Refine: Iterative Refinement with Self-Feedback** — One LLM can draft, critique and revise its own output in a loop and beat single-pass generation on many tasks, with no training.
- [2304.03442](cards/2304.03442.md) **Generative Agents: Interactive Simulacra of Human Behavior** — A memory stream with scored retrieval, periodic reflection and planning lets LLM agents act believably over time.
- [2305.11738](cards/2305.11738.md) **CRITIC: LLMs Can Self-Correct with Tool-Interactive Critiquing** — Models correct their outputs reliably when the critique step is grounded in external tools, and unreliably when they only review themselves.
- [2305.16291](cards/2305.16291.md) **Voyager: An Open-Ended Embodied Agent with Large Language Models** — A growing library of executable, verified skills lets an LLM agent accumulate and compose abilities over time without fine-tuning or forgetting.
- [2306.05685](cards/2306.05685.md) **Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena** — Strong LLM judges agree with humans about as often as humans agree with each other, but carry position, verbosity and self-preference biases.
- [2307.03172](cards/2307.03172.md) **Lost in the Middle: How Language Models Use Long Contexts** — Models use relevant information best at the start or end of the input and worst in the middle, so more context can hurt.
- [2308.10144](cards/2308.10144.md) **ExpeL: LLM Agents Are Experiential Learners** — An agent can learn reusable natural-language insights from both successful and failed trajectories on training tasks, and recall past successes at inference, with no parameter updates.
- [2309.02427](cards/2309.02427.md) **Cognitive Architectures for Language Agents** — Language agents can be described uniformly by modular memories, a structured action space, and a repeated decision cycle.
- [2309.11495](cards/2309.11495.md) **Chain-of-Verification Reduces Hallucination in Large Language Models** — Having the model plan fact-checking questions and answer them separately from the draft reduces hallucinated facts.
- [2310.01798](cards/2310.01798.md) **Large Language Models Cannot Self-Correct Reasoning Yet** — Without external feedback, asking an LLM to review and fix its own reasoning does not help and often makes answers worse.
- [2310.03714](cards/2310.03714.md) **DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines** — LM pipelines should be declared as modules and then optimised automatically against an explicit metric, instead of being hand-tuned as prompt strings.
- [2310.06770](cards/2310.06770.md) **SWE-bench: Can Language Models Resolve Real-World GitHub Issues?** — Benchmarks built from real tasks and verified by running tests expose capability gaps that synthetic tasks hide.
- [2310.08560](cards/2310.08560.md) **MemGPT: Towards LLMs as Operating Systems** — Treating the context window like RAM and external storage like disk, with the model paging data between them, gives the illusion of unbounded context.
- [2404.13501](cards/2404.13501.md) **A Survey on the Memory Mechanism of LLM-based Agents** — Agent memory can be analyzed systematically by its sources, forms and operations, and by how it is evaluated.
- [2405.15793](cards/2405.15793.md) **SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering** — An interface designed for the agent (few simple commands, concise output, guardrails) lifts task success more than a raw shell.
- [2407.01489](cards/2407.01489.md) **Agentless: Demystifying LLM-based Software Engineering Agents** — A fixed three-phase pipeline of localise, repair, validate matches or beats complex autonomous agents at lower cost.
- [2409.07429](cards/2409.07429.md) **Agent Workflow Memory** — Agents do better on long-horizon tasks when they induce reusable sub-task workflows from past successful trajectories and supply the relevant ones to later runs.
- [2502.12110](cards/2502.12110.md) **A-MEM: Agentic Memory for LLM Agents** — Memory notes that carry keywords and tags and are linked to related notes retrieve better than flat stores.
- [2504.07952](cards/2504.07952.md) **Dynamic Cheatsheet: Test-Time Learning with Adaptive Memory** — A curated, evolving store of short reusable insights improves a frozen model across tasks without weight updates.
- [2504.19413](cards/2504.19413.md) **Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory** — An extract-then-update memory pipeline, where each candidate fact is compared with similar stored memories and turned into one explicit operation, keeps long-term memory consistent at a fraction of full-context cost.
- [2510.04618](cards/2510.04618.md) **Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models** — Treating context as an evolving playbook, updated by small itemised deltas through separate generator, reflector and curator roles, avoids brevity bias and context collapse and improves agents and domain reasoning.

## Documentation (cite as `doc:<id>`; URLs in MANIFEST.csv)

- `doc:agent-skills-spec` [Specification - Agent Skills](https://agentskills.io/specification) — Open Agent Skills format: name (lowercase-hyphen, <=64, matches dir), description <=1024, scripts/references/assets, progressive disclosure.
- `doc:agents-md` [AGENTS.md](https://agents.md) — AGENTS.md: a tool-neutral README for coding agents at repo root.
- `doc:cc-cli-reference` [CLI reference](https://code.claude.com/docs/en/cli-reference.md) — Flags for headless evals: -p, --output-format json, --max-turns, --model, --setting-sources, --no-session-persistence, --permission-mode.
- `doc:cc-features-overview` [Extend Claude Code](https://code.claude.com/docs/en/features-overview.md) — What loads when: CLAUDE.md always, skill descriptions always, skill bodies on use, hooks cost zero context.
- `doc:cc-headless` [Run Claude Code programmatically](https://code.claude.com/docs/en/headless.md) — claude -p with --output-format json returns result, usage, total_cost_usd, num_turns; --bare skips CLAUDE.md/skills/hooks.
- `doc:cc-hooks` [Hooks reference](https://code.claude.com/docs/en/hooks.md) — Hook events and JSON I/O: PreToolUse permissionDecision deny, Stop decision block + stop_hook_active, PreCompact stdout steers summary, SessionEnd 1.5s default timeout.
- `doc:cc-hooks-guide` [Automate actions with hooks](https://code.claude.com/docs/en/hooks-guide.md) — Practical hook recipes; hooks give deterministic control instead of relying on the model to choose.
- `doc:cc-memory` [How Claude remembers your project](https://code.claude.com/docs/en/memory.md) — CLAUDE.md loads every session (target <200 lines); @imports; AGENTS.md is read only if imported when CLAUDE.md exists; auto memory toggle.
- `doc:cc-permissions` [Configure permissions](https://code.claude.com/docs/en/permissions.md) — Rules evaluate deny -> ask -> allow; first match wins; Bash/Read/Edit pattern syntax.
- `doc:cc-prompt-caching` [How Claude Code uses prompt caching](https://code.claude.com/docs/en/prompt-caching.md) — Prompt cache keys on the prefix; editing CLAUDE.md or switching model breaks it; keep stable content first.
- `doc:cc-settings` [Settings files and precedence](https://code.claude.com/docs/en/settings.md) — Settings scopes and precedence (managed > local > project > user); where hooks and permissions live.
- `doc:cc-skills` [Extend Claude with skills](https://code.claude.com/docs/en/skills.md) — Skill frontmatter fields; names+descriptions always listed (desc+when_to_use capped at 1,536 chars); body loads on invoke and persists in context.
- `doc:cc-sub-agents` [Create custom subagents](https://code.claude.com/docs/en/sub-agents.md) — Subagent frontmatter (name, description, tools, model, maxTurns, skills); separate context window; model aliases haiku/sonnet/opus.
- `doc:eng-agent-skills` [Equipping agents with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) — Skills = folders of instructions/scripts/resources loaded progressively; metadata first, body on relevance, files on demand.
- `doc:eng-building-effective-agents` [Building effective AI agents](https://www.anthropic.com/engineering/building-effective-agents) — Prefer simple composable workflows (chains, routing, evaluator-optimizer) before autonomous agents.
- `doc:eng-claude-code-best-practices` [Best practices for Claude Code](https://www.anthropic.com/engineering/claude-code-best-practices) — Give Claude a check to run, manage context aggressively, enforce non-negotiable rules with hooks, use subagents for investigation.
- `doc:eng-context-engineering` [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Context is a finite attention budget: smallest high-signal token set, just-in-time retrieval, compaction, structured notes, sub-agents.
- `doc:eng-multi-agent-research` [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) — Orchestrator + parallel subagents wins on breadth but costs ~15x tokens; subagents return condensed findings.
- `doc:eng-writing-tools` [Writing effective tools for AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents) — Design tools for agents: few high-leverage tools, meaningful concise outputs, clear errors, evaluate tools with realistic tasks.
- `doc:skill-best-practices` [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md) — Be concise, set degrees of freedom, keep SKILL.md small, one-level-deep references, scripts for deterministic work, evaluation-driven development.
