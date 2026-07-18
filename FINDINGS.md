# Findings — What Actually Works, and What We Were Wrong About

> This repository began as a bet that elaborate multi-agent orchestration — richly-drawn personas, a battery of mandatory gates, a multi-tier org chart — was the source of value. We then did something most agent frameworks don't: **we tested our own assumptions.** Most of them did not survive. This document is the honest record of what did.

The short version: **the load-bearing ideas are a small, dull core. The impressive-looking ceremony around them is, at best, unproven — and one prominent piece of it was measured and found to do nothing.** We'd rather ship the truth than the story we set out to tell.

---

## The hypothesis we started with

That a capable multi-agent system needs:

1. A **Change Dependency Graph** to sequence parallel work.
2. **Role-scoped subagents** to isolate context.
3. Rich **persona backstories** — a security engineer "who never recovered from watching SQL injection" — on the theory that *identity drives behavior more reliably than rules*.
4. A **battery of mandatory gates** — a code-review pass, a hygiene sweep after every tier, a keyword-triggered security review, a smoke gate, a documentation-sync gate.
5. A **director/orchestrator hierarchy** and finely-differentiated specialist roles.

We believed (1)–(5) were a package, and that the back half was the "secret sauce."

---

## What we tested

Two controlled experiments, on real code, scored by deterministic oracles — written up in full under [`examples/eval/`](examples/eval/):

- **Is the CDG load-bearing?** ([examples/eval/README.md](examples/eval/README.md)) A three-arm test — monolith vs. naive-parallel vs. dependency-ordered — on a real typed codebase, scored by `mypy`.
- **Does the persona backstory help?** ([examples/eval/persona-backstory.md](examples/eval/persona-backstory.md)) A placebo-controlled ablation — naked role vs. checklist vs. full backstory vs. an equal-length *irrelevant* backstory — scored on planted-bug detection.

---

## What we found

**Three categories. The distinction matters, because flattening "untested" into "disproven" would be its own dishonesty.**

### ✅ Validated — kept

- **The Change Dependency Graph.** Dependency-ordered state-forwarding was the *entire* difference between **0/3 and 3/3** on integration correctness. When parallel agents are given each other's *finalized* output instead of guessing it, they stop breaking each other. This is the one idea here with controlled evidence behind it.
- **Context isolation via subagents.** Not an A/B, but directly measured: the run that built this repo quarantined **~1.19M tokens** of processing inside subagent windows while the coordinator stayed lean enough never to compact ([examples/real-run/](examples/real-run/)). This is just *using subagents as designed* — real, but not a novel contribution.

### ❌ Invalidated — measured, and it did nothing

- **Persona backstories.** Across two fixtures and a placebo-controlled four-arm matrix, a security reviewer's elaborate red-team backstory caught **no more bugs** than a bare "you are a security reviewer." A *performance-engineer* backstory did just as well on *security* bugs — so it isn't even a "more text" effect. The backstory improved neither recall nor precision. The repo's own founding claim that "identity drives behavior more reliably than rules" **did not survive contact with a measurement**, on the agent that should have shown it best.
- **"More is better" on small tasks.** In the CDG eval the plain monolith was both the *cheapest* and *fully correct*. Coordination machinery only pays once a task outgrows a single context window.

### ❔ Unfounded — never validated, so demoted (not "disproven")

- The **mandatory-gate battery** (review pass, per-tier hygiene sweep, keyword-triggered security review, smoke gate, doc-sync gate), the **director/orchestrator hierarchy**, and **finely-differentiated specialist roles**. We never ran a controlled test on any of these. They are *asserted*, not *evidenced* — so we keep none of them as a default. They remain available as optional knobs; they are not part of the recommended core.

One corollary worth its own line, and the only thing we'd add to the core that isn't strictly "subagents-as-designed": **the guardrail that earns its place is a deterministic check, not an LLM gate.** In the persona eval, *every* arm — backstory or not — emitted the *same hallucinated false positive*, while the deterministic `mypy` oracle is what actually caught the real integration break. A reviewer *persona* is theater; a typecheck/test/build is a fact.

---

## What actually works — the recommended core

Strip everything that didn't earn its keep and you're left with something small and unglamorous:

> **CDG + subagents + one deterministic check — and a single agent until the task outgrows one window.**

