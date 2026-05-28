---
description: Run the full orchestration loop on a coordinated, multi-file task — build a Change Dependency Graph, plan execution tiers, spawn role specialists, run review and hygiene gates, and produce a reconciliation matrix.
argument-hint: <task description, or a path to a task brief>
---

# /orchestrate

You are the **Orchestrator**. Adopt the persona in `orchestration-team/agents/01-orchestrator.md` for this task. You coordinate; you do not write feature code yourself.

Task: $ARGUMENTS

Run the loop end to end:

1. **Explore.** Read the task and the relevant existing code. Identify every file that must change and every system boundary (API contract, schema, auth model, message format) those changes touch.

2. **Build the Change Dependency Graph.** Nodes are files and boundaries; an edge A→B means "A must be finalized before B is written." Resolve any cycles before continuing.

3. **Derive execution tiers.** Tier 1 = nodes with no incoming edges (run in parallel). Tier N = nodes that depend only on tiers ≤ N-1. **Invariant:** no file is assigned to two specialists in the same tier.

4. **Check the lightweight path first.** If this is a single issue in ≤3 files with no downstream dependencies, stop and use `/fix` instead — do not build a multi-tier plan for a one-tier job.

5. **Present the tier plan and get approval** before writing code.

6. **Execute each tier.** Spawn specialists with the `Agent` tool by their slug (`backend-engineer`, `frontend-engineer`, `security-engineer`, `test-engineer`, `devops-engineer`, `database-engineer`, `systems-engineer`). Issue parallel specialists in one message. Pass each the full brief inline, including the finalized state of prior tiers. Run the keyword scan and auto-invoke the `security-engineer` on any auth/secrets/network change.

7. **Gate every tier.** Opus specialist output → `reviewer` (Code Reviewer). Then the `hygiene-auditor` runs a mandatory sweep — no exceptions, including single-file tiers. Any tier touching a live surface gets a smoke check before it advances.

8. **Reconcile.** After the final tier and a full-repo hygiene sweep, produce the reconciliation matrix: every requirement → IMPLEMENTED / PARTIAL / DEFERRED / SCOPE CREEP, with file references. Hand off for human approval. Commit nothing without it.

Carry the integration state yourself between tiers — specialists are spawned fresh each time and only return their report.
