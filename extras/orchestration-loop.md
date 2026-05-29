# Orchestration Loop

This document walks the Orchestrator's orchestration loop end-to-end — from receiving a task brief to handing off the human review package. It also defines the structured report blocks that form the contract between orchestrator and specialists.

> **Scope note.** The validated path is minimal: explore → build the CDG → tier plan → execute in tiers forwarding each tier's *finalized* state → run **one deterministic check** (typecheck / test suite / build) → human review. The extra per-tier gates described in Phase 5 (keyword scan, LLM code review, hygiene sweep, smoke gate) were never validated in a controlled test and are presented here as **optional add-ons**, not mandatory steps. See [../FINDINGS.md](../FINDINGS.md).

---

## Overview

The Orchestrator never writes code. Its job is to ensure that the right specialist works on the right file at the right time with the right context, and that the integrated result passes one deterministic check before a human reviews it. It is the only agent who sees the full picture at all times.

**The lightweight default:** use one agent until the task outgrows a single context window. The CDG, tiering, and subagent coordination below pay off once a task is large enough that a single context can no longer hold it correctly — below that size, one capable agent plus the deterministic check is cheaper and just as correct.

The minimal validated loop:

```
1. Receive brief
2. Explore the codebase
3. Build the CDG
4. Produce the tier plan (await approval if needed)
5. Execute tiers (spawn specialists → forward each tier's finalized state to the next)
6. Run ONE deterministic verification check (typecheck / test suite / build)
7. Produce the reconciliation matrix → hand off to human
```

The per-tier LLM gates (keyword scan, Code Reviewer pass, Hygiene Auditor sweep, smoke gate) are **optional add-ons** layered on top of this loop, not part of it. They are flagged as optional where they appear below.

---

## Phase 1 — Receive Brief

The task brief arrives as the Orchestrator's incoming prompt. It may come from:

- **The Swarm (Director):** when the task is part of a multi-team or multi-project coordination. The Swarm's brief includes cross-team context and sequencing constraints.
- **A human directly:** when the Orchestrator is invoked without the Swarm for a single-project implementation run.
- **The advisory board's consolidated report:** when an implementation run is triggered by a board review cycle. In this case, the consolidated report is the primary input; the Orchestrator reads every board finding before building the CDG.

The Orchestrator's first act is to read and restate the task brief in its own words, confirming its understanding of scope, constraints, and success criteria. This restatement is included in its `[ANALYSIS REPORT]`.

---

## Phase 2 — Explore the Codebase

Before building the CDG, the Orchestrator reads the relevant parts of the codebase. It does not rely on the brief's description of the codebase — it reads the actual files. It specifically looks for:

- Files explicitly named in the brief
- Files that consume any system boundary the brief will change
- Existing patterns (naming conventions, error handling, test structure) that specialists must follow
- Latent issues adjacent to the change area that could create risk

Exploration produces the **project context block** — a summary of what the Orchestrator found, passed to every specialist in their task brief so they are not starting from zero.

---

## Phase 3 — Build the CDG

The Orchestrator constructs the Change Dependency Graph as described in `docs/architecture.md`. The CDG is made explicit — it is not held in the Orchestrator's head. It produces:

- A node list (every artifact in scope)
- An edge list (every dependency relationship)
- A tier assignment for every node

The CDG is included in its `[ANALYSIS REPORT]` and in every specialist task brief. Specialists are expected to flag disagreement with the CDG if they discover during their work that an edge is missing or wrong.

---

## Phase 4 — Tier Plan

From the CDG, the Orchestrator produces the execution plan:

- Which specialists are assigned to which tier
- Which files each specialist owns in that tier
- Where the deterministic verification check will run (the one validated gate)
- Optionally, which add-on gates are in play (keyword scan results, live-surface smoke checks) — see Phase 5

The tier plan is published in an `[ANALYSIS REPORT]` block. For tasks submitted by a human, the human may review and approve the plan before execution begins. This is recommended for any task with three or more tiers.

```
[ANALYSIS REPORT]
Orchestrator
Task: [brief reference]

Restatement:
[the Orchestrator's understanding of scope and success criteria]

CDG — Nodes:
- [file or boundary]: [role in the graph]

CDG — Edges:
- [A] → [B]: [reason for dependency]

Execution Plan:
  Tier 1 (parallel): [Specialist] owns [file(s)]
  Tier 2 (parallel): [Specialist] owns [file(s)]
  ...

Optional gates in play (if any):
  - [gate type]: [reason]

Open questions requiring human input before execution:
  - [question]
[/ANALYSIS REPORT]
```

---

## Phase 5 — Execute Tiers

For each tier, the loop is:

### 5a. Spawn specialists

Each specialist receives a task brief containing:
- The full task description
- The project context block (from Phase 2)
- The CDG (their node highlighted, their dependencies named)
- The finalized file contents from all prior tiers (the integration snapshot)
- Any additional context specific to their domain

Specialists within a tier are spawned in parallel, each in its own context window (the context-isolation property: a specialist explores at length and returns a short report, so the Orchestrator stays lean). Each is one-shot: they do their work, produce their report, and that is their entire contribution to this tier.

### 5b. Integration snapshot (validated — state-forwarding)

When a tier completes, the Orchestrator produces the integration snapshot: the full finalized content of every file modified so far. This is the state Tier N+1 specialists receive directly — they never infer what the previous tier produced. This finalized-state-forwarding is the validated mechanism (0/3 → 3/3 on integration correctness); everything in 5c is optional layered on top of it.