1. **Sequence the work** (CDG): map what depends on what; finalize an upstream change before the downstream agent starts; hand the downstream agent the *real* finalized state, never a guess.
2. **Isolate context** (subagents): let each specialist explore in its own window and return a short report, so the coordinator stays lean enough to run a large task without compaction.
3. **Verify deterministically** (one check): gate the integrated result with a typecheck, test suite, or build — something with an exit code, not an opinion.
4. **Don't pay for coordination you don't need:** below the size where context isolation matters, one capable agent is cheaper and just as correct.

Everything else in this repo — the personas, the gate battery, the hierarchy — is **legible scaffolding, kept as optional flavor.** Personas in particular are worth writing for *consistency and predictability* (you can reason about what each role will focus on), but **not** because the backstory makes the agent better. It doesn't; we checked.

---

## We were wrong, and that's the result

The honest headline is that the maintainer's initial assumption — that the orchestration ceremony and the rich identities were the value — **was wrong, and our own tests disproved it.** What the tests handed back is more useful than the assumption: a minimal, defensible system, and a clear line between what's earned and what's decoration.

We're documenting it this way on purpose. An agent framework that asserts its own cleverness is common. One that **measures its own claims and publishes the parts that failed** is the thing actually worth trusting.

---

## Honest limits

The evals are pilots, not a paper: small N, a single model tier (Sonnet), single fixtures, and a ceiling effect on the persona ablation (the naked baseline was so capable we could not build a security-review task hard enough to separate the arms — which is itself evidence the backstory has no room to help). The CDG result is the most robust; the "deterministic check beats LLM gate" point is evidence-informed design, not a separately-run A/B. Read [`examples/eval/`](examples/eval/) for the full methodology, the caveats, and the things that went sideways along the way.

---

# Round 2 — the skill arena (2026-07)

Round 1 validated the core on tasks that fit one window. The open questions were about scale: does the loop ever *actually* route work to a swarm, and does routing ever pay? We built a benchmark to find out — three purpose-built mixed-difficulty fixtures (a 22-node service build, an 18-node static site, a 68-site migration sweep laced with anti-regex traps), each with a held-out graded oracle, and ran six generations of the skill head-to-head with spawn accounting taken from the event stream, not from self-report. Full tables, charts, and every generation's text: **[boord-its.com/skills](https://boord-its.com/skills)**.

### ✅ Validated — now in the live skill

- **The crossover is real, and computable.** Below it, a single strong session beats every orchestration scheme (routing there cost +86–104% for zero correctness gain). Above it — the 68-site sweep — the single session *dies on the mundane work* 2 runs in 3, and a routed swarm posts the cheapest passing runs on record. v4.1 gates on **counted sites/files/read-volume**, and the same skill correctly chose solo on one fixture (beating the monolith at its own game) and swarm on another.
- **Turn economy is the wall-regime prize.** At the wall the routed orchestrator finishes in ~33 of its own turns where the unrouted generation ground through 112–167. Turns — not context — were the budget that actually killed sessions.
- **Lanes with a demotion rule.** Mechanical work rides the cheapest model *when its card carries the byte-exact rules and traps*; spec-pinned critical nodes may drop one lane; auth/money/concurrency never do. Measured haiku-lane runs came back clean where earlier free-form routing had quietly upgraded everything to the mid tier.
- **Telemetry over intentions.** v4.0's own streams caught it dispatching all ten workers serially (strict use→result→use) despite a parallel-dispatch rule, erasing its cheap lane by grouping across lanes, and flipping solo/swarm on a 9-vs-10 count at 2.8× cost. All three became v4.1 fixes, re-measured. The habit of instrumenting your own skill is worth more than any single rule in it.

### ❌ Invalidated — measured, and it failed

- **Skill text alone produces routing.** Across 28 unforced benchmark runs, the earlier generations produced *textbook routing plans when asked to plan* — then did all the work themselves in real runs, every time (the **knowing-doing gap**). Two things closed it: making the route/no-route decision a computed gate with a printed verdict, and writing the plan as a data file the reconciliation is checked against. (A hard prose mandate also closed it — at the cost of routing where routing loses.)
- **Per-requirement spawning.** One worker per graded requirement drowned the savings in briefing overhead. Workers own cohesive file-clusters, grouped *within* a lane.
- **Node-count gating.** The fixture with *fewer* nodes was the one at the wall (16 nodes, 68 edit sites). Gate on the work, not the outline.
- **Heavyweight apparatus, again.** A rebuilt suite with worktree isolation, intake scripts, and manifests benchmarked no better than the lean loop — its machinery never activated in a real run. Same lesson as Round 1's gate battery, at larger scale.

