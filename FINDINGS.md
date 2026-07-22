# One Skill to Run a Swarm

**Benchmarking AI orchestration for complex coding tasks — a working paper.**

> **Abstract.** We wanted to know one thing: what is the single best *skill* — the
> instruction file given to an AI orchestrator — for spawning a swarm of AI workers
> and finishing complex coding tasks? Over three rounds plus a local-hardware
> chapter — 256 graded runs, ~$790 of real API spend on the study ledger — we
> benchmarked eight generations of one skill on purpose-built test projects with
> hidden answer keys, measuring **Speed, Correctness, Turns, Cost, Context, and
> Swarm Control**. Most of what we believed at the start was wrong, and the
> failures taught more than the wins. The living result: a lean skill whose three
> drift-prone decisions are *computed instead of judged*, run by a strong
> orchestrator at low thinking effort, delegating to the cheapest workers that
> clear a deterministic gate. Taxonomy, for skill-library builders: this is a
> **software-engineering** skill whose function is **multi-agent orchestration**
> — it runs the team rather than writing the code, and every claim here was
> earned on coding fixtures only. Charts and full tables:
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

### 4.5 The local lane — worker fungibility leaves the API

The worker floor said the card is the quality mechanism and the model only buys
wall-clock. We tested whether that law survives leaving the API: open-weights
models on one RTX 3090 (24 GB, LM Studio serving an Anthropic-compatible
endpoint), replaying the same graded worker briefs through the same harness.

