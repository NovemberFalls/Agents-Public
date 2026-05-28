# Task Brief — Verdant / User Tagging (Fictional Example)

> Fictional example for illustration — not a real project.

This is the input handed to the Orchestrator (e.g., via `/orchestrate`). It is what a maintainer would actually write.

---

## Goal

Let users attach freeform tags to tasks, and show those tags on the task card.

## Done looks like

- A task can have zero or more tags. Tags are short strings, unique per task (no duplicate tag on the same task).
- `POST /tasks/{id}/tags` adds a tag to a task; `DELETE /tasks/{id}/tags/{tag}` removes one.
- `GET /tasks/{id}` includes a `tags: string[]` field in its response.
- The frontend `TaskCard` renders the tags as chips; an empty tag list renders nothing (no empty container).

## Known shape of the change

- New join table `task_tags(task_id, tag)` with a composite uniqueness constraint.
- The `Task` model gains a `tags` relationship.
- The task response schema gains a `tags` field.
- Two new route handlers; the existing detail handler is extended.
- One new API-client function on the frontend; the `TaskCard` component consumes it.

## Constraints

- No change to authentication or task ownership rules — tagging is available to any user who can already see the task. (Do not add new auth surface.)
- Tag strings are capped at 32 characters and trimmed; reject empty/whitespace-only tags with `422`.
- The migration must be reversible.

## Out of scope (explicitly)

- Tag autocomplete, tag colors, global tag management, or bulk tagging. File follow-ups if valuable; do not build them here.

## Pointers

- Migrations live in `db/migrations/`, numbered sequentially (latest is `0011_*`).
- The task model is `db/models/task.py`; response schemas are `api/schemas/task.py`; routes are `api/routes/tasks.py`.
- Frontend: API client `frontend/api/tasks.ts`, card component `frontend/components/TaskCard.tsx`.
