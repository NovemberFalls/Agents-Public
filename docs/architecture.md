# Architecture

This document explains the coordination model used by the orchestration team: the Change Dependency Graph, execution tiers, the verification gate, and the reconciliation matrix.

The **validated core** of this system is small: the CDG, context isolation via subagents, and exactly one deterministic verification check. The CDG was validated in a controlled experiment — dependency-ordered state-forwarding was the difference between 0/3 and 3/3 on integration correctness (see [../examples/eval/README.md](../examples/eval/README.md)). The deterministic check earns its place because in the persona eval an LLM "review" gate hallucinated a false positive while a deterministic oracle caught the real bug.

The richer machinery — the additional gate battery and the director/cross-team layer — was never validated in a controlled test. It is presented below as **optional, unvalidated add-ons**, not as mandatory. See [../FINDINGS.md](../FINDINGS.md) for the full account of what was tested and what was not.

---

## The core problem

When multiple specialists work on a codebase simultaneously, every specialist starts from a snapshot of the codebase taken at invocation time. If Specialist A changes `api/routes.py` and Specialist B changes `frontend/api-client.ts` simultaneously, and A's change alters the response schema, B is now writing a client for a contract that no longer exists. Neither specialist did anything wrong in isolation. The coordination model failed.

Serializing everything — running one specialist at a time — solves the staleness problem but discards the efficiency of parallel specialization. The goal is parallel execution where it is safe and sequential execution where it is necessary.

The Change Dependency Graph determines the boundary.

---

## Change Dependency Graph (CDG)

The CDG is built by the Orchestrator before any specialist writes a line of code.

**Nodes** are every artifact that will be modified or that acts as a coordination surface:
- Source files (each file is a node)
- System boundaries (API contract, database schema, authentication model, message queue schema, event contracts)

**Edges** represent dependencies: an edge from A to B means "modifying A requires B to be in a known, finalized state first." Edges are directional. Cycles indicate a design problem that must be resolved before execution begins.

**Building the CDG:**
1. Read the task brief and all relevant existing code.
2. Identify every file that must change.
3. For each file, identify which system boundaries it touches or exposes.
4. For each system boundary, identify every other file that consumes it.
5. Draw directed edges: if File X exposes a boundary consumed by File Y, X must be finalized before Y is written.

The CDG is explicit and shared. It is included in every specialist's task brief so each specialist understands which of their outputs is a dependency for downstream work.

---

## Execution Tiers

From the CDG, the orchestrator derives execution tiers.

**Tier 1** contains nodes with no incoming edges — changes that depend on nothing else in this task. These run in parallel.

**Tier 2** contains nodes whose only incoming edges are from Tier 1 nodes. These run after Tier 1 is finalized and reviewed.

**Tier N** contains nodes that depend on Tier N-1 being complete. Each tier runs sequentially relative to the previous tier; specialists within a tier run in parallel relative to each other.

**The file-per-tier invariant:** A file is assigned to at most one specialist per tier. No two specialists ever edit the same file within the same tier. If two changes to the same file are needed, they are either combined (one specialist does both) or sequenced across tiers.

**State synchronization:** At the end of each tier, the orchestrator produces an integration snapshot — the full finalized state of every file modified in that tier. This snapshot is passed as explicit input context to every specialist in the next tier. Specialists in Tier N never infer what Tier N-1 produced; they receive it directly.

---

## Worked Example

Fictional project: **Verdant**, an open-source task management API.

**Task brief:** Add user tagging to tasks. Tags are stored in a new `task_tags` join table. The REST API gains two new endpoints. The existing task detail endpoint is updated to include tags in its response. The frontend task card component is updated to display tags.

**Step 1 — identify artifacts:**
- `db/migrations/0012_task_tags.sql` (new migration)
- `db/models/task.py` (updated Task model with tags relation)
- `api/routes/tasks.py` (two new endpoints + updated detail endpoint)
- `api/schemas/task.py` (updated response schema — tags field added)
- `frontend/components/TaskCard.tsx` (display tags)
- `frontend/api/tasks.ts` (API client — updated to expect tags in response)

**Step 2 — identify system boundaries:**
- Database schema (consumed by: model layer, migration)
- API response contract for `GET /tasks/{id}` (consumed by: frontend client)

**Step 3 — draw edges:**
```
0012_task_tags.sql ──► task.py (model needs schema to exist)
task.py ──────────────► tasks.py (routes use the model)
tasks.py ─────────────► task.py (schema — response shape)
task.py (schema) ─────► TaskCard.tsx (frontend uses the schema)
task.py (schema) ─────► tasks.ts (API client uses the schema)
```

**Step 4 — derive tiers:**

