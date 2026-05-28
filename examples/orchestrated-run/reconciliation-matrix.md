# Reconciliation Matrix — Verdant / User Tagging (Fictional Example)

> Fictional example for illustration — not a real project.

**Scope:** Add user tagging to tasks (join table, endpoints, schema, frontend).
**Source:** [`task-brief.md`](task-brief.md) (direct task brief — no prior board audit, so no Readiness Score delta).
**Signed off by:** Orchestrator

---

## Reconciliation Matrix

### Implemented ✅

| # | Brief Requirement | Specialist | Tier | Implementation | File:Line | Verified By |
|---|-------------------|-----------|------|----------------|-----------|-------------|
| 1 | `task_tags` join table, unique per task, reversible | Database Engineer | T1 | Composite-PK table + `down` migration | `db/migrations/0012_task_tags.sql:1–24` | Code Reviewer (APPROVED) |
| 2 | `Task.tags` relationship | Database Engineer | T2 | Relationship returning plain strings | `db/models/task.py` | Orchestrator |
| 3 | `GET /tasks/{id}` returns `tags: string[]` | Backend Engineer | T2/T3 | `tags` field on `TaskRead`; detail handler populates it | `api/schemas/task.py`, `api/routes/tasks.py:88–96` | Test Engineer (detail test green) |
| 4 | `POST /tasks/{id}/tags` + `DELETE /tasks/{id}/tags/{tag}` | Backend Engineer | T3 | Endpoints with trim + 1–32 char validation → `422` | `api/routes/tasks.py:140–171` | Test Engineer (incl. negative cases) |
| 5 | Frontend API client for the new endpoints | Frontend Engineer | T3 | `addTag` / `removeTag` returning the sorted set | `frontend/api/tasks.ts` | Orchestrator |
| 6 | `TaskCard` renders chips; hides when empty | Frontend Engineer | T4 | Maps tags → chips; returns `null` for empty list | `frontend/components/TaskCard.tsx` | Test Engineer (render + empty test) |

### Partially Implemented ⚠️
None.

### Deferred ❌

| # | Item | Priority | Reason | Follow-up filed |
|---|------|----------|--------|-----------------|
| 1 | Tag autocomplete, colors, global tag management, bulk tagging | P2 | Explicitly out of scope per brief | yes (separate task) |

### Scope Creep 🔍
None — every change traces to a brief requirement. The idempotent-add behavior (re-adding a tag returns `201`, not `500`) is an implementation decision within Requirement 4, not new scope; recorded in the Backend Engineer's report.

---

## Files Changed

| File | Change | Lines Δ | Specialist | Tier |
|------|--------|---------|-----------|------|
| `db/migrations/0012_task_tags.sql` | add | +24 | Database Engineer | 1 |
| `db/models/task.py` | modify | +6 | Database Engineer | 2 |
| `api/schemas/task.py` | modify | +3 | Backend Engineer | 2 |
| `api/routes/tasks.py` | modify | +34 | Backend Engineer | 3 |
| `frontend/api/tasks.ts` | modify | +18 | Frontend Engineer | 3 |
| `frontend/components/TaskCard.tsx` | modify | +12 | Frontend Engineer | 4 |

**Total files modified:** 6 (+ 2 test files). **Net lines changed:** ~+97 source, ~+85 tests.

---

## Tests Written / Modified

| File | Tests Added | Covers |
|------|------------|--------|
| `tests/test_tags.py` | 8 | up→down→up; uniqueness; cascade; add/remove; 422 on empty + 33-char; 404 on missing task; idempotent add |
| `frontend/components/TaskCard.test.tsx` | 3 | renders chips; hides container when empty; chip count matches tag count |

**Test suite status:** all passing (illustrative).

---

## Hygiene (Hygiene Auditor)

Per-tier sweeps + final cross-tier sweep: CLEAN. No dead code, no unused imports introduced; the new `TagIn` schema and `addTag`/`removeTag` client functions are all referenced.

## Smoke / Verification

N/A for this example — Verdant is fictional, nothing is deployed. In a real run the migration tier (data-layer) would trigger the migration up/down drill before acceptance.

---

## Human Reviewer Checklist

- [ ] **Migration** — run `up`/`down`/`up` against a scratch DB; confirm clean.
- [ ] **422 paths** — `curl` an empty tag and a 33-char tag; confirm rejection.
- [ ] **No auth surface** — confirm the new endpoints reuse `get_task_or_404` and add no new permission path.
- [ ] **Deferred items** — comfortable that autocomplete/colors/bulk are out of scope?
- [ ] **Test suite** — `pytest tests/test_tags.py` and the frontend test green.

---

## Orchestrator Sign-Off

**Implementation complete:** yes.
**Quality assessment:** Clean run. The one design judgment (idempotent add over surfacing the DB uniqueness error) is recorded and defensible. The extra query on the detail handler is noted as a future optimization, not a blocker.
**Recommended next run:** the deferred tag-management features, if prioritized — they would warrant their own `/orchestrate` run (new endpoints + a management UI = multi-tier).