### 5c. Optional add-on gates (unvalidated)

The following per-tier gates were never validated in a controlled test. Run them if you find them useful, but they are not required, and none of them substitutes for the single deterministic check in Phase 6. See [../FINDINGS.md](../FINDINGS.md).

- **Keyword scan (optional).** Scan the tier's changes for triggers (auth, secrets, schema, live surface) and add gate agents — the Security Engineer for security-relevant changes, the Test Engineer for live-surface smoke probes, the Database Engineer for a missed schema change. Note: the eval found LLM security review unreliable relative to a deterministic check, so an auto-invoked LLM security pass is not a substitute for the deterministic gate.
- **Code Reviewer pass (optional).** An LLM review of specialist output returning an APPROVED or REVISE verdict in a `[CODE REVIEW]` block; a REVISE re-spawns the specialist (up to three iterations, then escalate). Useful as a sanity layer, but it is an opinion, not a fact — where it disagrees with the deterministic check, the deterministic check wins.
- **Hygiene Auditor sweep (optional).** A `[HYGIENE REPORT]` identifying unused imports, dead code paths, orphaned exports, and stale references introduced by the tier. Items are addressed in-tier or deferred with justification. Helpful, but unproven as a mandatory step.

---

## Phase 6 — Deterministic Verification (validated gate)

After all specialist tiers complete, run **one deterministic check** against the integrated result — a typecheck, a test suite, or a build — something with an exit code. A non-zero exit is a hard block. This is the one validated guardrail: in the persona eval, every LLM-reviewer arm hallucinated the *same* false positive while a deterministic `mypy` oracle caught the real integration break (see [../FINDINGS.md](../FINDINGS.md)). An LLM review produces an opinion; the deterministic check produces a fact, and where they disagree the fact wins.

In practice the Test Engineer writes or updates tests for the changes across all tiers and runs them against the integration snapshot; the pass/fail of that suite (or the typecheck/build) is the gate.

**Optional, unvalidated cross-tier sweeps** — run if useful, not required:

- **Code Reviewer — full integration sweep (optional).** An LLM review of the complete change set as one body of work, looking for issues only visible across tiers. An opinion, not the gate.
- **Hygiene Auditor — final cross-tier hygiene sweep (optional).** A review of the full diff from baseline to final state for residual dead code or orphaned artifacts.

---

## Phase 7 — Reconciliation Matrix and Human Handoff

The Orchestrator produces the reconciliation matrix (see `docs/architecture.md`) and assembles the human review package:

```
[COMPLETION REPORT]
Orchestrator
Task: [brief reference]
Status: COMPLETE | BLOCKED | PARTIAL

Reconciliation matrix:
| Requirement | Status | Notes |
|-------------|--------|-------|
| ...         | ...    | ...   |

Files changed:
- [path]: [specialist] — [one-line description]

Deterministic check (validated gate):
- [typecheck | test suite | build]: [PASS | FAIL] — [command + exit code]

Tests written:
- [test file or test name]: [what it covers]

Optional add-on results (if any were run):
- Smoke / drill: [PASS | FAIL | N/A] — [notes]
- Hygiene Auditor: [CLEAN | items addressed | items deferred with reason]
- Code Reviewer integration sweep: [notes | N/A]

Open items:
- [anything requiring human decision before commit]

Reviewer checklist:
[ ] Review reconciliation matrix — all IMPLEMENTED items verified
[ ] Review open items — decision recorded
[ ] Approve commit
[/COMPLETION REPORT]
```

Nothing is committed without explicit human approval. The reconciliation matrix and the open-items list are the human's decision surface. The human's job at this point is to verify that IMPLEMENTED items were actually implemented as described, make decisions on DEFERRED and SCOPE CREEP items, and give the approval signal.

---

## Iteration and Escalation

- Each specialist gets at most 3 iterations per task (initial + 2 revisions). On the third failure, the Orchestrator escalates to the human with a summary of what was attempted and what the blocker is.
- If the CDG itself is wrong (discovered mid-execution), the Orchestrator halts, revises the CDG, and restarts affected tiers. It does not continue with a known-wrong dependency graph. (This protects the validated state-forwarding mechanism.)
- A non-zero exit on the deterministic check (Phase 6) is a hard block — the result is not handed to the human as complete until it passes or the failure is explicitly documented for human decision.
- If an optional Security Engineer pass finds a blocking issue, treat it as a reason to halt and resolve before continuing — but remember it is an LLM opinion, and the deterministic check, not the security persona, is the validated gate.

---

## The Swarm / Director Layer (optional, unvalidated)

> The cross-team director hierarchy below was **never validated in a controlled test.** It is an optional coordination layer, not part of the recommended core. For a single-project, single-team implementation — and for most work — invoke the Orchestrator directly; the Swarm is not needed. See [../FINDINGS.md](../FINDINGS.md).

The Swarm sits above the Orchestrator. As designed, it is engaged when:

- Multiple independent workstreams need to run in parallel (e.g., separate frontend and backend teams each with their own Orchestrator).
- A single task spans team boundaries (e.g., an advisory board re-review feeds simultaneously into an implementation run and a documentation update).
- An implementation cycle needs to be coordinated with a board review cycle.

These are plausible uses, but the layer's value is asserted, not measured. The lightweight default — one agent, scaling up to a single Orchestrator only when a task outgrows one context window — is the recommendation.
