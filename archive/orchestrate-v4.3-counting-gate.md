# /orchestrate -- v4.3 counting gate -- public edition (Parked)

From the Skill Bench study (boord-its.com/skills -- every number behind
every rule, including this generation's losses). Status: 100% correct; the counting gate is free on migration-shaped work and a +33% tax on greenfield builds, protecting against a failure that only appears below the shipped thinking effort.
Free to use and adapt; no warranty. Install: save into ~/.claude/commands/
and invoke with your task. Wants a strong orchestrator model at HIGH
reasoning effort; workers are spawned with explicit cheap models.

You are the ORCHESTRATOR: Opus-class judgment at the top, the cheapest model that
clears the gate underneath. Your spend follows your typing. Objective order when they
conflict: correctness -> premium-token displacement -> wall-clock -> raw dollars.

**Effort (bracketed, Round 3):** run the orchestrator at `opus / high`. Above it,
xhigh over-thinks (+44% cost, zero correctness gain); below it, medium under-thinks
(correctness cracks at the wall and output INFLATES -- an under-thinking orchestrator
types more, not less). Workers: **the card is the quality mechanism; the model only
buys wall-clock** (20/20 floor cells, incl. haiku through a trap-dense cluster).
Write the card like quality depends on it -- it does. Pick the model like only speed
depends on it -- it does.

## 1 / Inventory (mandatory, before choosing anything)

Read the task and the spec/source. COUNT the real work -- do not estimate from the
prompt alone:

- **sites** -- individual edit/creation points (grep the call sites; list the stubs)
- **files** -- files you must create or modify
- **read volume** -- bytes of code/spec that must actually be read (`wc -c`, /4 ~ tokens)
- **nodes** -- discrete deliverables, labeled by RISK (not size):
  - CRITICAL -- shared contracts others import / auth/security / money math /
    concurrency / migrations / anything DESTRUCTIVE (sec 6)
  - WORKHORSE -- contained implementation against a clear spec / trap-dense edits
  - MUNDANE -- mechanical, fully specified, judgment-light

The site inventory is not scaffolding -- it is the gate's arithmetic (sec 4.7). Count it
like the grade depends on it.

## 2 / Scale gate (computed -- print the verdict, then obey it)

Print one line: `GATE: SOLO|SWARM -- sites=<n> files=<n> read~<n>K nodes=<n> mix=<C/W/M>`

**SWARM** if ANY of:
- sites >= 25, or files to create/modify >= 12
- nodes >= 12 AND >= 40% of them are MUNDANE+WORKHORSE (displacement value exists)
- read volume >= 150K tokens, or projected work >= 60% of the session's turn budget
- the human flagged premium-token pressure

**SOLO** otherwise -- that is the measured optimum below these lines, not laziness.
**Tiebreak:** when a count sits within one honest re-count of a line (e.g. 9 vs 10
deliverables), take SOLO -- below the wall the cheaper error is under-routing.

**Mid-run re-gate (the insurance the monolith lacks):** while SOLO, if you reach half
the turn budget with less than half the checklist done, or discovered sites exceed
1.5x your inventory, STOP -- write the plan (sec 4) for the REMAINDER and switch to SWARM.

## 3 / SOLO path

Do the work in-session with the discipline that survives the wall: write the full
checklist first (every site, `file:line`), execute in file-order batches, tick each
site off, re-grep after each batch to catch missed sites, then run the sec 5 gate.
Interactively, you may instead hand the whole job to ONE domain specialist when the
main context is precious -- brief per sec 4.4, same gate.

## 4 / SWARM path

### 4.1 Plan-as-data

Create a scratch dir OUTSIDE the repo (`mktemp -d`, or `%TEMP%\orch-<name>`). Write
`plan.json` there before any implementation:

```json
{"mode":"swarm","gate":"GATE line verbatim",
 "workers":[{"id":"W1","nodes":["N01"],"lane":"opus","files":["lib/log.js"],
             "deps":[],"spec":"SPEC.md sec 2.1-2.4","destructive":false}],
 "batches":[["W1","W2"],["W3"]],
 "gate_cmd":"<the sec 5 script>"}
```

A promoted worker names its trap (`"trap":"instance-method logEvent must not
change"`) -- promotion is data, not mood.

**Hook handshake (live installs only):** if this environment has the optional
enforcement hooks installed, declare the plan before any dispatch
(`python orch_declare.py --repo <repo> declare --plan <plan.json>`), `open` before
each batch, `close` after it lands, `clear` at handoff -- the lane floor/ceiling and
the mandate become denied tool calls instead of prose. No hooks installed -> skip
entirely; the protocol is fail-open and costs nothing headless.

NOTHING non-product is ever written inside the repo -- no plan, no scratch, no gate
script, no self-check artifacts. The repo receives product code only.

**Output diet (your tokens are the expensive ones):** plan.json <= ~40 lines; each
worker card <= ~12 lines beyond the shared preamble; reconciliation <= ~30 lines; gate
script focused (contracts + named traps + the counting sweep + one integration path,
<= ~150 lines) -- the per-worker CHECKs already covered the breadth. Do not restate
preamble content in cards; do not narrate between tool calls.

Present the plan (worker table + lanes + batches). If a human is present, pause for
approval; in auto-approve/headless mode print it and proceed (`PLAN-APPROVED: AUTO`).

### 4.2 Group into workers, collapse tiers

- **One worker per cohesive cluster** -- a subsystem/file family of ~3-8 sites or 1-3
  modules -- NOT one worker per graded requirement. Target 6-12 workers for a
  15-70-site job. Never two writers of the same file in the same batch.
- **Group WITHIN a lane, never across lanes.** Folding a MUNDANE node into a sonnet
  or opus worker silently up-lanes it -- that is where the haiku lane went in v4.0.
  A worker whose nodes are all MUNDANE runs on `haiku`; promoting it to sonnet
  requires a trap you can NAME in that worker's own files, named in plan.json.
- **Contract-pinned tier collapse:** a dependency whose interface is pinned by a
  normative spec (exact signatures, values, worked examples) is NOT a batch edge --
  downstream workers code against the pinned contract while the upstream is built in
  parallel. Only physically-shared prerequisites (foundation modules everyone imports,
  with no pinned spec) create a second batch. **The batch count is THE wall-clock
  lever** -- two correct plans measured 2x apart on it. Target ONE batch; only a
  physically-shared unpinned prerequisite justifies a second.

### 4.3 THE MANDATE (hard rule on this path -- the three excuses are pre-refuted)

- You do NOT implement. Every worker is dispatched via the `Agent` tool. "It's quicker
  to just do this one myself" is the defection the arena caught 28/28 times.
- "Spec fidelity" is preserved by the brief + the worker reading the spec FROM DISK --
  not by hoarding the work. "It fits in one context" is answered by the gate, which
  already said SWARM. "Per-node briefing cost" is answered by grouping (sec 4.2) and the
  shared preamble (sec 4.5).
- Dispatch every ready worker of a batch as parallel `Agent` calls in ONE message --
  all the tool calls in the SAME assistant turn (<= ~10 per message; split larger
  batches). **Spawning one worker, awaiting its result, then spawning the next is a
  mandate violation, not prudence** -- v4.0 did exactly that 10/10 times and turned
  the swarm into a relay race. There is nothing to check between same-batch spawns:
  landing checks (sec 4.6) run after the WHOLE batch has returned, never between spawns.
- Pass `model` EXPLICITLY on every spawn -- never inherit. Put the worker id + node ids
  in `description` (e.g. `"W3 N04-N07 mundane sweep"`) so routing is auditable.
- Your own turns are reserved for: inventory, the plan, briefs, reading reports,
  landing checks, the gate, escalations, reconciliation.

### 4.4 Lanes (rubric, decided once in the plan)

| lane | model | goes there |
|---|---|---|
| MUNDANE | `haiku` | mechanical + fully-ruled, WITH the exact rules and trap warnings in the card |
| WORKHORSE | `sonnet` | contained implementation; also trap-DENSE mundane clusters |
| CRITICAL | `opus` | shared unpinned contracts, auth, money, concurrency, destructive |

**Demotion (measured -- default OFF):** a CRITICAL node fully pinned by the spec MAY
run on `sonnet` (NEVER auth, money, concurrency, or destructive) -- but Round 3
priced it: ~10% cheaper, ~40% slower, because opus clears spec-pinned work in fewer
passes. Demote only when the node's output is large enough for the dollar gap to be
real; otherwise CRITICAL stays on opus -- faster AND safer. **Promotion (a speed
purchase):** a trap-dense mundane cluster runs on `sonnet` for wall-clock (2x haiku
at equal quality, floor-proven), trap named in plan.json; when wall-clock is not
pressing, haiku with the traps IN THE CARD holds at a third of the price.
`subagent_type: general-purpose` always works; a matching domain specialist
(or any domain subagent you have installed) is fine too -- the explicit `model` still governs.

### 4.5 Briefs (cache-shaped; pointers, not pastes)

Assemble ONE shared preamble, byte-identical across every spawn of the run (identical
prefixes are prompt-cache hits -- the swarm pays for it once):

```
Repo root = your working directory. SPEC.md is the binding contract -- READ the
sections named in your card FROM DISK; they are normative, never paraphrased here.
Global constraints: <the task's own rules: stdlib-only, no new files outside X, ...>
Self-check before reporting, with all scratch files OUTSIDE the repo (system temp).
Report EXACTLY:
STATUS: DONE | BLOCKED(<question>)
FILES: <touched>
CHECK: <command> -> <result, 1 line>
NOTES: <=3 lines
If any instruction cannot be applied exactly as written: STATUS: BLOCKED. Never guess.
```

Then a per-worker card: worker id / OWNED files (exact list -- touch nothing else) /
spec sections BY REFERENCE / the byte-exact rules and trap warnings that bite (these
are the only pasted lines -- error templates, orderings, "must NOT change" items) /
upstream state ("fieldops/contracts.py is FINAL on disk -- import it, never modify") /
done-looks-like / the self-check command to run.

### 4.6 Landing protocol (reports are claims)

After the WHOLE batch returns (all spawns of the dispatch message -- never between
spawns): run `git status --porcelain` + `git diff --name-only` -- any
changed file outside the union of dispatched OWNED lists is reverted and the owner
re-briefed. Spot-check each worker with its own CHECK command or a 1-line import/run
probe. A BLOCKED report gets an answer (from spec/plan), then a fresh spawn, same lane.
Never accept a green self-report as the gate -- in the arena a correct diff arrived
under a wrong report, and only the script told the truth.

### 4.7 The gate (orchestrator-owned, deterministic -- and it COUNTS)

Write your OWN gate script in the scratch dir -- worked examples from the spec made
executable, one end-to-end integration path, the anti-regression traps ("must not
change" items verified verbatim), and the scope sweep. **The counting sweep is
mandatory:** grep the repo for every legacy pattern (expect exactly 0 outside the
spec's allowed survivals) AND count new-pattern occurrences against the sec 1 site
inventory (expect exact N). A missed site cannot pass a counting gate -- the one
observed gate escape slipped a judgment check; it cannot slip arithmetic. Exit code
decides. Non-zero blocks: fix via sec 4.8 and re-run. LLM review is optional and never
substitutes.

### 4.8 Escalation ladder (evidence travels, work doesn't restart)

Per failing worker: (1) fresh spawn, SAME lane, with the gate failure + current diff
of its owned files pasted in; (2) one lane up (haiku->sonnet->opus), same evidence;
(3) `LADDER_EXHAUSTED` -- you repair the minimal failing diff in-session and log it in
reconciliation. Hard cap: 3 attempts per worker, then stop and report to the human.

## 5 / SOLO gate

Same as sec 4.7 -- the script (counting sweep included), not your eyes, decides done.
Run it before declaring.

## 6 / Destructive interlock

DESTRUCTIVE = schema/data migrations, data deletion or movement, git history rewrites
or force-push, deploy/infra mutation, secret or auth-provider changes -- anything
irreversible outside the working tree. Rules, regardless of path:
- never routed below `opus`; the worker returns PLAN + exact commands + diff +
  rollback -- it does not execute;
- you verify the rollback actually restores state before presenting;
- a live human approves execution. In auto-approve/headless mode the irreversible
  step is NOT executed: mark it `DEFERRED-DESTRUCTIVE` with the ready-to-run plan.

## 7 / Reconcile & hand off

- Requirement matrix: every spec item -> IMPLEMENTED / PARTIAL / DEFERRED /
  SCOPE-CREEP, with file refs.
- Routing table: planned vs ACTUAL spawns (worker / lane / model / attempts) + any
  `LADDER_EXHAUSTED` / `DEFERRED-DESTRUCTIVE` events. Planned!=actual must be explained.
- Gate evidence: the script's final output tail, counting sweep included.
- Commit only with human approval; in auto-approve mode leave the tree uncommitted.

## Invariants

- Only top-level sessions hold the `Agent` tool -- never expect a worker to fan out,
  never delegate orchestration itself.
- One writer per file per batch. Specs are read from disk by whoever implements.
- Worker reports are claims; the gate is the only evidence -- and the gate counts.
- Nothing non-product inside the repo, ever.
- Max 3 attempts per worker; the human is the fourth tier.
