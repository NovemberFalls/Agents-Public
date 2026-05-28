# Context Ledger — Verdant / User Tagging (Fictional Example)

> Fictional example for illustration. **Every number below is a transparent model, not a metered run** — see "Model assumptions" and "How to reproduce with real numbers." Figures are labeled *illustrative*; the arithmetic is shown so you can replace it.

This is the point of the whole example: showing *where the tokens go* when you run a task through specialists instead of one agent, and which number actually justifies the architecture.

---

## The claim, stated honestly

**Robust win — peak context.** Orchestration keeps any single context window small. The coordinating window never absorbs the specialists' file reading; it holds the plan and short reports. On this 6-file task the coordinator peaks ~3.6× smaller than a monolith, and the gap *widens* with task size.

**Not a free lunch — total spend.** Orchestration adds real cost: shared files get re-read across specialist windows, plus a Code Reviewer pass and hygiene sweeps. It also *avoids* a cost (a long single agent re-sends its ever-growing window on every turn, and pays for compaction-driven rework). Which dominates is **workload-dependent** — roughly a wash-to-modestly-higher here, clearly higher for trivial tasks. So total spend is **not** the number to optimize, and we don't claim a win on it. Peak context is.

---

## Model assumptions (illustrative token sizes)

| Artifact | ~tokens | | Fixed cost | ~tokens |
|---|---:|---|---|---:|
| `db/migrations/0011_*.sql` (read for convention) | 400 | | task brief | 300 |
| `db/migrations/0012_task_tags.sql` (new) | 250 | | a specialist's own reasoning+output | 600 |
| `db/models/task.py` | 1,400 | | the short report the Orchestrator keeps | 200 |
| `api/schemas/task.py` | 800 | | CDG + tier plan the Orchestrator holds | 500 |
| `api/routes/tasks.py` | 2,200 | | a Code Review pass (own window) | 1,400 |
| `frontend/api/tasks.ts` | 1,100 | | a hygiene sweep (own window) | 700 |
| `frontend/components/TaskCard.tsx` | 1,500 | | reconciliation matrix the Orchestrator holds | 400 |

Total unique file content ≈ **7,650 tokens**. Hold that number — it's what one window would accumulate.

---

## Peak context — per window

Each specialist runs in its **own** window. None of these coexist; each is created, does its work, returns a ~200-token report, and is discarded.

| Step | Specialist | Reads (illustrative) | **Window peak** | Returns to coordinator |
|------|-----------|----------------------|----------------:|------------------------|
| T1 | Database Engineer | 0011 (400) + model (1,400) | **~2,700** | 200-tok report |
| T1 gate | Code Reviewer | DB report + migration diff | **~1,400** | 150-tok verdict |
| T2a | Database Engineer | migration (250) + model (1,400) | **~2,450** | 200 |
| T2b | Backend Engineer | migration (250) + schema (800) | **~1,750** | 200 |
| T3a | Backend Engineer | routes (2,200) + schema (800) + model (1,400) | **~5,400** | 200 |
| T3b | Frontend Engineer | client (1,100) + contract (400) | **~2,300** | 200 |
| T4 | Frontend Engineer | card (1,500) + client (1,100) | **~3,400** | 200 |
| T5 | Test Engineer | all changed files (~7,250) | **~8,350** | 200 |

**Largest single window:** the Test Engineer at ~8,350 — but it is transient and isolated; it exists only for that step and then vanishes.

## Peak context — the coordinator (persists across the run)

The Orchestrator's window only ever accumulates the plan and the short reports:

```
start:           brief 300 + CDG/plan 500                    =   800
+ T1:            + DB report 200 + review verdict 150         = 1,150
+ T2:            + 2 reports (200×2)                          = 1,550
+ T3:            + 2 reports (200×2)                          = 1,950
+ T4:            + 1 report 200                               = 2,150
+ T5:            + test report 200                            = 2,350
+ hygiene:       + per-tier summaries (~100 × 5)              = 2,850
+ reconcile:     + matrix 400                                 = 3,250
                                                    PEAK  ≈  ~3,250
```

