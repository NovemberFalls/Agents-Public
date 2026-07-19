# One Skill to Run a Swarm

**Benchmarking AI orchestration for complex coding tasks — a working paper.**

> **Abstract.** We wanted to know one thing: what is the single best *skill* — the
> instruction file given to an AI orchestrator — for spawning a swarm of AI workers
> and finishing complex coding tasks? Over three rounds and ~94 graded runs (~$480
> of real API spend), we benchmarked eight generations of one skill on purpose-built
> test projects with hidden answer keys, measuring **Speed, Correctness, Turns,
> Cost, Context, and Swarm Control**. Most of what we believed at the start was
> wrong, and the failures taught more than the wins. The living result: a lean
> skill whose three drift-prone decisions are *computed instead of judged*, run by a
> strong orchestrator at moderate thinking effort, delegating to the cheapest
> workers that clear a deterministic gate. Charts and full tables:
> **[boord-its.com/skills](https://boord-its.com/skills)**.

---

## 1 · The question

A single strong AI session can carry a surprising amount of work. But complex
coding tasks — dozens of files, hundreds of edit points, more source than fits in
one context window — eventually break it. The obvious answer is delegation: one
orchestrator planning and verifying, a swarm of cheaper workers implementing. The
non-obvious questions are *when* that pays, *what the orchestrator must actually
do*, and *how little* you can spend on any given seat without losing correctness.

Frameworks usually assert answers. We measured them.

## 2 · Plain words

- **Orchestrator** — the one AI session in charge. It plans, briefs, delegates,
  and verifies. In the winning design it writes no product code itself.
- **Swarm / workers** — cheaper AI sessions the orchestrator spawns, each owning a
  small, exclusive slice of the job.
- **Skill** — the markdown instruction file that tells the orchestrator how to run
  all of the above. The thing under test.
- **The scale wall** — the point where a job stops fitting in one AI session.
  Below it, one strong session wins. Above it, one session breaks down and
  delegation is the only thing that scales.
- **Effort** — how hard a model is allowed to think before acting (its reasoning
  budget: low → medium → high → max).
- **Hidden answer key** — a grading script the skill never sees, copied into the
  project only *after* a run ends. Every claim in this paper is scored by one.
- **Turns** — orchestrator round-trips. A cheap-looking metric that turned out to
  be the budget that actually kills sessions.

## 3 · Method

**Test projects.** Purpose-built, frozen codebases with a genuine difficulty
gradient: a 22-requirement service build (shared contracts, security gate, money
math, concurrency — plus boilerplate), a six-page static site that sits right at
the solo-vs-swarm limit, and a 68-edit-point migration across 33 files laced with
traps that defeat find-and-replace. Every run starts from an identical frozen copy.

**Grading.** A hidden answer key per project, applied only after the run. Partial
credit is per-requirement and per-edit-point, so we can see *what kind* of work a
configuration drops, not just pass/fail.

**Honest accounting.** Worker spawns are counted from the raw event stream — not
from the model's self-report (models claim delegation they didn't do). Costs are
API-equivalent dollars from real runs. The orchestrator's model and effort are
pinned per configuration. Failed runs, losing designs, and our own reversed
conclusions are all published; sample sizes are small (1–3 runs per cell) and we
say so.

**Pinned model generation.** Every number describes one recorded generation of
models (currently Haiku 4.5 / Sonnet 5 / Opus 4.8, with the top-tier seat
experiments on Fable 5); each run logs the exact model IDs, and the harness trips
an alarm if a provider release re-points a tier mid-study. New releases are
re-qualified against the champion's cells before any published number changes —
a release is treated as a fresh optimization opportunity, never a silent upgrade.

## 4 · Results

### 4.1 Round 1 — the ceremony didn't help

We began with an elaborate multi-agent system: rich personas, a battery of
mandatory review gates, a director hierarchy. Controlled tests kept three things
and killed the rest:

- **Kept: dependency-ordered handoffs.** Giving a downstream worker the *finalized*
  upstream state instead of a guess was the entire difference between 0/3 and 3/3
  on integration correctness. The one idea with clean causal evidence.
- **Kept: context isolation.** Workers explore in their own windows and return
  short reports; the run that built this repo quarantined ~1.19M tokens away from
  the coordinator.
- **Kept: one deterministic check.** A typecheck/test/build with an exit code. In
  our ablation, *every* persona variant emitted the same hallucinated false
  positive; the compiler caught the real break.
