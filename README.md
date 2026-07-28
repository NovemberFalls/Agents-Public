# swarmsmith

> A small, validated orchestration model for multi-agent coding work with Claude Code
> and the Claude Agent SDK — the **`/orchestrate`** loop. This is **the instrument**,
> not the paper.

> **🔬 This repo is the apparatus behind a research program.** swarmsmith is the
> orchestration harness that the **[deterministic-evals](https://github.com/NovemberFalls/deterministic-evals)**
> studies measure — the skills, agents, and deterministic gate that lower a task to
> application so cheap hands can execute it. The **findings** live in the program, each
> scored only where a deterministic oracle exists:
>
> - **[gate-on-the-fact](https://github.com/NovemberFalls/gate-on-the-fact)** — a persona is theater; gate on a fact. *(confirmed)*
> - **[capability-isnt-free](https://github.com/NovemberFalls/capability-isnt-free)** — capability above the task is wasted spend; route to the cheapest tier that clears the gate. *(confirmed, 2 fixtures)*
> - **[cheapest-hands](https://github.com/NovemberFalls/cheapest-hands)** — cheap/local hands clear the gate once the spec lowers the task. *(partial — local 30B confirmed)*
>
> The raw data quarry is **[FINDINGS.md](FINDINGS.md)** — *One Skill to Run a Swarm* —
> which the studies cite at a pinned commit. Interactive charts, every losing run
> shown: **[boord-its.com/skills](https://boord-its.com/skills)**. The living skill,
> the enforcement hooks, and the museum of retired generations are all here.

---

## What this is

The **`/orchestrate`** loop: a way to run multi-agent coding work that is **measured, not asserted.** Three ideas carry it, and only these:

1. **The Change Dependency Graph (CDG)** — the rockstar. Sequence parallel work, finalize an upstream change before the downstream agent starts, and hand the downstream agent the *real* finalized state instead of letting it guess. In a controlled test this was the entire difference between **0/3 and 3/3** on integration correctness.
2. **Context isolation via subagents** — each specialist explores in its own window and returns a short report, so the coordinator stays lean enough to run a large task without compaction.
3. **One deterministic check** — gate the integrated result with a typecheck / test suite / build (something with an exit code). **Not** an LLM "review" gate. See [docs/the-deterministic-check.md](docs/the-deterministic-check.md).

Plus one rule: **use a single agent until the task outgrows one context window.** Below that line, coordination is pure overhead.

Everything is Markdown — persona files and process. No application code.

---

## What we were wrong about

The honest version, in full in [FINDINGS.md](FINDINGS.md):

- **Persona backstories did nothing *for detection*.** A placebo-controlled ablation: a security reviewer's elaborate red-team backstory caught no more bugs than a bare "you are a security reviewer," and a *performance-engineer* backstory did just as well on security bugs. Identities are kept as **flavor** — useful for a legible roster (and plausibly for shaping *response format*, which we didn't test), not because they improve what a reviewer *finds*.
- **The mandatory-gate battery and the director hierarchy were never validated** — and the extra review passes, re-passed state, and parallel ceremony **cost tokens** without earning them. They're demoted to optional, and the heavier pieces moved to [`extras/`](extras/).
- **More agents isn't better on small tasks.** A plain monolith was cheapest *and* correct; coordination only pays once a task is too big for one window.

The takeaway: **keep the CDG, keep context isolation, gate with a deterministic check, and don't over-build.** That's the whole product.

---

## Quick start

### The command

`/orchestrate <task>` — one self-scaling entry point, now at **v4.1**: it *counts* the work (sites, files, read volume), prints a `GATE: SOLO|SWARM` verdict, and obeys it — solo with checklist discipline below the measured crossover, a lane-routed worker swarm (haiku/sonnet/opus) with a plan file and deterministic gates above it. The skill is [`.claude/commands/orchestrate.md`](.claude/commands/orchestrate.md) (with [`fix.md`](.claude/commands/fix.md) for the explicit single-issue path). Copy them into `~/.claude/commands/`.

### The agents

The specialists `/orchestrate` spawns live in [`orchestration-team/agents/`](orchestration-team/agents/) — each a valid Claude Code subagent (`name` + `description` + `model`). Copy the ones you want into `~/.claude/agents/`, or load a file's body as an Agent SDK system prompt.

### The gate

Wire a deterministic check (typecheck/test/build) as the one required gate — the pattern and the exact mypy setup that worked in our eval are in [docs/the-deterministic-check.md](docs/the-deterministic-check.md).

### The dials (measured, Round 3 — full ladders)

Run the **orchestrator at high reasoning effort, not max** — same correctness, −44% cost on the planning-heavy fixture. The complete ladder adds nuance: the *bottom* rung matched or beat it on cost (tie-breaks pending) while the *middle* rung is where correctness cracked — if you deviate from high, go down, never halfway. A top-tier model in the orchestrator seat is the measured **speed** configuration (all-time wall records, a two-turn swarm at minimum effort) at roughly double the seat cost. Worker lanes hold far below their labels when briefs carry the exact rules and traps. Optional [`hooks/`](hooks/) turn the routing rules into denied tool calls.

---

## Repo layout

```
swarmsmith/
├── README.md
├── FINDINGS.md                     # the raw data quarry the studies cite (pinned)
├── orchestration-team/
│   ├── README.md
│   ├── agents/                     # Orchestrator + 7 role specialists (+ optional reviewer, hygiene-auditor)
│   └── templates/
├── docs/
│   ├── architecture.md             # the CDG, tiers, the verification gate
│   ├── the-deterministic-check.md  # the one validated gate — how to wire it
│   ├── token-efficiency.md         # where the tokens go (and where the ceremony bled them)
│   └── authoring-an-agent.md
├── .claude/commands/
│   ├── orchestrate.md              # the loop (v4.1 — computed gate, plan-as-data, lanes)
│   └── fix.md                      # the lightweight path
├── hooks/                          # optional enforcement: mandate + lane floor/ceiling as denied tool calls
├── archive/                        # retired generations + why each died (the ledger)
├── examples/
│   ├── eval/                       # the controlled experiments (CDG validated; backstory not)
│   ├── real-run/                   # metered tokens from the run that built this repo
│   └── orchestrated-run/           # a worked CDG example + context ledger
└── extras/                         # NOT the validated core — kept for reference
    ├── README.md
    ├── advisory-board/ · writing-team/ · ttrpg-team/   # the pattern applied to other domains (untested)
    ├── swarm.md · orchestration-loop.md                # the director layer + the old gated loop
    └── board-review.md · sample-review/                # advisory scoring + example
```

---

## Built by

**November Falls.**

## License

MIT — see [LICENSE](LICENSE).