The coordinator **never holds the 7,650 tokens of file content.** That content lived and died inside specialist windows.

## Versus a monolith (one window, nothing is ever shed)

A single agent doing all six changes reads each file as it goes and keeps everything. At the final step (writing tests) it is *still* carrying the migration it read first.

```
brief 300 + planning 500 + migration read/write 650
+ model 1,400 + schema 800 + routes 2,200 + client 1,100 + card 1,500
+ test authoring 800 + accumulated reasoning across ~12 turns ~2,500
                                                    PEAK  ≈ ~11,750
```

| Metric | Monolith | Orchestrated | |
|---|---:|---:|---|
| **Peak single-window context** | ~11,750 | **~3,250** (coordinator) | **~3.6× leaner** |
| Largest transient window | — | ~8,350 (isolated, Test) | |
| Where peak occurs | at the end, carrying everything | distributed, discarded each step | |

**Why this is the number that matters, and why the gap grows:**
- The monolith's peak ≈ the **sum of everything it touched**. The coordinator's peak ≈ the **sum of the reports**. Double the files and the monolith's peak roughly doubles; the coordinator's barely moves.
- Past the model's window limit the monolith triggers **compaction** — lossy summarization mid-task, the exact "stale context" failure this repo exists to prevent. The coordinator stays far below the limit.
- **Reasoning quality** degrades as a window fills with now-irrelevant detail. Each specialist reasons over only its slice; the coordinator reasons over summaries.

---

## Total spend (the honest, workload-dependent number)

We deliberately do **not** headline this. Components:

**Orchestration adds:**
- Re-reads of shared files across windows — e.g. `task.py` is read in T1, T2a, T3a, and T5 (4 × 1,400 ≈ 5,600 vs the monolith's single 1,400).
- An entire Code Reviewer window (~1,400) and a hygiene window per tier (~700 × 5).
- The coordinator window itself.

**Orchestration avoids:**
- Re-sending a single growing context **every turn**: a ~12-turn monolith re-bills an averaging ~6k-token window each turn — that re-billing is large and is exactly what isolation sidesteps.
- Compaction-driven re-exploration after the monolith blows its window.

**Net:** for a task this size, roughly a wash to modestly higher; **prompt caching** (cheap cached reads, a stable system prompt, a reused project brain) shifts it further toward orchestration. For a *trivial* task there is no isolation benefit to pay for — overhead simply loses (next section). Optimize for peak context and parallelism, not this number.

*(Parallelism, separately: T2 and T3 each run two specialists concurrently. That is a wall-clock win — "streamline development" — orthogonal to tokens.)*

---

## When orchestration LOSES — and the repo says so

**Task:** fix a typo'd field name in `api/schemas/task.py` (~800-token file). One file, no dependents.

| Approach | Work | ~tokens | Round-trips |
|---|---|---:|---|
| Inline / lightweight `/fix` | read 800 + edit + 200 | **~1,000** | 1 |
| Full `/orchestrate` | CDG+plan 900 + specialist window (read 800 + edit) 1,000 + hygiene 600 + reconcile 300 | **~2,800** | 3 |

The task already fits in one small window, so context isolation buys nothing — the coordination machinery is pure overhead, ~2.8× the cost and three times the round-trips. This is why the Orchestrator's **first question is "is this a one-tier job?"** and why [`/fix`](../../.claude/commands/fix.md) exists. A model you can only ever win with isn't a model.

---

## How to reproduce with real numbers

To replace the illustrative figures above with metered ones:

1. Pick a **real** repo and a **real** multi-file task.
2. Run it twice: once as a single agent (no subagents), once via `/orchestrate`.
3. From each run capture: **peak single-context size** (the max tokens in the coordinating/only window before any compaction) and **total input + output + cached tokens** across all calls. Claude Code reports token usage per session and per subagent.
4. Compare. Expected shape: a large **peak-context** win for orchestration that grows with task size; **total spend** a wash-to-higher on small tasks, improving as the task grows and as caching kicks in.

If your metered results differ from this shape, trust the meter over this model — and the interesting part is *why* they differ.