- **Killed: persona backstories.** A placebo-controlled ablation — an elaborate
  security-reviewer backstory caught no more planted bugs than "you are a security
  reviewer," and an *irrelevant* backstory did just as well. Identity flavor is
  legible; it is not performance.
- **Demoted: everything unvalidated.** The gate battery, the hierarchy, the
  finely-drawn roles — never tested, so never required.

### 4.2 Round 2 — the knowing-doing gap, and where the wall really is

We then benchmarked the skill itself, six generations head-to-head.

- **Below the wall, refusing to delegate wins.** For any job that fits one
  session, swarms are pure overhead — forcing delegation there cost +86–104% for
  zero correctness gain. The winning skill *computes* a go/no-go from counted
  work (edit points, files, reading volume) and prints its verdict before acting.
- **At the wall, delegation is the only thing that scales.** On the 68-edit
  migration, the single session died on the easy work two runs in three; a routed
  swarm posted the cheapest passing runs on record. Turns — not tokens — were the
  killing budget: ~33 orchestrator turns routed vs 112–167 unrouted.
- **The knowing-doing gap.** Across 28 unforced runs, earlier skills produced
  *textbook* delegation plans when asked to plan — then quietly did everything
  themselves in real runs, every time. Prose rules defect; computed rules hold.
  The fix that survived: a computed gate plus a plan written to a data file that
  the final reconciliation is checked against.
- **Heavyweight apparatus failed twice.** A rebuilt suite with worktrees,
  manifests, and intake scripts benchmarked no better than the lean loop — its
  machinery never activated in real runs.

### 4.3 Round 3 — effort, the worker floor, and four challengers that lost

- **Even the SEAT is nearly fungible — our predictions failed in the best way.**
  We put the mid-tier and cheapest models in the *orchestrator* seat, predicting
  the first would crack at scale and the second would fail outright. Both passed
  everything. The cheapest seat landed within noise of the champion's cost — and
  its telemetry shows how: it *hired seven top-tier workers* for the risky parts.
  A weak seat that knows its limits buys judgment downstream; a strong seat keeps
  judgment and buys cheap hands. Both clear the gate, because the skill supplies
  the decisions either way. (Small samples; the mid-tier seat also lost on price —
  too expensive to be free, too weak to hold critical work itself. On both the
  effort ladder and the seat ladder, the middle is the worst place to stand.)
- **The worker floor was never found.** We replayed real worker briefs from
  validated runs at every model × effort combination: 20/20 passed, including the
  cheapest model at *minimum* effort through a trap-dense cluster at a third of
  the mid-tier price. With a good enough brief, worker choice is a **speed dial,
  not a correctness dial**. The brief *is* the orchestrator's judgment, exported.
- **The effort ladders kept correcting us — all the way to the bottom.** Max
  effort over-thinks (+44% on the planning-heavy project for nothing). One rung
  down held everything, and we declared the optimum "bracketed" when the rung
  below it cracked once. Then the bottom rung went perfect with the all-time cost
  records, and the k=4 tie-break settled it: **minimum effort is the champion** —
  8/8 passing, cheaper AND faster than high everywhere, with non-overlapping cost
  ranges on the scale-wall project (low's worst run beat high's best). Once the
  route decision is computed and the gate is a script, the orchestrator's job is
  to execute the plan — paying for deliberation the skill already did is pure
  tax. The middle rung keeps the only correctness blemish in the study (5/6):
  if you deviate at all, go to the bottom, never halfway. Meanwhile the
  *top-tier* model in the orchestrator seat got cheaper AND faster at every step
  down, finishing an entire swarm in **two orchestrator turns** at minimum effort
  — all-time speed records, at roughly double the seat price.
- **Dispatch-as-code: proven, parked.** Scripting each batch (so serial dispatch
  is structurally impossible and every worker gets an explicit effort) worked —
  100% correct, zero out-of-scope files, turns collapsed. It also re-transmitted
  the entire brief set per batch and lost on cost at *both* efforts tested
  (+21–48%). Structural overhead, not thinking depth. Parked on single-variable
  evidence.
- **The counting gate: proven, parked.** Adding a mandatory count-every-edit-point
  gate (the exact counter to the one graded miss we ever observed) stayed 100%
  correct — free on migration-shaped work, a +33% tax on build-shaped work,
  protecting against a failure that only appears below the effort we ship.
