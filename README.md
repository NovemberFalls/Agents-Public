# Agents-Public

> A library of role-based AI-agent persona definitions and a coordination model for running them with Claude Code and the Claude Agent SDK.

---

## What is this?

This repository is a library of Markdown persona files. Each file defines a specialist agent by **role** — a sharp domain scope, explicit behavioral rules, a defined model tier, and a structured report format. There is no application code here: only prompts, patterns, and process.

Every persona file is a valid **Claude Code subagent definition**. Drop one into a `~/.claude/agents/` directory and it becomes an agent you can invoke; load its body as a system prompt and it becomes an Agent SDK agent. The agents coordinate through an orchestration loop designed to prevent the most common multi-agent failure mode — specialists working from stale context about what other specialists changed — while keeping the token cost of that coordination under control.

Four teams are included, all built on the same pattern: an implementation fleet, a strategic advisory board, a creative-writing review board, and a tabletop-RPG pressure-test team.

---

## Why

Two problems motivate everything here: **coordination** and **context cost**.

### Context debt compounds faster than technical debt

When multiple agents work the same codebase at once with no coordination, they produce changes that are each correct in isolation and broken in combination. An agent writing an API endpoint cannot see that the frontend agent changed the contract five minutes ago. An agent adding a database column cannot see that the migration already ran.

The naive fix — serialize everything — throws away the efficiency of parallel specialization. The fix here is different: **build the dependency graph before writing any code.** The Change Dependency Graph (CDG) maps every file to be modified and every system boundary it touches. From the graph, the orchestrator derives execution tiers — groups of changes with no mutual dependencies that run safely in parallel. Tier N starts only when Tier N-1 is finalized and reviewed. No specialist ever works from a stale snapshot of another's output.

### Specialists are a token strategy, not just an org chart

The headline benefit of role-scoped subagents is **context isolation**. When the orchestrator delegates to a specialist, that specialist reads files, greps, and explores in its *own* context window — and returns only a short report. The expensive, token-heavy work stays quarantined; the orchestrator's window holds the plan and the summaries, not the raw exploration, so it can coordinate a large task without bloating into compaction.

Add right-sized models per role (pay Opus rates only where they buy something), skills that load a workflow on demand instead of carrying it in every prompt, and a shared project-brain that is read once instead of re-derived each run. The robust win is **peak context**: any single window stays small, so a large task never bloats into compaction. Total token *spend* is a separate, workload-dependent question — coordination and review gates cost tokens, so for a one-line change the repo prescribes a lightweight single-specialist path instead. The full rationale, including the honest counter-argument, is in **[docs/token-efficiency.md](docs/token-efficiency.md)**, with a worked token ledger on a sample task in **[examples/orchestrated-run/](examples/orchestrated-run/)**.

---

## One pattern, four domains

The coordination model is domain-agnostic. The same loop — independent specialists, a graph of dependencies, parallel-where-safe execution, structured reports, mandatory review and hygiene gates — drives code, project strategy, prose, and game design. The four teams are the same idea applied to four problem spaces:

| Team | Domain | What it produces |
|------|--------|------------------|
| **Orchestration** | Code | A task brief turned into reviewed, integrated changes |
| **Advisory Board** | Project strategy | A weighted Readiness Score across seven domains |
| **Writing** | Manuscripts | Structured critique for continuity, voice, craft, canon |
| **TTRPG** | Homebrew game rules | Exploits, balance gaps, and playability findings |

---

## Architecture