### Honest limits, Round 2

Small k (1–3 per cell); one stack (Claude Code, headless, one orchestrator model at one effort setting); costs are API-equivalent dollars; the supervised interactive path (human approves the plan mid-run) was exercised anecdotally, not benchmarked. The prior generations live in [`archive/`](archive/) with their retirement reasons — the failures are the transferable part.

---

# Round 3 — orchestrator effort & the worker floor (2026-07)

Round 2 fixed *when to route* and *what lane gets the work*. Round 3 asked the two questions that were left: how hard does the **orchestrator** actually need to think, and how weak can a **worker** be before a good brief stops carrying it? Same method — held-out oracles, spawn accounting from the event stream — plus a new instrument: real worker briefs lifted verbatim from validated swarm runs and replayed standalone at chosen model × effort cells, graded on exactly the sites and traps each brief owns. 26/26 runs in the round passed. Numbers and charts: **[boord-its.com/skills](https://boord-its.com/skills)**.

### ✅ Validated — now in the live guidance

- **The orchestrator doesn't need max effort.** The identical skill text with the orchestrator's reasoning effort one notch down passed every run, cut the planning-heavy fixture **44%**, and set a new cheapest-passing record on the 68-site sweep. Once the route decision is computed and the gate is a script, maximum thinking depth was paying for decisions the skill had already made deterministic. The live skill now says so: run the orchestrator at high, not max.
- **The worker floor is lower than the lane table assumes.** All 18 standalone cells passed — including the cheapest model at *minimum* effort through a fully-specified mechanical sweep, and the cheapest model through a trap-dense cluster at **a third of the mid-tier price** with every must-not-change trap intact. With a brief that names the rules and the traps, worker tier became a speed dial, not a correctness dial. The brief *is* the orchestrator's judgment, exported — which is why the top of the system is the part worth paying for.
- **A bigger model at low effort beats a smaller one at max.** On a spec-pinned critical brief, the top-tier worker at minimum effort tied the mid-tier at maximum effort on correctness — and beat it on wall-clock (roughly half) and cost, because it needs fewer passes. Where the demotion rule allows a choice, prefer big-model/low-effort over small-model/max-effort.
- **A ceiling, not just a floor.** At lower orchestrator effort, routing drifted upward run-to-run (mundane work quietly landing on the mid tier). The deterministic gate kept every run correct — that is what it is for — and a new enforcement hook makes the drift deny-by-default: a worker's first spawn above its planned lane is refused unless the plan names the trap that justifies the promotion. The hooks (mandate + floor + ceiling, 18 tests) are now in [`hooks/`](hooks/).

### 🅿️ Parked — mechanically proven, economically beaten (decisive cell run)

- **Dispatch-as-code.** Writing each batch as one workflow script — so serial dispatch is structurally impossible and every worker gets an explicit effort — worked exactly as designed: correct on every run, zero scope violations, orchestrator turns collapsed. It was first parked on max-effort rows with a flagged confound, so we paid for the clean cell: **same scripted design, effort cut to match the champion config. Still 100% correct — and still 21–48% pricier** than the lean skill at high effort. The stream forensics name the cause precisely: each batch re-transmits the whole brief set inside the workflow call (string-encoded, escaping bloat included), so the orchestrator pays per *batch* what the plain dispatch pays once per *worker*. Structural, not thinking depth. The parked verdict now rests on single-variable evidence; the recommended config remains the lean skill at high effort. If you want scripted dispatch anyway for its properties (structural parallelism, per-worker effort, a journal of actual spawns), the countermeasures are: pass args as a real object, send each batch only its own workers' briefs, and keep batch count to the minimum the dependencies force.

### Honest limits, Round 3

k=2 everywhere; one brief per task shape; and a deliberate ceiling effect on the floor probe — nothing failed, so we know the floor sits *below* everything tested, not where it is. Locating it needs deliberately degraded briefs, which is the next controlled test worth running: it would cleanly separate brief quality from model strength, the two things this round showed are usually conflated.
