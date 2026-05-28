# Token Efficiency

The most common objection to a multi-agent system is that it must cost more tokens than a single agent: more prompts, more coordination, more review passes. That objection is right about the overhead and wrong about the net result — *for the tasks this system is built for.* This document explains where the tokens actually go, why role-scoped subagents and on-demand skills come out ahead, and where they do **not** (so you don't pay for coordination you don't need).

---

## The real cost driver is context, not calls

In a long agent session the dominant token cost is not the number of tool calls — it is the size of the context window that gets re-read on every turn. A single agent that does everything accumulates every file it opens, every grep result, every dead end into one growing transcript. By the time it is deep in a task, each new turn re-processes a large and mostly-irrelevant history. Quality degrades (the signal is buried) and cost climbs (you pay for the whole window, every turn).

The architecture in this repo attacks that directly with four mechanisms.

### 1. Context isolation — the core win

When the orchestrator delegates to a specialist subagent, that specialist runs in its **own** context window. All of its expensive work — reading twenty files, running greps, trial and error — stays in the specialist's window. Only its final report (a few hundred tokens) returns to the orchestrator.

```
Monolithic agent                     Orchestrator + subagents
─────────────────                    ────────────────────────
main context                         main context (orchestrator)
 ├─ read file A   ┐                   ├─ delegate ──► [Backend Engineer ctx]
 ├─ read file B   │ all of this        │                 ├─ read A,B,C,D…
 ├─ read file C   │ piles into          │                 └─ returns 1 report ──┐
 ├─ grep…         │ ONE window          │                                       │
 ├─ read file D   │ and is re-read     ├─ delegate ──► [Test Engineer ctx]      │
 └─ …             ┘ every turn          │                 └─ returns 1 report ──┤
                                        └─ integrates the reports ◄─────────────┘
```

The orchestrator's window holds the *plan and the summaries*, not the raw exploration. It stays lean, so it can coordinate a large task without hitting compaction or drowning in irrelevant detail. The token-heavy reading is quarantined where it is needed and discarded when it is done.

### 2. Right-sized models per task

Each specialist declares the model it runs on — Sonnet for scoped, well-defined work; Opus for cross-file architecture, novel security analysis, or anything where a wrong answer is expensive. You pay Opus rates only on the slices that need Opus. A monolith runs the *entire* task at one tier — and "to be safe" that tier is usually the expensive one.

### 3. Skills load instructions on demand

A skill (a slash command) injects its workflow into context **only when invoked**. The orchestration loop, the advisory-board rubric, the single-issue fix protocol — each lives in its own skill file and is loaded only while that work is happening, instead of sitting in the system prompt for every session. The baseline prompt stays small; the heavy procedure is paged in when, and only when, it is relevant.

### 4. A shared project brain prevents re-exploration

Across multiple runs on the same codebase, the biggest avoidable token sink is re-reading the same files to rebuild the same mental model. A written project-brain snapshot — architecture, key file locations, conventions, gotchas — is built once and passed to specialists as explicit context. Each run starts from the snapshot instead of re-deriving it from scratch.

---

## The honest counter-argument

Coordination is not free. Passing each tier's finalized state forward as explicit context costs tokens. The review gate and the hygiene gate cost tokens. A task split into five tiers pays five rounds of setup.

So the architecture is a **net win** only when both of these hold:

- **The task is large enough** that a single-window agent would bloat its context, force compaction, or lose the thread. Below that threshold, the overhead dominates.
- **The work is genuinely parallelizable or genuinely needs review** — independent changes that can run in separate windows, or changes risky enough that a second set of eyes earns its cost.

For a one-line fix in a single file, this machinery is pure overhead. That is exactly why the repo defines a **lightweight path**: one specialist, no tiers, no board. Use it. The orchestrator's first question on any task is "is this a one-tier job?" — and if it is, it skips its own apparatus.

The point is not "always use many agents." It is "isolate context when context is the cost, and don't when it isn't."

---

## Rules of thumb

| Situation | Use | Why |
|---|---|---|
| One file, well-understood change | Lightweight path (single specialist) | Coordination overhead would exceed the work |
| Many files, independent changes | Full orchestration, parallel tiers | Context isolation + parallelism pay off |
| Repeated runs on one codebase | Shared project brain | Read the architecture once, not every run |
| Mixed difficulty across subtasks | Per-specialist model selection | Pay Opus rates only where they buy something |
| A workflow you run often | A skill, not a bigger system prompt | Load the procedure on demand, not always |

The orchestration model is a tool for managing context as a finite budget. Spend it where it buys correctness or speed; conserve it everywhere else.