```
                       ┌──────────────────────────────────────────┐
                       │           ADVISORY BOARD (parallel)        │
                       │   CFO · CMO · CPO · CTO · UI/UX · Code     │
                       │   Auditor · Gap Analyst · DevOps/SRE ·     │
                       │   CSO · Legal                              │
                       │          Weighted Readiness Score          │
                       └────────────────┬───────────────────────────┘
                                        │ consolidated findings
                                        ▼
                   ┌────────────────────────────────────────┐
                   │            Swarm (Director)             │
                   │     cross-team routing & coordination   │
                   └────────────────────┬────────────────────┘
                                        ▼
                   ┌────────────────────────────────────────┐
                   │              Orchestrator               │
                   │   explore → CDG → tier plan → review    │
                   └──────────────┬─────────────────────────┘
                                  │
          ┌───────────────────────┼────────────────────────┐
          ▼                       ▼                        ▼
   Tier 1 (parallel)       Tier 2 (sequential)        Tier N ...
   ┌──────────────────┐    ┌──────────────────┐
   │ Backend │Frontend│    │ Database Engineer │
   │ Security│Systems │    │ (receives Tier 1  │
   │ Test    │DevOps  │    │ finalized state)  │
   └─────────┴────────┘    └──────────────────┘
          │                        │
          ▼                        ▼
   ┌─────────────────────────────────────┐
   │  Code Reviewer — review gate         │
   │  (all Opus output before Orchestr.)  │
   └────────────────────┬────────────────┘
                        ▼
   ┌─────────────────────────────────────┐
   │  Hygiene Auditor — hygiene sweep     │
   │  (mandatory after every tier)        │
   └────────────────────┬────────────────┘
                        ▼
   ┌─────────────────────────────────────┐
   │  Orchestrator — reconciliation       │
   │  matrix: every requirement →         │
   │  IMPLEMENTED / PARTIAL / DEFERRED    │
   └────────────────────┬────────────────┘
                        ▼
                 Human review + approval
```

---

## The Teams

| Team | Description | Agents | Folder |
|------|-------------|--------|--------|
| **Orchestration Team** | Implementation fleet. Turns a task brief into reviewed, integrated code changes. The Swarm routes, the Orchestrator plans and sequences, nine specialists execute. | 11 | [orchestration-team/](orchestration-team/) |
| **Advisory Board** | Standing review board. Evaluates a project across seven domains and produces a weighted Readiness Score (1–10). Each agent reviews independently. | 10 | [advisory-board/](advisory-board/) |
| **Writing Team** | Creative-writing review board. Reviews manuscripts for continuity, voice, reader experience, craft, and canon. Does not write prose. | 5 | [writing-team/](writing-team/) |
| **TTRPG Team** | Tabletop-RPG pressure-test team. Stress-tests homebrew rules for balance, exploits, and playability across system experts, min-maxers, players, and live GMs. | 17 | [ttrpg-team/](ttrpg-team/) |

---

## Quick Start

### With Claude Code subagents

Claude Code loads subagents from Markdown files in `~/.claude/agents/` (user-level) or `.claude/agents/` (project-level). Each file's frontmatter must follow Claude Code's subagent schema:

```yaml
---
name: backend-engineer        # required — lowercase letters + hyphens only; this is the invocation slug
description: Use for backend route changes, API logic, and server internals.   # required — drives auto-delegation
model: sonnet                 # optional — alias only (sonnet | opus | haiku | inherit)
---
```

`name` and `description` are required: a file with no `description` does not load. `tools` is optional (omit to inherit all). Unknown keys are ignored.

