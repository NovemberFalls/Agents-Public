# skills-bench

> **An open benchmark for AI agent skills — scored *only* where a deterministic
> oracle exists.** The first track is multi-agent software orchestration, and its
> headline result is a published null result against our own founding hypothesis.

We built an elaborate multi-agent orchestration system — rich personas, a battery
of mandatory review gates, a director hierarchy — and then did the thing frameworks
usually skip: we tested our own assumptions against hidden answer keys. **Most of
them did not survive.**

The one that did is the one worth quoting:

> **A reviewer persona produces an _opinion_. A typecheck / test / build produces a
> _fact_. Gate on the fact.**

That cuts against where most of the industry is currently pointed — toward
LLM-as-reviewer, agent debate, and ever-richer evaluator personas. In our
placebo-controlled ablation, *every* persona variant emitted the **same
hallucinated false positive** ("`hmac.new` doesn't exist" — it does), no matter how
elaborate its backstory. The deterministic `mypy` oracle is what caught the *real*
integration break. A persona is theater; a typecheck is a fact — and the finding
generalizes well past coding agents.

**Read the study: [FINDINGS.md](FINDINGS.md) — _One Skill to Run a Swarm_.** ~400
graded runs (257 API-lane + 141 local-hardware), eight generations of one
orchestration skill benchmarked on Speed · Correctness · Turns · Cost · Context ·
Swarm Control, with the decisive cells confirmed at **k=25** under a pre-registered
protocol. Interactive charts, every losing run shown:
**[boord-its.com/skills](https://boord-its.com/skills)**.

> **On sample size (read this).** The load-bearing claims are **confirmed at k=25**
> under a protocol registered before spend (~150 graded runs, bootstrap CIs,
> Mann–Whitney) — including a pre-registered *dethronement trigger* that removed our
> own small-sample "perfect" champion when it failed to survive scale. Exploratory
> and secondary cells remain **n=1–3** and are labeled where they appear. Read the
> powered medians as measured; read the n=1–3 rows as directional.

---

## What survived the evidence

Three ideas earned their place. Only these. In order of how far they transfer:

1. **Gate on a fact, not an opinion.** One deterministic check with an exit code — a
   typecheck, test suite, or build — is the only verification gate the evidence
   supports. LLM "review" gates hallucinated identically across every persona we
   tried and gated nothing real. This is the most transferable result in the study
   and it stands alone: [docs/the-deterministic-check.md](docs/the-deterministic-check.md).

2. **Forward finalized state, don't let downstream agents guess** — the Change
   Dependency Graph (CDG). In a controlled test, dependency-ordered forwarding of an
   upstream agent's *actual* finalized output was the entire difference between
   **0/3 and 3/3** on integration correctness. It pays for itself *only* once a task
   is too big for one context window; below that line it is pure overhead.

3. **Isolate context via subagents.** Each specialist explores in its own window and
   returns a short report, so the coordinator stays lean enough to run a large task
   without compaction. This is just using subagents as intended.

Plus one rule that governs all of it: **use a single agent until the task outgrows
one context window.** Below that measured crossover, coordination is overhead, and a
plain monolith was both the cheapest *and* a fully correct configuration in our eval.

---

## Results at a glance

The numbers behind the claims. Full tables, CIs, and every losing run in
[FINDINGS.md](FINDINGS.md); charts at [boord-its.com/skills](https://boord-its.com/skills).

**Compute-then-apply vs. a worker model editing in place** — mechanical fan-out, k=25:

| metric | compute → deterministic apply | model edits in place |
|---|:---:|:---:|
| cost / run | **$0.46** | $1.19 |
| wall (p50) | **102s** | 173s |
| output tokens (min / p50 / max) | **9.2 / 10.1 / 12.6k** (±15% band) | 5.2 / 17.6 / 26k (wide) |
| correctness (raw / via gate) | 88% / ~100% | 96% / ~100% |

~1.7× faster, ~2.6× cheaper, **variance collapsed to a ±15% band.** End-to-end on the
full fixture (k=3): **$1.91 / 336s vs $3.85 / 624s** — both 16/16, so ~1.9× faster and
2.0× cheaper at matched correctness.

**Turns — not tokens — were the budget that killed sessions.** A computed route ran a
full swarm in **~33 orchestrator turns vs 112–167** unrouted, and at minimum effort
finished an entire swarm in **two turns.** Forcing delegation *below* the scale wall
cost **+86–104%** for no correctness gain.

**Effort is mostly a tax** (pre-registered n-scaling, k=25, ~150 runs). Low-effort cost
sits **fully below** high-effort on both fixtures (**p<0.0001, rank-biserial 0.85–0.98**
— the largest effects in the study). Under retry-until-green: **$5.81 / 8.3min (low) vs
$7.62 / 13.3min (high) vs $11.94 / 23.1min (monolith).** The honest twist: at equal n the
small-sample "perfect" champion **did not survive** (80% vs high's 88% on the hard
refactor) — our own pre-registered dethronement trigger fired and moved the *correctness*
crown to high effort. End state: **two crowns — high effort when one pass must land, low
effort under a retry loop and a gate.**

---

## The leaderboard — who won each fixture, and why v5.0

Three purpose-built fixtures spanning the difficulty gradient, each with a hidden
answer key. The winner flips with the work, exactly as the scale-wall rule predicts:

| Fixture (shape) | Solo / monolith | v4.1 swarm | v5.0 apply-tier | Winner — why |
|---|:---:|:---:|:---:|---|
| **arena_website** — 6-page site, *at the wall* | ✅ 3/3 · **$2.4** | ✅ 3/3 · $2.9 | ✅ 3/3 · $2.5 | **Solo** — cheapest, all correct. Below the wall, coordination is pure overhead. |
| **arena_feature** — 22-requirement build, *generative* | ✅ 3/3 · **$3.7** | ✅ 3/3 · $4.5 | ✅ 3/3 · $4.3 | **Solo** cheapest; v5.0 ≈ v4.1 — the apply-tier never fires on generative work, so it's a clean no-regression. |
| **arena_refactor** — 68-edit migration, *diffable* | ❌ **1/3** · $7.6 | ✅ 3/3 · $10.5 | ✅ 3/4† · **$8.2** | **v5.0** — solo *cracks to 56%*; orchestration becomes necessary, and the apply-tier lands it **~22% cheaper than v4.1 at matched correctness.** |

*Per-tier detail: on arena_refactor the monolith dropped **17 of 39 MUNDANE nodes** (find-and-replace traps) while every orchestrated arm held. †v5.0's one raw miss was detected and recovered through the deterministic gate + escalation ladder (§4.9), not force-applied. Full tables, CIs, and every losing run in [FINDINGS.md](FINDINGS.md); interactive bar charts at [boord-its.com/skills](https://boord-its.com/skills).*

**Why v5.0 ships as the default, in one line:** on the only fixture where you *must*
swarm, it wins on cost while matching correctness; on the two where you shouldn't
swarm at all, it costs the same as v4.1 and the rule correctly routes you to solo.
It is never worse and sometimes decisively better — a strict superset.

---

## What we were wrong about (the null results)

These are the reason to trust the section above. Full detail in [FINDINGS.md](FINDINGS.md):

- **Persona backstories did nothing.** A placebo-controlled ablation: an elaborate
  security-reviewer backstory caught no more planted bugs than a bare "you are a
  security reviewer," and an *irrelevant* (performance-engineer) backstory did just
  as well on security bugs. Identities are kept as **flavor** — useful for a legible
  roster, not because they improve output.
- **The mandatory-gate battery and the director hierarchy were never validated** —
  and the extra review passes, re-passed state, and parallel ceremony **cost tokens**
  without earning them. Demoted to optional; the heavier pieces moved to [`extras/`](extras/).
- **More agents isn't better on small tasks.** The monolith was cheapest and correct;
  coordination only pays once a task is too big for one window.
- **Max reasoning effort is mostly a tax.** A strong orchestrator at *low* effort held
  correctness while max effort mostly bought cost. A good-enough brief makes the
  worker model a **speed dial, not a correctness dial.**

The takeaway: **gate on a fact, forward finalized state, isolate context, and don't
over-build.** That is the whole product.

---

## Field use — what this framework built

This isn't only a benchmark. The orchestration model here is the toolchain one
engineer used to ship a portfolio of production systems — measured from `git`
history (**active-days** = distinct calendar days with at least one commit, the
honest hands-on-keyboard proxy), not estimated.

**The headline is concurrency, not any single system:** at the 2026 spring–summer
peak, **6–8 production systems were live in the same week**, sustained across ~5
months, solo — each reaching working state in a few dozen active build-days, in
parallel rather than in series. These aren't ten unrelated repos; they're a
**system-of-systems**, and this orchestration harness is the factory the rest were
built with. That is the strongest evidence the model works: it is load-bearing in
production, not just on fixtures.

A sample of what shipped on it — build facts only, git-measured:

| System | What it is | Active days | Signal |
|---|---|---:|---|
| **[claude-cockpit](https://github.com/NovemberFalls/claude-cockpit)** | Multi-session Claude Code manager | 36 | 545 automated tests, CI on every push (public, AGPL) |
| **[Branchive](https://branchive.io)** | Hosted VCS for Unreal teams | 22 | 57-tool MCP behind OAuth 2.1, auth-on in production |
| **[BITSM](https://bitsm.io)** | Multi-tenant AI-native ITSM | 40 | 3-tier agentic triage (Haiku → Sonnet → human), 10k-doc RAG |
| **[Klikor](https://klikor.io)** | Macro-pad platform | 57 | 62 licenses in the field |
| **ops-mcp** | Autonomous infra incident triage | 19 | 19-tool MCP, 6-level escalation |
| **[Order](https://project-order.com)** | Rust/Axum platform (the spine) | 73 | 795 commits, sustained multi-month backbone |
| **Propulsen** | Bespoke deal-management platform | 25 | live, deployed, under maintenance |
| **[Bits News](https://boord-its.com/news)** | Local-inference voice-AI pipeline | — | working, scheduled system in a ~12-hour build |

*LOC is omitted on purpose — it's a coarse, partly-scaffolded proxy, not an
achievement. The trustworthy signals are active-days, tests/CI, and real adoption.*

---

## Method & reproducibility

Every claim in this study is scored by a **hidden answer key** — a grading script the
skill never sees, copied into the frozen test project only *after* a run ends. The
oracles are deterministic: planted bugs, exit-code checks, per-requirement partial
credit. "You graded your own exam" doesn't apply when the exam is a script with a
non-zero exit.

- **Test projects.** Purpose-built, frozen codebases with a real difficulty gradient
  (a 22-requirement service build, a six-page site at the solo/swarm limit, a
  68-edit-point / 33-file migration laced with find-and-replace traps).
- **Honest accounting.** Worker spawns are counted from the raw event stream, not the
  model's self-report (models claim delegation they didn't do). Costs are
  API-equivalent dollars. Model IDs and effort are pinned per configuration.
- **Fixtures held privately, by design.** The graded fixtures and answer keys are *not*
  published — an open answer key stops being a hidden answer key, and keeping the
  arena's contents private is standard practice for a benchmark that intends to keep
  measuring new model generations fairly. What *is* fully disclosed is the
  **methodology, the oracle design, and the exact gate setup** — enough to reproduce
  the *shape* of any result on your own substrate:
  [docs/the-deterministic-check.md](docs/the-deterministic-check.md) walks the exact
  `mypy` + Pydantic-plugin oracle that caught the real bug. Internal runs at higher N
  will be posted as results, not fixtures.

---

## Honest limits (kept exactly as brutal as they should be)

- **Mixed N, and labeled.** Decisive cells are powered at **k=25** (~150 runs,
  pre-registered CIs and significance tests); exploratory and secondary cells are
  **n=1–3** and marked as such. Not every cell is powered — but the ones the
  conclusions rest on are, and our own pre-registered rule dethroned a champion when
  the numbers said to.
- **One model generation.** Every number describes one recorded generation
  (Haiku 4.5 / Sonnet 5 / Opus 4.8, top-tier seat on Fable 5). A provider release is
  re-qualified against the champion, never silently adopted.
- **Coding fixtures only.** Every claim was earned on software-engineering tasks. The
  deterministic-gate result plausibly generalizes; we have not measured that it does.
- **Narrow contract changes.** The CDG eval used a free-choice rename — the simplest
  kind of contract change. A structural change (splitting one field into two) is the
  stronger trap, and a follow-up.

If we extend the work, we extend this section with it.

---

## Scope — what gets a leaderboard, and what doesn't

skills-bench is organized as **domain tracks**, but it holds itself to the same rule
it found for orchestration: **we only publish a leaderboard where a deterministic
oracle exists.** A track earns a scoreboard when "correct" has an exit code — a
typecheck, a test, a known number — not a reviewer's opinion.

| Track | Oracle | Status |
|---|---|---|
| **Software** (this study) | typecheck / test / build | **live** |
| **Analytics** | known query results — a number is checkable | planned (deterministic) |
| **Medical / Legal** | none — "correct" is expert judgment | **deliberately not leaderboarded** |

Medical and Legal are *not* scored here, and that is on principle: the study's own
headline is that an LLM "judge" is theater. Grading a clinical or legal answer with
another model would reproduce exactly the failure we published. Those domains get a
track when — and only when — someone solves the oracle, not before. Refusing to
score what we cannot score deterministically is the same discipline as the gate.

---

## Appendix: the skill, if you want to run it

The framework is the *minimal thing the evidence supports*, not the headline. If you
want to use it:

### The command
`/orchestrate <task>` — one self-scaling entry point (v4.1): it *counts* the work
(sites, files, read volume), prints a `GATE: SOLO|SWARM` verdict, and obeys it. Solo
with checklist discipline below the measured crossover; a lane-routed worker swarm
(haiku/sonnet/opus) with a plan file and deterministic gates above it. The skill is
[`.claude/commands/orchestrate.md`](.claude/commands/orchestrate.md) (with
[`fix.md`](.claude/commands/fix.md) for the single-issue path). Copy into
`~/.claude/commands/`.

### The agents
The specialists live in [`orchestration-team/agents/`](orchestration-team/agents/) —
each a valid Claude Code subagent (`name` + `description` + `model`). Copy the ones
you want into `~/.claude/agents/`, or load a body as an Agent SDK system prompt.

### The gate
Wire a deterministic check as the one required gate — the pattern and the exact setup
that worked are in [docs/the-deterministic-check.md](docs/the-deterministic-check.md).

### Repo layout
```
├── FINDINGS.md                     # THE STUDY — read this first
├── docs/
│   ├── the-deterministic-check.md  # the one validated gate — how to wire it
│   ├── architecture.md             # the CDG, tiers, the verification gate
│   ├── token-efficiency.md         # where the tokens went
│   └── authoring-an-agent.md
├── examples/
│   ├── eval/                       # the controlled experiments (method + results)
│   ├── real-run/                   # metered tokens from the run that built this repo
│   └── orchestrated-run/           # a worked CDG example + context ledger
├── .claude/commands/               # the loop (orchestrate.md) + the lightweight path (fix.md)
├── orchestration-team/             # orchestrator + role specialists
├── hooks/                          # optional enforcement as denied tool calls
├── archive/                        # retired generations + why each died (the ledger)
└── extras/                         # NOT the validated core — kept for reference
```

---

## Built by

**November Falls.**

## License

MIT — see [LICENSE](LICENSE).
