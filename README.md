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

One self-scaling entry point: it *counts* the work (sites, files, read volume), prints a `GATE: SOLO|SWARM` verdict, and obeys it — solo with checklist discipline below the measured crossover, a lane-routed worker swarm (haiku/sonnet/opus) with a plan file and deterministic gates above it.

**Current champion — [`.claude/commands/orch-anth-5.0.md`](.claude/commands/orch-anth-5.0.md) (v5.0).** v4.1 plus a **deterministic apply-tier**: on mechanical fan-out the orchestrator computes the exact change and emits verbatim SEARCH/REPLACE blocks that a stdlib applier lands — no worker model in the edit path.

**The crown is scoped, and the scope is the finding.** Measured against v4.1's canonical *swarm* path (opus/low, identical toolset, 46 harness-recorded runs, 2026-07-31):

| where | v5.0 | v4.1 | crown |
|---|---|---|---|
| Small/medium (~28K tok), k=5 | **10/10**, $1.91 / $5.47 per result | 7/10, $4.03 / $8.65 | **v5.0** — 1.6–2.1× cheaper per result |
| Large (400K tok), k=3 | 3/3, $10.10, 871s | 3/3, $11.00, 1118s | **tie on correctness** |
| Hygiene, k=3 | 3/3 (v5.1, $0.60) | 3/3, **$0.53** | **v4.1** — cheapest at equal correctness |

Read the denominator: per *attempt* v4.1 is marginally faster on the refactor fixture and the two are within 6%. The entire economic win is conversion rate — v5.0 converts every attempt, v4.1 converts 7 of 10. Earlier "1.9× faster / 2.0× cheaper" figures compared against a **solo-restricted** v4.1; corrected in [FINDINGS.md §4.7a](FINDINGS.md), along with a null result for the mandatory clean phase (+30% cost, no correctness gain) and a harness bug that understated turn counts in 35% of retained streams.

**Install v5.0 with [`packages/coding-v5.0/`](packages/coding-v5.0/) — don't just copy the markdown.**

```bash
python packages/coding-v5.0/install.py          # skill + applier, pinned together
python packages/coding-v5.0/install.py --check  # verify; exit 1 on drift
```

v5.0's apply-tier calls a **deterministic applier**, and the skill and that tool are one contract: the skill emits SEARCH/REPLACE in exactly one format, the applier applies a block *iff* its SEARCH matches exactly once. Copying the skill file alone leaves you with a skill describing a tool you don't have — and substituting an approximate one is measurably **worse than not installing it at all** (a model handed a flawed "exact" patch scored 8/16, *below* the same model working from the spec at 10/20; see [FINDINGS.md](FINDINGS.md) §4.7). The installer checksums everything, touches no hooks, and edits no settings. Python 3.8+, stdlib only.

Also here: [`orchestrate.md`](.claude/commands/orchestrate.md) — the **v4.1** predecessor, kept as rollback and as the readable baseline v5.0 is measured against; [`orch-anth-5.0-mega.md`](.claude/commands/orch-anth-5.0-mega.md) — a **PROPOSED, unbenched** director tier that spawns one sub-orchestrator per partition (mechanism proved, payoff not yet measured); and [`fix.md`](.claude/commands/fix.md) — the explicit single-issue path (also installed by the package). Those you can copy into `~/.claude/commands/` directly, as they have no tool dependency.

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
├── packages/
│   └── coding-v5.0/                # INSTALL THIS — v5.0 skill + its applier, pinned + checksummed
│       ├── install.py              #   --check / --uninstall; no hooks, no settings edits
│       ├── commands/               #   orch-anth-5.0.md, fix.md
│       ├── tools/apply_blocks.py   #   the deterministic applier §4.9 depends on
│       └── tests/                  #   27 tests pinning the apply contract
├── .claude/commands/
│   ├── orch-anth-5.0.md            # the champion (v5.0 — v4.1 + deterministic apply-tier)
│   ├── orch-anth-5.0-mega.md       # PROPOSED director tier (recursive sub-orchestration)
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