- **The plateau.** The lean skill at high effort has now survived four
  challengers. The text is at a measured plateau; the remaining headroom is in
  dials and unmeasured regimes, not prose.

### 4.4 The complete matrix (four seats × five efforts, the full worker grid, and scale)

The final campaign tested everything evenly — every orchestrator seat (top-tier,
strong, mid, cheap) at every effort rung (low → max, a fifth rung most people
don't know exists), the full 45-cell worker grid, and the 400K-token deep audit.

- **The worker floor: 45/45 cells green, 90 graded runs, zero failures** — the
  cheapest model wrote the security-critical shared module correctly at every
  effort level. On brief-carried work, the floor simply does not exist.
- **Both max-effort ladders are monotone**: cost rises with every rung of extra
  thinking on both the top-tier and strong seats (the top seat's build-project
  ladder runs 5.73 → 8.92 → 9.91 → 12.39 → 13.15). Effort is a tax on decisions
  the skill already made.
- **A dark horse, then a lesson in sample size:** the mid-tier seat at *minimum*
  effort posted a USD 2.31 run — the first swarm ever to beat the no-skill
  baseline on the small project. The k=4 tie-break then revealed that run as an
  outlier (its siblings: 4.31–5.92); ranges overlap the champion's and the crown
  stayed put. What survives is bigger than a crown: **two different models in the
  orchestrator seat now produce statistically indistinguishable swarms across 16
  graded runs each.** The skill is the orchestrator; the seat is a rental — and
  the tie-break policy caught its own headline before we shipped it.
- **The middle curse, third sighting:** the cheap seat's effort ladder failed at
  exactly the middle rung (and, newly, at max — the study's first over-thinking
  *breakage* rather than mere tax). Top or bottom. Never the middle.
- **At scale, the swarm finally separates on correctness — and wins on price.**
  On the 400K-token audit the crowned config passed every run at a **median USD
  15.39 vs the single session's USD 36.60** (which also passed, at 9× its usual
  prices) — and the runner-up config dropped a run there, independently
  validating the tie-break. Delegation's promise, graded: **42% of the
  monolith's price in the regime delegation was invented for.**

Live, sortable, with every losing run shown: [boord-its.com/skills](https://boord-its.com/skills).

## 5 · Discussion — three laws we keep re-measuring

1. **Judgment concentrates at the top.** Quality lives in the plan and the briefs;
   worker strength only buys wall-clock. Spend on the orchestrator's *artifacts*,
   not on worker glamour.
2. **Computed beats prose.** Every rule that mattered eventually defected when
   expressed as prose and held when expressed as a computation, a data file, or an
   exit code. If a decision can drift, make it arithmetic.
3. **Effort optimum scales inversely with capability.** The more capable the seat
   — orchestrator or worker — the less deliberate thinking it needs. Max effort is
   mostly a tax; the correctness risk we observed lives in the *middle* of the
   ladder, not the bottom.

And the standing guardrail behind all three: **reports are claims; exit codes are
evidence.** LLM review never gates anything here.

## 6 · Limitations

Small samples (1–3 runs per cell). One stack (Claude Code, headless), one family
of models, API-equivalent pricing. Three test projects — broad in shape but not in
domain. Correctness ceilings on several boards (many configs at 100%, separated
only by cost/speed). Two cells remain unrun: the top-tier seat at minimum effort
on the migration project (blocked by a usage cap mid-campaign) and the
very-large-context regime the delegation gate was partly designed for. The
supervised interactive path (human approves the plan mid-run) is exercised daily
but not benchmarked.

## 7 · Use it / reproduce it

- **The skill:** [`.claude/commands/orchestrate.md`](.claude/commands/orchestrate.md)
  — copy into `~/.claude/commands/`, run the orchestrator at high effort.
- **Enforcement hooks:** [`hooks/`](hooks/) — the mandate, lane floor, and lane
  ceiling as denied tool calls, with an 18-case test suite.
- **The roster:** [`orchestration-team/`](orchestration-team/) — worker personas
  as valid Claude Code subagents (flavor, not magic; see §4.1).
- **The museum:** [`archive/`](archive/) — every retired generation with its cause
  of death.
- **Round-1 experiments:** [`examples/eval/`](examples/eval/) — the controlled
  tests behind §4.1, including the one that disproved our founding assumption.

*This document was restructured from round-by-round findings into paper form on
2026-07-18; the full evolution is in the git history.*
