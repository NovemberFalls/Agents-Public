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
| **the heavyweight suite** | [orchestrate-heavyweight-suite.md](orchestrate-heavyweight-suite.md) | A heavyweight rebuild — worktree isolation, intake scripts, manifests, candidate commits (four files, concatenated). Benchmarked and rejected: its apparatus never activated in a real run and it cost more where it shouldn't. The lesson: *apparatus you can't measure activating is dead weight.* |
| **v4.0** | [orchestrate-v4.0.md](orchestrate-v4.0.md) | The first computed-gate/plan-as-data generation. Superseded within a day by v4.1 after its own telemetry caught three defects: it dispatched all 10 workers serially despite a parallel-dispatch rule, silently folded cheap-lane work into mid-lane workers, and flipped its go/no-go on a 9-vs-10 count at 2.8× cost. |
| **v4.2 — scripted dispatch** | [orchestrate-v4.2-scripted-dispatch.md](orchestrate-v4.2-scripted-dispatch.md) | Dispatch-as-code: each batch one workflow script, so serial spawning is structurally impossible and every worker gets an explicit reasoning effort. Mechanically proven at both efforts tested (100% correct, zero scope violations) and 21–48% pricier at equal correctness — the script re-transmits the whole brief set per batch. Parked on single-variable evidence. |
| **v4.3 — counting gate** | [orchestrate-v4.3-counting-gate.md](orchestrate-v4.3-counting-gate.md) | The champion plus a mandatory count-every-edit-point gate. 100% correct; free on migration-shaped work, a +33% tax on greenfield builds, protecting against a failure that only appears below the shipped effort. The champion's fourth surviving challenge. |

## Why keep a museum

Because the failures are the transferable part. Anyone can publish their current
best skill; the sequence — *what we believed, what we measured, what died* — is what
lets someone else skip the same year of mistakes. Round 1 of that story is
[FINDINGS.md](../FINDINGS.md); Round 2 (the arena) is appended there.
