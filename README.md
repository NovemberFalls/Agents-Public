# agent-fleet

> A collection of AI-agent persona definitions and orchestration patterns for use with Claude Code and the Claude Agent SDK.

---

## What is this?

This repository is a library of Markdown persona files, each defining a specialist AI agent with a real identity, a sharp domain scope, explicit behavioral rules, and a structured report format. There is no application code here — only prompts, patterns, and process.

Drop these persona files into a Claude Code subagent directory or load one as a system prompt via the Claude Agent SDK. Invoke by role. The agents coordinate through a structured orchestration loop that prevents the most common multi-agent failure mode: specialists working from stale context about what other specialists changed.

Four teams are included: an implementation fleet, a strategic advisory board, a creative-writing review board, and a tabletop-RPG pressure-test team.

---

## Why

**Context debt compounds faster than technical debt.**

When multiple AI agents work on the same codebase simultaneously without coordination, they produce changes that look correct in isolation and break things in combination. An agent writing a new API endpoint has no idea whether the frontend agent changed the contract five minutes ago. An agent adding a new database column has no idea whether the migration agent already ran that migration.

The standard solution — serialize everything — throws away the efficiency of parallel specialization. The solution in this repository is different: **build the dependency graph before writing any code.**

The Change Dependency Graph (CDG) maps every file to be modified and every system boundary that modification touches. From the graph, the orchestrator derives execution tiers — groups of changes with no mutual dependencies that can run safely in parallel. Tier N only starts when Tier N-1 is finalized and reviewed. No specialist ever works from a stale snapshot of another specialist's output.

Multi-agent coordination fails when the orchestrator treats agents as fire-and-forget. It works when the orchestrator treats coordination as an engineering problem with a designed solution.

---

## ASCII Architecture

```
                        ┌─────────────────────────────────────────┐
                        │          ADVISORY BOARD (parallel)       │
                        │  Alexandra · Marcus · Priya · Dr. Reyes  │
                        │  Sophie · Chen · Jordan · Kai · Viktor   │
                        │              · Evelyn                    │
                        │         Weighted Readiness Score         │
                        └────────────────┬────────────────────────┘
                                         │ consolidated findings
                                         ▼
                    ┌────────────────────────────────────────┐
                    │              Vera (Director)            │
                    │   cross-team routing & coordination    │
                    └────────────────────┬───────────────────┘
                                         │
                                         ▼
                    ┌────────────────────────────────────────┐
                    │          Nadia (Orchestrator)           │
                    │  explore → CDG → tier plan → review    │
                    └──────────────┬─────────────────────────┘
                                   │
           ┌───────────────────────┼────────────────────────┐
           │                       │                        │
           ▼                       ▼                        ▼
    Tier 1 (parallel)       Tier 2 (sequential)        Tier N ...
    ┌──────────────┐        ┌──────────────────┐
    │ Ash  │ Finn  │        │ Sage             │
    │ Zara │ Quinn │        │ (receives Tier 1 │
    │ Sam  │ Dev   │        │ finalized state) │
    └──────┴───────┘        └──────────────────┘
           │                        │
           ▼                        ▼
    ┌─────────────────────────────────────┐
    │  Atlas — code review gate           │
    │  (all Opus output before Nadia)     │
    └────────────────────┬────────────────┘
                         │
                         ▼
    ┌─────────────────────────────────────┐
    │  Reaper — hygiene sweep             │
    │  (mandatory after every tier)       │
    └────────────────────┬────────────────┘
                         │
                         ▼
    ┌─────────────────────────────────────┐
    │  Nadia — reconciliation matrix      │
    │  every requirement: IMPLEMENTED /   │
    │  PARTIAL / DEFERRED / SCOPE CREEP   │
    └────────────────────┬────────────────┘
                         │
                         ▼
                  Human review + approval
```

---

## The Teams

| Team | Description | Agents | Folder |
|------|-------------|--------|--------|
| **Orchestration Team** | Implementation fleet. Turns a task brief into reviewed, integrated code changes. Vera routes, Nadia orchestrates, nine specialists execute. | 11 | [orchestration-team/](orchestration-team/) |
| **Advisory Board** | Standing review board. Evaluates a project across 7 domains and produces a weighted Readiness Score (1–10). Each agent reviews independently. | 10 | [advisory-board/](advisory-board/) |
| **Writing Team** | Creative-writing review board. Reviews manuscripts for continuity, voice, reader experience, craft, and canon consistency. Does not write prose. | 5 | [writing-team/](writing-team/) |
| **TTRPG Team** | Tabletop-RPG pressure-test team. Stress-tests homebrew rules for balance, exploits, and playability across system experts, min-maxers, and a live GM. | 18 | [ttrpg-team/](ttrpg-team/) |

