# Agents-Public

> A small, validated orchestration model for multi-agent coding work with Claude Code and the Claude Agent SDK — the **`/orchestrate`** loop.

> **📋 Read [FINDINGS.md](FINDINGS.md) first.** This repo started as an elaborate multi-agent fleet — rich personas, a battery of mandatory gates, a director hierarchy, four teams. We tested our own assumptions. **Most of the elaboration didn't help, and the ceremony bled tokens the whole time.** The one thing that earned its keep was the **Change Dependency Graph**. So the repo has been cut down to what the evidence supports. The rest is preserved, honestly labeled, in [`extras/`](extras/).
>
> **Round 2 (2026-07):** we then benchmarked six generations of the skill itself on purpose-built fixtures with held-out oracles — and found the *knowing-doing gap* (skills that plan routing, then defect), the real scale crossover, and three defects in our own redesign, caught by its own telemetry. The live skill is now **v4.1** (computed SOLO/SWARM gate, plan-as-data, model lanes); every retired generation sits in [`archive/`](archive/) with its retirement reason. Numbers and charts: **[boord-its.com/skills](https://boord-its.com/skills)**.
>
> **Round 3 (2026-07):** then we measured *effort*. The orchestrator holds full correctness one reasoning notch below max (−44% on the planning-heavy fixture, new record at the scale wall), and real worker briefs replayed at every lane × effort passed **18/18** — a good enough brief makes the worker tier a speed dial, not a correctness dial. The enforcement hooks that keep routing honest in both directions now ship in [`hooks/`](hooks/).

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

- **Persona backstories did nothing.** A placebo-controlled ablation: a security reviewer's elaborate red-team backstory caught no more bugs than a bare "you are a security reviewer," and a *performance-engineer* backstory did just as well on security bugs. Identities are kept as **flavor** — useful for a legible roster, not because they improve output.
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

### The dials (measured, Round 3)

Run the **orchestrator at high reasoning effort, not max** — same correctness, −44% cost on the planning-heavy fixture. Worker lanes hold far below their labels when briefs carry the exact rules and traps; where demotion is legal, prefer big-model/low-effort over small-model/max-effort. Optional [`hooks/`](hooks/) turn the routing rules into denied tool calls.

---

## Repo layout

```
Agents-Public/
├── README.md
├── FINDINGS.md                     # what we tested, what held, what we were wrong about
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