1. Copy the persona files you want into `~/.claude/agents/` (or a project's `.claude/agents/`).
2. In a Claude Code session, the orchestrator spawns specialists with the `Agent` tool, passing the full task brief inline; or invoke an agent directly by its role.
3. The specialist's final message is its completion report — the orchestrator parses that block and continues.

### With skills (slash commands)

The two workflows in this repo are packaged as skills under [`.claude/commands/`](.claude/commands/) so the procedure loads on demand instead of living in your system prompt:

| Command | When to use |
|---------|-------------|
| [`/orchestrate`](.claude/commands/orchestrate.md) | Multiple findings or coordinated changes across files — runs the full CDG → tiers → review loop |
| [`/fix`](.claude/commands/fix.md) | A single issue in ≤3 files with no downstream dependencies — the lightweight path |

Copy them into `~/.claude/commands/` (or a project's `.claude/commands/`) and invoke by name.

### With the Claude Agent SDK

Load a persona file's body as the system prompt when instantiating an agent:

```python
# Conceptual — adapt to your SDK version.
system_prompt = open("orchestration-team/agents/01-orchestrator.md").read()
agent = ClaudeAgent(system_prompt=system_prompt, model="claude-opus-4-7")  # use the current Opus model ID
report = agent.run(task_brief)
```

Each persona declares its preferred model and the conditions under which it escalates.

---

## Repo Layout

```
Agents-Public/
├── README.md                        # this file
├── LICENSE                          # MIT
├── CONTRIBUTING.md                  # how to add agents and teams
│
├── orchestration-team/
│   ├── README.md                    # team overview, flow diagram, invariants
│   ├── agents/
│   │   ├── 00-roster.md
│   │   ├── 00-swarm.md
│   │   ├── 01-orchestrator.md
│   │   ├── 02-reviewer.md
│   │   ├── 03-backend-engineer.md
│   │   ├── 04-frontend-engineer.md
│   │   ├── 05-security-engineer.md
│   │   ├── 06-test-engineer.md
│   │   ├── 07-devops-engineer.md
│   │   ├── 08-database-engineer.md
│   │   ├── 09-systems-engineer.md
│   │   ├── 10-hygiene-auditor.md
│   │   └── project-brain-template.md
│   └── templates/
│       ├── execution-plan.md
│       ├── task-brief.md
│       ├── specialist-report.md
│       ├── code-review.md
│       ├── reconciliation-matrix.md
│       └── task-file.md
│
├── advisory-board/
│   ├── README.md                    # board overview, scoring formula
│   ├── agents/
│   │   ├── 00-roster.md
│   │   ├── 01-cfo-advisor.md
│   │   ├── 02-cmo-advisor.md
│   │   ├── 03-cpo-advisor.md
│   │   ├── 04-cto-advisor.md
│   │   ├── 05-uiux-lead.md
│   │   ├── 06-code-auditor.md
│   │   ├── 07-gap-analyst.md
│   │   ├── 08-devops-sre.md
│   │   ├── 09-cso-advisor.md
│   │   └── 10-legal-advisor.md
│   └── templates/
│       ├── agent-review.md
│       ├── agent-memory.md
│       ├── consolidated-report.md
│       └── owner-responses.md
│
├── writing-team/
│   ├── README.md
│   ├── agents/                      # continuity, voice, reader, craft, canon
│   └── session-protocol.md
│
├── ttrpg-team/
│   ├── README.md
│   ├── agents/                      # 17: system experts, min-maxers, players, GMs, VTT
│   ├── session-protocol.md
│   └── combat-log-format.md
│
├── docs/
│   ├── architecture.md              # CDG, tiers, gates, reconciliation matrix
│   ├── orchestration-loop.md        # the orchestrator's loop end-to-end
│   ├── board-review.md              # advisory board scoring and process
│   ├── token-efficiency.md          # where the tokens go, and why this comes out ahead
│   └── authoring-an-agent.md        # how to write a good persona file
│
├── examples/
│   ├── sample-review/                # advisory board review of fictional "Lumina"
│   │   ├── README.md
│   │   ├── cto-advisor-review.md
│   │   ├── cfo-advisor-review.md
│   │   └── consolidated-report.md
│   ├── orchestrated-run/             # full loop on fictional "Verdant" (illustrative)
│   │   ├── README.md
│   │   ├── task-brief.md
│   │   ├── execution-plan.md         # CDG + tiers + file-ownership matrix
│   │   ├── tier-reports.md           # specialist reports + Code Reviewer gate
│   │   ├── reconciliation-matrix.md
│   │   └── context-ledger.md         # the token/context model — illustrative
│   ├── real-run/                     # REAL metered run that built this repo
│   │   └── README.md                 # harness-reported tokens from 16 subagents
│   └── eval/                         # REAL 3-arm experiment: is the CDG load-bearing?
│       └── README.md                 # monolith vs naive-parallel vs CDG, mypy-scored
│
└── .github/
    └── workflows/
        └── secret-scan.yml          # gitleaks gate on push and PR
```

---

## Authoring your own

See [docs/authoring-an-agent.md](docs/authoring-an-agent.md) for how to write a persona that a model can inhabit consistently, and [CONTRIBUTING.md](CONTRIBUTING.md) for filename conventions, the required frontmatter, and the secret-hygiene gate.

---

## Built by

Built and maintained by **November Falls**.

## License

MIT — see [LICENSE](LICENSE).
