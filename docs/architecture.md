# Architecture

This document explains the core coordination model used by the orchestration team: the Change Dependency Graph, execution tiers, mandatory gates, and the reconciliation matrix.

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

## Mandatory Gates

Four gate types are mandatory regardless of tier size or perceived simplicity.

### 1. Keyword scan (auto-invocation)

Before any tier executes, the orchestrator scans the tier's planned changes against this table:

| Keyword / pattern | Auto-invoked agent | Reason |
|---|---|---|
| auth, session, JWT, token, password, credential, secret, API key | Security Engineer | Authentication and secrets surface requires security review |
| migration, schema change, ALTER TABLE, DROP COLUMN, INDEX | Database Engineer + Test Engineer | Schema changes have irreversible failure modes |
| deploy, publish, release, live endpoint, public surface | Test Engineer — smoke gate | Changes reaching a live surface need verification before full rollout |

Specialists do not self-gate. The orchestrator is solely responsible for running the keyword scan and adding the appropriate agents. A specialist who touches auth logic does not decide for themselves whether the Security Engineer is needed.

### 2. Code hygiene sweep (Hygiene Auditor)

The Hygiene Auditor runs after every tier, including lightweight single-file tiers. No exceptions. The Hygiene Auditor identifies dead code, unused imports, orphaned files, and stale exports introduced or exposed by the tier's changes. Its hygiene report is included in the integration snapshot passed to the next tier.

The final cross-tier hygiene sweep runs after all specialist tiers complete, before the reconciliation matrix is produced.

### 3. Code Reviewer gate

The Code Reviewer reviews all output from Opus-model specialists before that output reaches the Orchestrator. The Code Reviewer can approve or return work for revision. A Code Reviewer-approved review does not block the Orchestrator's own review — the Orchestrator reviews all output — but the Code Reviewer catches structural and integration issues at the specialist level before they compound.

### 4. Smoke / verification gate

Any tier that touches a live surface (a deployed endpoint, a running service, a public interface) triggers a smoke gate: the Test Engineer probes the live surface to verify behavior before the tier is accepted. A failing smoke gate blocks the tier regardless of code-review outcome. The tier does not advance until the Test Engineer confirms the live surface behaves as expected.

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