---

## Quick Start

### With Claude Code subagents

Claude Code allows you to define subagents as Markdown persona files in `~/.claude/agents/`. Each file becomes an agent you can spawn from within a Claude Code session using the `Agent` tool.

1. Copy the persona files for the agents you want into `~/.claude/agents/` (or a project-level `.claude/agents/` directory).
2. In a Claude Code session, invoke an agent by its registered role — the orchestrator (Nadia) spawns specialists inline, passing the full task brief in the prompt.
3. The specialist's final message is its completion report. The orchestrator reads that report directly and continues.

Each persona file includes an **Invocation Protocol** section that describes exactly how that agent expects to be called and what it returns.

### With the Claude Agent SDK

Load a persona file's content as the system prompt when instantiating an agent:

```python
# Conceptual — adapt to the SDK version you are using
system_prompt = open("orchestration-team/agents/01-nadia-orchestrator.md").read()
agent = ClaudeAgent(system_prompt=system_prompt, model="claude-opus-...")
response = agent.invoke(task_brief)
```

Each agent's persona file specifies its preferred model (Sonnet or Opus) and the conditions under which it escalates to a more capable model.

### Minimal usage pattern

- **Single implementation task:** invoke Nadia with a task brief. She builds the CDG, plans tiers, spawns specialists, and returns a reconciliation matrix.
- **Project audit:** invoke each advisory board member independently with the project context. Consolidate the 10 individual reports using the weighted formula in `docs/board-review.md`.
- **Manuscript review:** invoke each writing-team member with the manuscript. Each returns a structured critique.
- **Rules stress-test:** invoke the TTRPG team members with the homebrew ruleset. They independently probe for exploits and balance issues.

---

## Repo Layout

```
agent-fleet/
├── README.md                        # this file
├── LICENSE                          # MIT
├── CONTRIBUTING.md                  # how to add agents and teams
│
├── orchestration-team/
│   ├── README.md                    # team overview, flow diagram, invariants
│   ├── agents/
│   │   ├── 00-roster.md
│   │   ├── 00-vera-director.md
│   │   ├── 01-nadia-orchestrator.md
│   │   ├── 02-atlas-reviewer.md
│   │   ├── 03-ash-backend.md
│   │   ├── 04-finn-frontend.md
│   │   ├── 05-zara-security.md
│   │   ├── 06-sam-tester.md
│   │   ├── 07-dev-devops.md
│   │   ├── 08-sage-database.md
│   │   ├── 09-quinn-systems.md
│   │   └── 10-reaper-hygiene.md
│   └── templates/
│       ├── execution-plan.md
│       ├── task-brief.md
│       ├── specialist-report.md
│       ├── atlas-review.md
│       └── reconciliation-matrix.md
│
├── advisory-board/
│   ├── README.md                    # board overview, scoring formula
│   ├── agents/
│   │   ├── 00-roster.md
│   │   ├── 01-alexandra-cfo.md
│   │   ├── 02-marcus-cmo.md
│   │   ├── 03-priya-cpo.md
│   │   ├── 04-dr-reyes-cto.md
│   │   ├── 05-sophie-uiux.md
│   │   ├── 06-chen-auditor.md
│   │   ├── 07-jordan-gaps.md
│   │   ├── 08-kai-devops.md
│   │   ├── 09-viktor-cso.md
│   │   └── 10-evelyn-legal.md
│   └── templates/
│       ├── agent-review.md
│       ├── agent-memory.md
│       ├── consolidated-report.md
│       └── owner-responses.md
│
├── writing-team/
│   ├── README.md
│   └── agents/
│
├── ttrpg-team/
│   ├── README.md
│   └── agents/
│
├── docs/
│   ├── architecture.md              # CDG, tiers, gates, reconciliation matrix
│   ├── orchestration-loop.md        # Nadia's loop end-to-end
│   ├── board-review.md              # advisory board scoring and process
│   └── authoring-an-agent.md        # how to write a good persona file
│
├── examples/
│   └── sample-review/
│       ├── README.md                # what this example illustrates
│       ├── dr-reyes-review.md       # fictional CTO review of Lumina
│       ├── alexandra-review.md      # fictional CFO review of Lumina
│       └── consolidated-report.md   # weighted Readiness Score
│
└── .github/
    └── workflows/
        └── secret-scan.yml          # gitleaks gate on push and PR
```

---

## License

MIT — see [LICENSE](LICENSE).