```
Tier 1 (parallel):
  - Database Engineer: write 0012_task_tags.sql
  (no dependencies; everything else depends on the schema existing)

Tier 2 (parallel, after Tier 1):
  - Database Engineer: update db/models/task.py  (depends on Tier 1 migration)
  - Backend Engineer:  update api/schemas/task.py  (can be drafted from the migration)

Tier 3 (parallel, after Tier 2):
  - Backend Engineer:  update api/routes/tasks.py  (depends on model + schema)
  - Frontend Engineer: update frontend/api/tasks.ts  (depends on finalized schema)

Tier 4 (after Tier 3):
  - Frontend Engineer: update frontend/components/TaskCard.tsx  (depends on API client shape)

Tier 5:
  - Test Engineer: write tests for all new endpoints and the updated frontend component
```

In this example, Tier 1 and Tier 2 are database-specialist work. Tier 3 splits across the Backend Engineer and the Frontend Engineer — they can run in parallel because their outputs do not depend on each other within Tier 3. Tier 4 waits because the component depends on the finalized API client.

---

## The Verification Gate (validated)

There is exactly **one** gate in the recommended core, and it is deterministic.

### Deterministic verification check

Before an integrated result is handed to the human, gate it with something that has an exit code — a typecheck, a test suite, or a build. Not an LLM "review" pass. This is the guardrail with evidence behind it: in the persona eval, every LLM-reviewer arm emitted the *same* hallucinated false positive, while the deterministic `mypy` oracle is what actually caught the real integration break (see [../FINDINGS.md](../FINDINGS.md) and [../examples/eval/](../examples/eval/)). A reviewer persona produces an opinion; a typecheck/test/build produces a fact.

Run the deterministic check on the integrated state after the tiers complete, and treat a non-zero exit as a hard block. That is the validated gate.

---

## Optional, unvalidated add-ons

Everything in this section is **available but was never validated in a controlled test.** It is asserted, not evidenced. Treat these as optional knobs, not as mandatory gates — and read [../FINDINGS.md](../FINDINGS.md) before relying on any of them as if they were load-bearing. None of them is part of the recommended core; the lightweight default (one agent, plus the deterministic check when the task outgrows a single context window) is the recommendation.

### Keyword scan (auto-invocation) — optional

A pattern-triggered scan that adds gate agents before a tier executes:

| Keyword / pattern | Auto-invoked agent | Reason |
|---|---|---|
| auth, session, JWT, token, password, credential, secret, API key | Security Engineer | Authentication and secrets surface requires security review |
| migration, schema change, ALTER TABLE, DROP COLUMN, INDEX | Database Engineer + Test Engineer | Schema changes have irreversible failure modes |
| deploy, publish, release, live endpoint, public surface | Test Engineer — smoke gate | Changes reaching a live surface need verification before full rollout |

The intent is that specialists do not self-gate — the orchestrator runs the scan and adds agents. This is a reasonable-sounding policy, but note that the eval found LLM reviewers (including security review) unreliable relative to a deterministic check; an auto-invoked LLM security pass is not a substitute for the deterministic gate above.

### Code hygiene sweep (Hygiene Auditor) — optional

A sweep that identifies dead code, unused imports, orphaned files, and stale exports introduced or exposed by a tier's changes, with its report folded into the integration snapshot. The original design ran this after every tier including lightweight single-file tiers, plus a final cross-tier sweep. It was never validated as carrying its weight; run it if you find it useful, but it is not required.

### Code Reviewer (LLM review) pass — optional

An LLM review of specialist output (originally: all Opus-model output) before it reaches the Orchestrator, returning approve-or-revise. Useful as a sanity layer, but it is an LLM opinion, not a deterministic check — and is explicitly *not* the validated gate. Where they disagree, the deterministic check wins.

### Smoke gate — optional

For tiers touching a live surface (a deployed endpoint, a running service, a public interface), the Test Engineer probes the surface before the tier is accepted. Sensible for live-surface work, but unvalidated as a mandatory step. If used, a failing smoke probe should block the tier.

---

## Reconciliation Matrix

The reconciliation matrix is the Orchestrator's final deliverable — the human-facing record of what the implementation actually did relative to what was asked.

One row per requirement from the original task brief (and from any advisory board findings that fed the task):

| Requirement | Status | Notes |
|-------------|--------|-------|
| Add `task_tags` join table | IMPLEMENTED | Migration 0012; model updated |
| Expose tags in task detail endpoint | IMPLEMENTED | Schema updated; endpoint verified |
| Display tags in TaskCard | IMPLEMENTED | Frontend Engineer — keyboard accessible |
| Bulk-tag endpoint | DEFERRED | Out of scope for this tier; separate task filed |

**Status values:**
- **IMPLEMENTED** — delivered in full, tested, reviewed.
- **PARTIAL** — delivered with a known gap; the gap is documented.
- **DEFERRED** — consciously moved out of scope; a follow-up is filed.
- **SCOPE CREEP** — the change was made but was not in the original brief; flagged for human awareness.

The matrix is the primary artifact the human reviewer uses to decide whether to approve the commit. It closes the loop between "what we said we would do" and "what we actually did."
