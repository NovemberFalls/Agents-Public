# Worked Orchestration Run — Verdant (Fictional Example)

> Fictional example for illustration — not a real project, company, or person.

---

This directory shows the full orchestration loop applied to one concrete task, end to end: a task brief in, a reviewed-and-reconciled change set out. It is the runnable companion to the conceptual walkthrough in [`docs/architecture.md`](../../docs/architecture.md), which uses the same task.

**Verdant** is an imaginary open-source task-management API (Python/FastAPI backend, a small React frontend). It has no affiliation with any real product. The task:

> **Add user tagging to tasks.** Tags are stored in a new `task_tags` join table. The REST API gains two endpoints and the task-detail endpoint returns tags. The frontend task card displays them.

## What this example demonstrates

1. How the **Orchestrator** turns a brief into a Change Dependency Graph and execution tiers ([`execution-plan.md`](execution-plan.md)).
2. What a **specialist report** and a **Code Reviewer gate** actually look like for real changes ([`tier-reports.md`](tier-reports.md)).
3. How every requirement is closed out in a **reconciliation matrix** ([`reconciliation-matrix.md`](reconciliation-matrix.md)).
4. **Where the tokens go** — and the metric that actually proves the architecture pays for itself ([`context-ledger.md`](context-ledger.md)).

## Honest methodology note — read this before the ledger

Verdant is fictional, so there is **no real codebase to meter**. The numbers in `context-ledger.md` are a **transparent model**, not the output of an instrumented run: every figure is derived from a stated assumption about file size and what each agent reads, and the arithmetic is shown so you can check or replace it. They are labeled *illustrative* throughout.

This matters because the easy version of this artifact — quoting precise token counts as if measured — would be the exact dishonesty the repo argues against. The ledger instead does two things a cherry-picked demo would not:

- It headlines **peak context**, not total tokens. Peak context is the robust, scalable win; **total spend is workload-dependent** (orchestration adds gate and re-read overhead, but avoids re-billing a monolith's ever-growing window each turn). So the ledger refuses to claim a total-token win — and shows the components honestly either way.
- It includes a **"when it loses"** case (a one-file change) where the lightweight path wins, because a model you can only ever win with is not a model.

`context-ledger.md` ends with **"How to reproduce with real numbers"** so you can run the same comparison on an actual repo and get metered figures.

## Files in this directory

| File | Contents |
|------|----------|
| `README.md` | This file |
| `task-brief.md` | The input: the Verdant tagging task as handed to the Orchestrator |
| `execution-plan.md` | The Orchestrator's CDG, tiers, and file-ownership matrix |
| `tier-reports.md` | Two specialist reports + the Code Reviewer gate on the Opus tier |
| `reconciliation-matrix.md` | Every requirement → IMPLEMENTED / PARTIAL / DEFERRED |
| `context-ledger.md` | The token/context model — the point of the example |

## How to read it

Read in file order for the narrative (brief → plan → reports → matrix), or skip straight to `context-ledger.md` if you only care about the token argument. The personas, report-block labels (`[CODE REVIEW]`), and matrix format here match the live templates in [`orchestration-team/templates/`](../../orchestration-team/templates/) — this example doubles as a calibration target for what those artifacts should contain.