- **The parity result, honestly scoped:** a quantized 35B MoE (Qwen3.6-35B,
  ~3B active) went **6/6 official on the hardened bench cards — the same
  perfect floor Sonnet 5 holds as a worker** — at 3–9× the wall and $0
  marginal cost. This is *worker-role parity on curated briefs*, not general
  parity: on public SWE-bench the open ladder trails (51.6–70.6% vs Sonnet
  5's 82.1%), and on live-written briefs the gap reappears (below). We never
  benched Sonnet 4; the study pins one generation and compares inside it.
- **The ladder's optimum is interior, again:** 30B (84 tok/s) coin-flips the
  critical card; 35B (30 tok/s) is perfect — fewer, surer turns pay for the
  slower decode; 80B (13 tok/s at depth) collapses **no** further turns, so
  its halved decode is pure loss: 5/6, one 99-turn spin, walls 2×. The same
  bend-back curve we measured on the effort dial and the seat ladder, now on
  parameter count.
- **One card is a queue, not a swarm:** 2- and 4-way parallel slots made every
  batch *slower* than sequential (+10–18%) — decode shares one
  memory-bandwidth pool. A 30B running entirely from system RAM beside the
  GPU resident held correctness under co-load but netted ~0 extra throughput
  (an overflow valve). Hardware corollary: a second identical card is the
  only purchase that adds a worker; a bigger die is still one pool.
- **The orchestrated-local variant failed graduation — instructively.** Five
  arena runs produced four *novel* defection modes, each caught verbatim in
  retained streams and pre-refuted in the next text iteration: a **fourth
  excuse** ("I hold the full call-site map in context now; I'll execute
  directly rather than re-fragmenting the trap knowledge across workers" —
  the inventory step itself breeds it); a discovery coin-flip whose fallback
  dissolved into solo; fire-and-forget dispatch that graded half-done work
  while orphaned workers were still generating; and a tool-timeout ceiling
  that amputated the local legs of an otherwise-correct run. Run 5, fully
  mechanized: both local lanes carried real work, displaced API spend
  collapsed — and correctness broke at 59/68 on briefs written live
  (curated briefs: 6/6, same model), while 45 turns of seat babysitting
  priced the run at parity with the all-API champion.
- **Economics, measured:** a Sonnet-class worker job is $0.25–0.56 on the
  API; local it is $0 at 2.3–8.5 min. One saturated overnight ≈ 145 jobs ≈
  $52 displaced against ~$0.34 of electricity; a used ~$1,300 card
  breaks even in ~25 saturated nights — *if* dispatch is direct. The fully
  orchestrated mode doesn't save until the seat cost is dieted or the work is
  batched; six graduation runs in, it reaches 68/68 edit sites with zero API
  worker spend and fails on one unexecuted import — the gap is now a gate
  stanza, not a discipline.

### 4.6 The challengers round — re-sweep the field, then re-crown it

Asked whether we had tested the *best* local models, the honest answer was no:
the shortlist was six months stale. One fresh web sweep picked five
challengers (three dense — the all-MoE ladder's missing archetype — plus two
fast MoE; two required direct downloads the catalogs didn't carry), and one
scripted overnight gauntlet graded them all on the same briefs: a ≥8 tok/s
decode bar, then the three worker cards, 3-for-3 earning a second pass.

- **The crown changed hands.** Qwen3.6-27B went 6/6 at k=2 and beat the
  sitting 35B resident's wall in *every* cell — the long card in less than
  half the time (181–217s vs 427–506s) at 38 tok/s. It now holds the GPU
  seat, and its smaller footprint returns ~3 GB of VRAM.
- **The round's wildest number:** gpt-oss-20b ran the trap-dense brief — all
  11 must-not-change traps held — in **21 seconds: the API floor's own
  wall-clock, from a $0 local card** (130 tok/s). It loses the long march
  (5/13 on the sweep card), so it serves as a burst tool for short briefs
  only; on the RAM pool it converges to the same ~8 tok/s as everything else
  and loses its magic entirely.
- **Correctness ceilings everywhere; walls decide seats.** Gemma 4 31B also
  went 6/6 — at 12 tok/s and 3–25× the winner's walls: perfect and
  unseatable. The agent-tuned dense contender (Devstral Small 2) burned turn
  caps exploring; one newcomer couldn't drive the harness at all (0/3,
  spin-to-cap).
- **Method finding, possibly the transferable one:** model knowledge decays
  in months, and the only reason re-ranking the entire local field cost $0
  API and one night is that the harness already existed. Keep the gauntlet
  cheaper than your staleness.

Live, sortable, with every losing run shown: [boord-its.com/skills](https://boord-its.com/skills).

## 5 · Discussion — the laws we keep re-measuring

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

The local-lane chapter re-measured all three from new angles — law 1 from the
failing side (the same 35B: curated briefs 6/6, live-written briefs 59/68 —
the brief, not the brain, carried the quality), law 3 on a new axis (parameter
count bends back exactly like effort did), and it added a fourth we now treat
as standing:

4. **One bandwidth pool is one worker.** Parallelism only comes from genuinely
   separate pools (a second card, system RAM, the API) — splitting a shared
   pool into lanes made every batch slower than single-file, at every width we
   tried. Fifth confirmation: every model we ran CPU-side, however fast on
   GPU, converged to the same ~8 tok/s — the pool's ceiling, not the model's.
   Scale out, never up.

5. **Re-sweep before you buy, build, or crown.** Our local-model shortlist
   went stale in six months; one fresh sweep and one $0 overnight re-ranked
   the whole field and dethroned our certified resident. Standing rule: any
   claim of "best available model" carries a date, and the harness must stay
   cheap enough to re-run when that date ages.

And the standing guardrail behind all three: **reports are claims; exit codes are
evidence.** LLM review never gates anything here.

## 6 · Limitations

Small samples (1–3 runs per cell). One stack (Claude Code, headless), one family
of API models, API-equivalent pricing. Three test projects — broad in shape but
not in domain. Correctness ceilings on several boards (many configs at 100%,
separated only by cost/speed). Two cells remain unrun: the top-tier seat at
minimum effort on the migration project (blocked by a usage cap mid-campaign)
and the very-large-context regime the delegation gate was partly designed for.
The supervised interactive path (human approves the plan mid-run) is exercised
daily but not benchmarked. The local-lane chapter is one GPU, one quantization
family, k=1–2 per cell; its parity claim is card-scoped by construction, and
the orchestrated-local variant is published as a failed graduation, not a
recommendation.

## 7 · Threats to validity — answered where we can, conceded where we can't

We wrote our critics' best arguments down before they did. Where we have an
answer, it's here; where we don't, that's here too.

- **"The fixtures and answer keys are private — unfalsifiable."** They stay
  private for the same reason every serious benchmark's do: a grader that can
  leak into training data is a dead grader, and half our fixtures wrap real
  private code. Private test sets are the norm (chat arenas don't pre-publish
  prompts; abstract-reasoning benchmarks keep held-out sets) — what keeps a
  private bench honest is not disclosure but **third-party entries through the
  same pipe**. Hence §8: the arena is open. Send a skill; we run it blind and
  publish the row, win or lose, next to our own losers.
- **"n=1–4 per cell is not statistics."** It wasn't — so we ran the
  confirmation. The pre-registered n-scaling pass (protocol committed before
  spend: cells, k, bootstrap CIs, Mann–Whitney, success criteria,
  publish-regardless) took every decisive cell to k=25 — ~150 clean graded
  rows, ~$710 across two tiers. The honest headline: the champion's small-n
  8/8 did NOT survive scale (80% on the hard refactor at k=25; runner-up 88%;
  monolith 64%), and at equal n the gap FIRED the protocol's pre-registered
  dethronement trigger — the study's own published rule removed the study's
  own champion, and the correctness crown moved to the high-effort
  configuration. What survived, equally decisively, is the cost claim: the
  low-effort cost CIs sit fully below high's on both fixtures (p<0.0001,
  rank-biserial 0.85–0.98 — the largest effects in the study), and under
  retry-until-green economics (pre-registered before analysis) it stays
  cheapest AND fastest to a green gate in every cell: $5.81/8.3min on the
  refactor vs $7.62/13.3min (high) and $11.94/23.1min (monolith). The end
  state is two crowns — high effort when one pass must land, low effort under
  a retry loop and a gate. Small-n perfection died in public, exactly as the
  protocol promised it would if it was going to; the medians are no longer
  estimates.
- **"You graded your own exam."** The exams are deterministic: planted bugs,
  counted edit-points, executable checks, exit codes. When a test is "did the
  planted trap survive? did the suite pass?", self-grading is just *grading* —
  the same way a proctored multiple-choice exam doesn't care who feeds the
  scantron. We can argue all day about whose website is prettier; we cannot
  argue about whether the website was built. Open-ended *quality* judging is
  phase two of that argument and would need juries or votes; this paper is
  phase one, on purpose.
- **"You only beat your own variants."** True, and the fix is structural, not
  rhetorical: the open challenge (§8) exists so the comparison set stops being
  ours. Until entries arrive, the strongest external anchors are the monolith
  control (the no-skill baseline any framework must beat) and the local-model
  challengers round, where five outside models ran the same gauntlet and
  re-ranked our own residents.
- **"A 27B is not better than Sonnet."** Agreed — we never claim it. The
  claim's exact shape: in the *worker role*, on *these graded briefs*, the 27B
  delivered the same correctness at 2–4× the wall-clock for $0 marginal cost
  on owned hardware. Same exam, same grade, different bill. General-capability
  gaps (SWE-bench et al.) are stated alongside every parity claim.
- **Conceded without contest:** one stack (Claude Code), one API model family,
  code fixtures only, small n until the k=25 pass runs, and an inference-engine
  version that moved mid-study for the challenger rows (recorded per row).

## 8 · The open challenge

Think your skill does better? Send one skill file (a Claude Code command — a
single .md) via an issue on this repo. We read it, run it through the same
frozen projects, hidden answer keys, and pinned models as every arm in this
paper, and publish the result — win or lose, attributed or anonymous, your
call. One entry per person per round; obviously-hostile files don't run
(submissions execute with tools in isolated copies, after human review).
Deterministic checks decide. Taste is a different tournament.

## 9 · Use it / reproduce it

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
