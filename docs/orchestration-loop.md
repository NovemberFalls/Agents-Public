# Orchestration Loop

This document walks the Orchestrator's orchestration loop end-to-end — from receiving a task brief to handing off the human review package. It also defines the structured report blocks that form the contract between orchestrator and specialists.

---

## Overview

The Orchestrator never writes code. Its job is to ensure that the right specialist works on the right file at the right time with the right context, and that every output is reviewed before it is accepted. It is the only agent who sees the full picture at all times.

The loop has seven phases:

```
1. Receive brief
2. Explore the codebase
3. Build the CDG
4. Produce the tier plan (await approval if needed)
5. Execute tiers (spawn specialists → Code Reviewer review → Hygiene Auditor sweep → smoke gate)
6. Produce the reconciliation matrix
7. Hand off to human
```

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
- Which mandatory gates apply (keyword scan results)
- Which gates require external confirmation (e.g., live-surface smoke gates)

The tier plan is published in an `[ANALYSIS REPORT]` block. For tasks submitted by a human, the human may review and approve the plan before execution begins. This is recommended for any task with three or more tiers or with Security Engineer involvement.

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

Mandatory gates triggered:
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

Specialists within a tier are spawned in parallel. Each is one-shot: they do their work, produce their report, and that is their entire contribution to this tier.

### 5b. Keyword scan

Before accepting any tier's output, the Orchestrator runs the keyword scan against all changes in the tier. If triggers fire (auth, secrets, schema, live surface), the appropriate gate agents are added:

- **The Security Engineer** reviews security-relevant changes and produces a security finding report.
- **The Test Engineer** runs smoke probes if a live surface is involved.
- **The Database Engineer** is consulted if a schema change was missed in the tier plan.

### 5c. Code Reviewer review

All output from Opus-model specialists is reviewed by the Code Reviewer before reaching the Orchestrator. The Code Reviewer produces a `[CODE REVIEW]` block with an APPROVED or REVISE verdict. A REVISE verdict sends the specialist's work back with specific revision notes. The specialist is re-spawned (up to three iterations total; on the third failure, the Orchestrator escalates to the human).

The Code Reviewer reviews Sonnet-model output only on the Orchestrator's explicit request — typically for output that touches a critical system boundary.

### 5d. Hygiene Auditor sweep

The Hygiene Auditor runs after every tier. It reads the tier's changes and the integration snapshot, then produces a `[HYGIENE REPORT]` identifying:

- Unused imports introduced by this tier's changes
- Dead code paths exposed by the changes
- Orphaned exports that nothing now imports
- Stale references to renamed or removed symbols

The Hygiene Auditor's findings are either clean (tier accepted) or contain items to address. Items are addressed in the same tier by re-spawning the relevant specialist, or deferred with justification. No tier is finalized with open hygiene findings unless the Orchestrator explicitly defers them with a documented reason.

### 5e. Integration snapshot

After the Hygiene Auditor clears the tier, the Orchestrator produces the integration snapshot: the full finalized content of every file modified so far. This is the state Tier N+1 specialists will receive.

---

## Phase 6 — Cross-Tier Final Review

After all specialist tiers complete, three final passes run:

1. **Test Engineer — full test pass:** the Test Engineer writes or updates tests for all changes across all tiers, runs them against the integration snapshot, and reports coverage and failures.

2. **Code Reviewer — full integration sweep:** the Code Reviewer reviews the complete set of changes across all tiers as a single body of work, looking for issues that only become visible when all tiers are seen together.

3. **Hygiene Auditor — final cross-tier hygiene sweep:** the Hygiene Auditor reviews the full diff from baseline to final state, catching any residual dead code or orphaned artifacts that per-tier sweeps may have missed.

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

Tests written:
- [test file or test name]: [what it covers]

Smoke / drill results:
- [gate]: [PASS | FAIL | N/A] — [notes]

Hygiene Auditor summary:
- [CLEAN | items addressed | items deferred with reason]

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
- If the CDG itself is wrong (discovered mid-execution), the Orchestrator halts, revises the CDG, and restarts affected tiers. It does not continue with a known-wrong dependency graph.
- If the Security Engineer's security review finds a blocking issue, the implementation halts until the issue is resolved. Security findings do not get deferred.

---

## The Swarm's Role

The Swarm sits above the Orchestrator. It is engaged when:

- Multiple independent workstreams need to run in parallel (e.g., separate frontend and backend teams each with their own Orchestrator).
- A single task spans team boundaries (e.g., an advisory board re-review feeds simultaneously into an implementation run and a documentation update).
- An implementation cycle needs to be coordinated with a board review cycle.

For a single-project, single-team implementation, invoke the Orchestrator directly. The Swarm is not needed for single-stream work.
