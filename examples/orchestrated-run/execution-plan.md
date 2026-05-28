# Execution Plan — Verdant / User Tagging (Fictional Example)

> Fictional example for illustration — not a real project.

**Date:** (illustrative)
**Requested by:** `/orchestrate`
**Task brief reference:** [`task-brief.md`](task-brief.md)
**Orchestrator:** Reviewing and signing

---

## Scope Summary

**In scope:** `task_tags` join table + migration; `Task.tags` relationship; `tags` field on the task response schema; two new route handlers + extended detail handler; frontend API client function + `TaskCard` rendering.
**Out of scope:** tag autocomplete, colors, global tag management, bulk tagging (per brief).
**Requirements addressed:** 4 of 4 from the brief's "Done looks like".

---

## Change Inventory

| # | Change | Files Touched | Brief Requirement | Priority |
|---|--------|--------------|-------------------|----------|
| 1 | New join table + reversible migration | `db/migrations/0012_task_tags.sql` | join table | P0 |
| 2 | `Task.tags` relationship | `db/models/task.py` | model relationship | P0 |
| 3 | `tags` field on response schema | `api/schemas/task.py` | `GET /tasks/{id}` returns tags | P0 |
| 4 | Add/remove endpoints + extended detail | `api/routes/tasks.py` | two endpoints + detail | P0 |
| 5 | API-client function | `frontend/api/tasks.ts` | client for new endpoints | P1 |
| 6 | Tag chips on the card | `frontend/components/TaskCard.tsx` | render tags, hide if empty | P1 |

---

## Change Dependency Graph

```
0012_task_tags.sql      ──independent (nothing exists yet to depend on)
db/models/task.py        ←depends on── 0012_task_tags.sql   (model maps the new table)
api/schemas/task.py      ←depends on── 0012_task_tags.sql   (tags field mirrors the column)
api/routes/tasks.py      ←depends on── db/models/task.py, api/schemas/task.py
frontend/api/tasks.ts    ←depends on── api/schemas/task.py  (consumes the response contract)
frontend/components/TaskCard.tsx ←depends on── frontend/api/tasks.ts
```

Dependencies of note:
- Everything depends on the schema existing → the migration is the sole root and must finalize first.
- `api/routes/tasks.py` and `frontend/api/tasks.ts` both depend on the **finalized response contract** but not on each other → parallelizable once the schema is fixed.
- `TaskCard.tsx` depends on the API client's shape → it waits one tier.

---

## Execution Tiers

### Tier 1 — single task (root of the graph)

| Specialist | Task | Files | Model | Rationale |
|-----------|------|-------|-------|-----------|
| Database Engineer | Write reversible migration for `task_tags` | `db/migrations/0012_task_tags.sql` | **Opus** | Migration = irreversible failure mode; escalated per roster |

*Code Reviewer reviews after: Database Engineer (Opus output).*

### Tier 2 — parallel (requires Tier 1 finalized)

*Integration context passed from Tier 1: the final `task_tags` schema (columns, composite unique constraint).*

| Specialist | Task | Files | Model | Rationale |
|-----------|------|-------|-------|-----------|
| Database Engineer | `Task.tags` relationship | `db/models/task.py` | Sonnet | File-scoped, standard ORM mapping |
| Backend Engineer | `tags` field on response schema | `api/schemas/task.py` | Sonnet | File-scoped, well-defined contract |

### Tier 3 — parallel (requires Tier 2 finalized)

*Integration context passed: finalized `Task` model + finalized response schema (the `tags: string[]` contract).*

| Specialist | Task | Files | Model | Rationale |
|-----------|------|-------|-------|-----------|
| Backend Engineer | Add/remove endpoints + extend detail handler | `api/routes/tasks.py` | Sonnet | Uses finalized model + schema |
| Frontend Engineer | API-client function | `frontend/api/tasks.ts` | Sonnet | Consumes finalized response contract |

### Tier 4 — single task (requires Tier 3 finalized)

*Integration context passed: the finalized API-client function signature.*

| Specialist | Task | Files | Model | Rationale |
|-----------|------|-------|-------|-----------|
| Frontend Engineer | Render tag chips; hide when empty | `frontend/components/TaskCard.tsx` | Sonnet | Consumes the client shape |

### Final Tier — Testing

| Specialist | Task | Coverage |
|-----------|------|---------|
| Test Engineer | Tests for all changes | migration up/down; uniqueness constraint; add/remove endpoints incl. 422 on empty/oversized tag; detail returns tags; card renders chips and hides when empty |

---

## File Ownership Matrix

*No file appears in more than one tier.*

| File | T1 | T2 | T3 | T4 |
|------|----|----|----|----|
| `db/migrations/0012_task_tags.sql` | Database Engineer | — | — | — |
| `db/models/task.py` | — | Database Engineer | — | — |
| `api/schemas/task.py` | — | Backend Engineer | — | — |
| `api/routes/tasks.py` | — | — | Backend Engineer | — |
| `frontend/api/tasks.ts` | — | — | Frontend Engineer | — |
| `frontend/components/TaskCard.tsx` | — | — | — | Frontend Engineer |

**Conflicts detected:** none.

---

## Keyword Scan (auto-invocation)

- `migration` / `schema change` → **Database Engineer + Test Engineer** auto-included (both already in the plan).
- No `auth` / `session` / `token` / `secret` triggers → **Security Engineer not invoked** (brief explicitly forbids new auth surface; the Code Reviewer will flag if that changes).

---

## Risk Assessment

| Risk | Likelihood | Mitigation |
|------|-----------|-----------|
| Migration not cleanly reversible | M | Opus tier + Code Reviewer gate; Test Engineer runs up→down→up |
| Duplicate tag on a task | M | Composite unique constraint at the DB layer, not just app logic |
| Empty/oversized tags accepted | M | `422` validation in the route; negative tests required |

---

## Human Approval Gate

- [x] **Irreversible change (database migration)** → this plan **requires human approval before Tier 1 begins**.

**The Orchestrator's assessment:** pause for human approval (migration present). *Approved by maintainer; proceeding.*
