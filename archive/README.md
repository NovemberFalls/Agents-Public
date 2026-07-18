# Archive — the generations ledger

Every retired generation of the `/orchestrate` skill, preserved verbatim and honestly
labeled. Nothing here is recommended for use — the live skill is
[`.claude/commands/orchestrate.md`](../.claude/commands/orchestrate.md) — but each
generation taught us something measurable, and deleting the evidence would be the
kind of tidiness this repo exists to resist.

Benchmarks for every generation: **[boord-its.com/skills](https://boord-its.com/skills)** —
eight arms across three rounds, purpose-built fixtures, held-out graded oracles,
spawn accounting from the event stream.

| generation | file | verdict |
|---|---|---|
| **v0 — the lean classic** | [orchestrate-v0.md](orchestrate-v0.md) | The validated core (CDG + context isolation + one deterministic check + lightweight default). Passed everything below the scale wall on discipline alone — and never once actually routed work (0 spawns across every benchmark run: the *knowing-doing gap*). Retired 2026-07-17. |
| **v0.5 — the routed mandate** | [orchestrate-v0.5-routed-mandate.md](orchestrate-v0.5-routed-mandate.md) | v0 plus a hard routing mandate written against the model's own confessed excuses. The first arm that routed for real — proving forced routing wins at scale (cheapest passing runs on the 68-site sweep) and *loses* below it (+86–104% cost on small mixed builds). Never installed live; its lesson became v4's computed gate. |
| **the "new suite"** | *(not preserved here)* | A heavyweight rebuild — worktree isolation, intake scripts, manifests, candidate commits. Benchmarked and rejected: its apparatus never activated in a real run and it cost more where it shouldn't. The lesson (*apparatus you can't measure activating is dead weight*) survives; the four files don't need to. |
| **v4.0** | *(delta only)* | The first computed-gate/plan-as-data generation. Superseded within a day by v4.1 after its own telemetry caught three defects: it dispatched all 10 workers serially despite a parallel-dispatch rule, silently folded cheap-lane work into mid-lane workers, and flipped SOLO/SWARM on a 9-vs-10 count at 2.8× cost. v4.1 = v4.0 + those four fixes; the live file *is* the v4.0 lineage, so only the delta is recorded. |
| **v4.2 — scripted dispatch** | *(parked, never installed)* | Dispatch-as-code: each batch one workflow script, so serial spawning is structurally impossible and every worker gets an explicit reasoning effort. Round 3 proved it mechanically (4/4 correct, zero scope violations) and priced it out at max orchestrator effort (~2× wall, costlier than simply lowering the orchestrator's effort). Waits for its decisive cell rather than a burial — parked is not retired. |

## Why keep a museum

Because the failures are the transferable part. Anyone can publish their current
best skill; the sequence — *what we believed, what we measured, what died* — is what
lets someone else skip the same year of mistakes. Round 1 of that story is
[FINDINGS.md](../FINDINGS.md); Round 2 (the arena) is appended there.
