# Eval — Is the Change Dependency Graph load-bearing, or ceremony?

> A real experiment on a real codebase. Not fictional, not a model — agents were run, an objective oracle scored them, and the numbers below are what happened.

> **This folder holds two evals.** This file tests the *Change Dependency Graph*. [`persona-backstory.md`](persona-backstory.md) tests whether the persona *backstory* improves output (it found no measurable effect). Together they say: the coordination discipline earned its keep; the character sheets did not.

The rest of this repo *asserts* that the orchestration loop prevents the most common multi-agent failure: a specialist building against a contract another specialist changed. This eval **tests** the single claim that actually matters — that **forwarding each tier's finalized state to the next tier** (the core of the [Change Dependency Graph](../../docs/architecture.md)) is what prevents that failure, rather than the personas, the gates, or the org chart.

It isolates exactly one variable: **does the agent updating the consumers receive the finalized contract, or not?**

---

## Setup

- **Substrate:** a real, private, fully type-annotated FastAPI + Pydantic service (not this repo). The contract is a four-field Pydantic model — `kills`, `assists`, `deaths`, `kda` (combat metrics over a time window) — constructed and read in two separate router modules.
- **The task:** *"These four fields are ambiguously named — rename them to clearer, more precise names."* The renamer **chooses the new names freely.** That free choice is what makes the trap fair instead of rigged: a second agent genuinely cannot know whether the renamer will pick `pvp_kills`, `pvp_killing_blows`, `killing_blows`, etc.
- **Oracle:** `mypy` with the Pydantic plugin, scored as the count of `"…" has no attribute "…"` errors on the model. **0 = integration intact (PASS); ≥1 = broken (FAIL).** Exit-code objective — not a human judgment. (Validated before running: a field rename with one stale consumer reliably produces `error: "CombatWindowTotals" has no attribute "kills"`.)
- **Three arms, N = 3 runs each:**
  - **A — Monolith:** one agent renames the model *and* updates every consumer, in one context window.
  - **B — Naive parallel:** the renamer and the consumer-updater work independently; the updater **never sees the renamer's chosen names** (enforced — see "What went sideways").
  - **C — CDG-ordered:** the renamer finalizes first; the consumer-updater is then handed the **finalized names** and updates the consumers.

---

## Results

| Arm | Run 1 | Run 2 | Run 3 | Pass rate | Avg tokens |
|-----|:-----:|:-----:|:-----:|:---------:|:----------:|
| **A — Monolith** | PASS | PASS | PASS | **3/3** | ~51,000 |
| **B — Naive parallel (blind)** | FAIL | FAIL | FAIL | **0/3** | ~96,000 |
| **C — CDG-ordered** | PASS | PASS | PASS | **3/3** | ~89,000 |

Token figures are harness-reported, summed across the agent(s) in each run.

---

## Why B failed — the mechanism

Independent agents **agree on the obvious names and diverge on the ambiguous ones.** Across all runs:

| Field | Renamer chose | Blind updater chose | Match? |
|-------|---------------|---------------------|:------:|
| `assists` | `pvp_assists` | `pvp_assists` | ✅ every time |
| `deaths` | `pvp_deaths` | `pvp_deaths` | ✅ every time |
| `kills` | `pvp_killing_blows` | `pvp_kills` | ❌ every time |
| `kda` | `pvp_kda_ratio` | `pvp_kda` | ❌ every time |

Every single Arm B failure was those two ambiguous fields — the blind updater confidently produced `combat.pvp_kills` / `combat.pvp_kda` against a model that had `pvp_killing_blows` / `pvp_kda_ratio`. In Arm C the updater was handed those exact names and matched perfectly, every run. **Coordination matters precisely where naming is ambiguous — which, in a real refactor, is most of the time.**

---

## What this proves — and what it does NOT

**Proves (the repo's load-bearing claim holds):** forwarding finalized state is the entire difference between **0/3 and 3/3** once work is parallelized. Same task, same agents, same oracle — the only variable was whether the consumer-updater received the renamer's actual choice. The Change Dependency Graph is not ceremony; it is the thing that makes parallel agents safe.

**Does NOT prove orchestration is cheaper.** The **monolith was both the cheapest (~51K) and fully correct (3/3).** Arm C cost ~73% more than the monolith for the *same* correct result. So the value of the orchestration machinery is **not** cost — it is that *if you must parallelize* (to isolate context on a task too large for one window), the CDG is what stops the parallel agents from breaking each other. On a task this small — three files, comfortably one window — the correct move is the monolith / [lightweight path](../../.claude/commands/fix.md), exactly what the repo prescribes. **The CDG earns its keep only above the size where one window stops being enough.**

**Honest limits:** N = 3 (a pilot, not a powered study); one contract on one repo; a rename (the simplest kind of contract change).

---

## What went sideways (the honest part)

Two things broke during the eval, and both are worth more than a clean result would have been:

1. **Blindness leaked through the filesystem.** The first Arm B attempt ran both agents on one shared working tree. The renamer won the race, and the "blind" updater simply **read the finalized names off disk** — silently turning Arm B into Arm C. Those runs were discarded and Arm B was re-run with **enforced isolation**: the updater works against the *original* model (the new names do not exist yet), and its output is combined with the renamer's afterward. *This is itself a finding:* naive-parallel agents on a shared tree will read each other's half-finished work nondeterministically — a coordination hazard in its own right.

2. **An agent dodged the question.** In one discarded run, the blind updater refused to guess and instead wrote **dynamic, order-dependent field resolution** (`getattr` over `model_fields`) — passing the typecheck via a fragile workaround it was never asked for, and editing an out-of-scope file to do it. A free-form rename leaves that escape hatch open; a **structural** change (e.g. splitting one field into two) would close it and is the stronger trap for a follow-up.

A note on the oracle, too: mypy only catches the mismatch **with the Pydantic plugin enabled** — plain mypy treated the consumer's model instance as `Any` and saw nothing. Worth knowing if you reproduce this.

---

## Reproduce

1. Pick a typed Pydantic (or TypeScript) codebase with a model whose fields are consumed in another module.
2. Define the rename task with **free name choice** for the renamer.
3. Run the three arms; for B, ensure the consumer-updater **cannot** see the renamer's output (separate trees, combined afterward).
4. Score with `mypy` (+ pydantic plugin) or `tsc --noEmit` — count attribute/contract errors on the model.
5. Repeat N times; report pass rate and tokens per arm.

---

## Bottom line

Strip the eval down to its result: **the personas and the "mandatory gates" are not what this validates. Context isolation is just using subagents as intended. The one idea here with teeth is the Change Dependency Graph — dependency-ordered forwarding of finalized state — and it pays for itself exactly when a task is big enough to need parallel agents. Below that line, one agent is cheaper and just as correct.**
