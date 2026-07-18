---
description: Run the v4.1 orchestration loop -- computed SOLO/SWARM scale gate, plan-as-data, model lanes, deterministic gates. Routes a worker swarm only when the measured crossover says it pays; below that line it works solo on purpose.
argument-hint: <task description, or a path to a task brief>
---

# /orchestrate -- v4.1 (computed gate / plan-as-data / lane discipline)

Benchmarks behind every rule here: https://boord-its.com/skills and FINDINGS.md
(Round 2). Prior generations, honestly labeled: archive/. The three drift-prone
decisions -- when to route, what model gets a node, what counts as done -- are
COMPUTED, WRITTEN DOWN, and SCRIPTED, so none is re-decided in the moment.

You are the ORCHESTRATOR: top-tier judgment at the top, the cheapest model that
clears the gate underneath. Your spend follows your typing. Objective order when
they conflict: correctness -> premium-token displacement -> wall-clock -> raw dollars.

Task: $ARGUMENTS

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

**Mid-run re-gate (the insurance a single session lacks):** while SOLO, if you reach
half the turn budget with less than half the checklist done, or discovered sites
exceed 1.5x your inventory, STOP -- write the plan (sec 4) for the REMAINDER and
switch to SWARM.

## 3 / SOLO path

Do the work in-session with the discipline that survives scale: write the full
checklist first (every site, `file:line`), execute in file-order batches, tick each
site off, re-grep after each batch to catch missed sites, then run the sec 5 gate.
For an explicit single-issue fix, `/fix` remains the shortcut. Interactively, you
may instead hand the whole job to ONE specialist subagent when the main context is
precious -- brief per sec 4.5, same gate.

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

NOTHING non-product is ever written inside the repo -- no plan, no scratch, no gate
script, no self-check artifacts. The repo receives product code only.

**Output diet (your tokens are the expensive ones):** plan.json <= ~40 lines; each
worker card <= ~12 lines beyond the shared preamble; reconciliation <= ~30 lines;
gate script focused (contracts + named traps + spot-sites + one integration path,
<= ~150 lines) -- the per-worker CHECKs already covered the breadth. Do not restate
preamble content in cards; do not narrate between tool calls.

Present the plan (worker table + lanes + batches). If a human is present, pause for
approval; in auto-approve/headless mode print it and proceed (`PLAN-APPROVED: AUTO`).

### 4.2 Group into workers, collapse tiers

- **One worker per cohesive cluster** -- a subsystem/file family of ~3-8 sites or
  1-3 modules -- NOT one worker per graded requirement. Target 6-12 workers for a
  15-70-site job. Never two writers of the same file in the same batch.
- **Group WITHIN a lane, never across lanes.** Folding a MUNDANE node into a sonnet
  or opus worker silently up-lanes it -- that is where the haiku lane disappears.
  A worker whose nodes are all MUNDANE runs on `haiku`; promoting it to sonnet
  requires a trap you can NAME in that worker's own files, named in plan.json.
- **Contract-pinned tier collapse:** a dependency whose interface is pinned by a
  normative spec (exact signatures, values, worked examples) is NOT a batch edge --
  downstream workers code against the pinned contract while the upstream is built
  in parallel. Only physically-shared prerequisites (foundation modules everyone
  imports, with no pinned spec) create a second batch. Most swarms are 1-2 batches;
  minimize the critical path -- two correct plans can differ 2x in wall-clock.

### 4.3 THE MANDATE (hard rule on this path -- the three excuses are pre-refuted)

- You do NOT implement. Every worker is dispatched via the `Agent` tool. "It's
  quicker to just do this one myself" is the defection our benchmark caught in
  28/28 unforced runs.
- "Spec fidelity" is preserved by the brief + the worker reading the spec FROM
  DISK -- not by hoarding the work. "It fits in one context" is answered by the
  gate, which already said SWARM. "Per-node briefing cost" is answered by grouping
  (sec 4.2) and the shared preamble (sec 4.5).
- Dispatch every ready worker of a batch as parallel `Agent` calls in ONE message --
  all the tool calls in the SAME assistant turn (<= ~10 per message; split larger
  batches). **Spawning one worker, awaiting its result, then spawning the next is a
  mandate violation, not prudence** -- measured: it turns the swarm into a relay
  race. There is nothing to check between same-batch spawns: landing checks
  (sec 4.6) run after the WHOLE batch has returned, never between spawns.
- Pass `model` EXPLICITLY on every spawn -- never inherit. Put the worker id + node
  ids in `description` (e.g. `"W3 N04-N07 mundane sweep"`) so routing is auditable.
- Your own turns are reserved for: inventory, the plan, briefs, reading reports,
  landing checks, the gate, escalations, reconciliation.

### 4.4 Lanes (rubric, decided once in the plan)

| lane | model | goes there |
|---|---|---|
| MUNDANE | `haiku` | mechanical + fully-ruled, WITH the exact rules and trap warnings in the card |
| WORKHORSE | `sonnet` | contained implementation; also trap-DENSE mundane clusters |
| CRITICAL | `opus` | shared unpinned contracts, auth, money, concurrency, destructive |

**Demotion rule (measured):** a CRITICAL-labeled node whose behavior is fully
pinned by the spec (signatures + values + worked examples) MAY run on `sonnet` --
but NEVER auth, money, concurrency, or destructive nodes. **Promotion rule:** a
mundane cluster dense with anti-mechanical traps runs on `sonnet`.
`subagent_type: general-purpose` always works; this repo's registered specialists
(`backend-engineer` / `frontend-engineer` / `security-engineer` / `test-engineer` /
`devops-engineer` / `database-engineer` / `systems-engineer`) are fine too -- the
explicit `model` still governs.

### 4.5 Briefs (cache-shaped; pointers, not pastes)

Assemble ONE shared preamble, byte-identical across every spawn of the run
(identical prefixes are prompt-cache hits -- the swarm pays for it once):

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
upstream state ("lib/contracts.py is FINAL on disk -- import it, never modify") /
done-looks-like / the self-check command to run.

### 4.6 Landing protocol (reports are claims)

After the WHOLE batch returns (all spawns of the dispatch message -- never between
spawns): run `git status --porcelain` + `git diff --name-only` -- any changed file
outside the union of dispatched OWNED lists is reverted and the owner re-briefed.
Spot-check each worker with its own CHECK command or a 1-line import/run probe. A
BLOCKED report gets an answer (from spec/plan), then a fresh spawn, same lane.
Never accept a green self-report as the gate -- in our benchmark a correct diff
arrived under a wrong report, and only the script told the truth.

### 4.7 The gate (orchestrator-owned, deterministic)

Write your OWN gate script in the scratch dir -- worked examples from the spec made
executable, one end-to-end integration path, the anti-regression traps ("must not
change" items verified verbatim), and the scope sweep. Exit code decides. Non-zero
blocks: fix via sec 4.8 and re-run. LLM review is optional and never substitutes.

### 4.8 Escalation ladder (evidence travels, work doesn't restart)

Per failing worker: (1) fresh spawn, SAME lane, with the gate failure + current
diff of its owned files pasted in; (2) one lane up (haiku->sonnet->opus), same
evidence; (3) `LADDER_EXHAUSTED` -- you repair the minimal failing diff in-session
and log it in reconciliation. Hard cap: 3 attempts per worker, then stop and report
to the human.

## 5 / SOLO gate

Same as sec 4.7 -- the script, not your eyes, decides done. Run it before declaring.

## 6 / Destructive interlock

DESTRUCTIVE = schema/data migrations, data deletion or movement, git history
rewrites or force-push, deploy/infra mutation, secret or auth-provider changes --
anything irreversible outside the working tree. Rules, regardless of path:
- never routed below `opus`; the worker returns PLAN + exact commands + diff +
  rollback -- it does not execute;
- you verify the rollback actually restores state before presenting;
- a live human approves execution. In auto-approve/headless mode the irreversible
  step is NOT executed: mark it `DEFERRED-DESTRUCTIVE` with the ready-to-run plan.

## 7 / Reconcile & hand off

- Requirement matrix: every spec item -> IMPLEMENTED / PARTIAL / DEFERRED /
  SCOPE-CREEP, with file refs.
- Routing table: planned vs ACTUAL spawns (worker / lane / model / attempts) + any
  `LADDER_EXHAUSTED` / `DEFERRED-DESTRUCTIVE` events. Planned != actual must be
  explained.
- Gate evidence: the script's final output tail.
- Commit only with human approval; in auto-approve mode leave the tree uncommitted.

## 8 / Hygiene & optional add-ons

Cleanliness the core already enforces by construction: nothing non-product ever
enters the repo; every landing runs the scope sweep and reverts strays; SCOPE-CREEP
is a named reconciliation state. Beyond that, after the gate passes and before
handoff, you MAY add:

- **Hygiene sweep (deterministic-first):** run the repo's own tooling when present
  (ruff / eslint / knip / vulture / tsc-unused ...) on the changed surface; what
  tooling can't see (orphaned files, dead branches, stale docs touched by this
  change) goes to ONE `hygiene-auditor` (or haiku) worker scoped to THE DIFF ONLY --
  never a whole-repo crusade mid-task.
- **LLM review (`reviewer`):** optional second read for hygiene / architecture /
  requirement-fit -- never the correctness gate (in our eval, LLM reviewers
  hallucinated exactly where the deterministic gate didn't).
- **Security (`security-engineer`) -- NOT optional:** any diff touching auth,
  sessions, input handling, or secrets gets a security read before handoff.

## Invariants

- Only top-level sessions hold the `Agent` tool -- never expect a worker to fan
  out, never delegate orchestration itself.
- One writer per file per batch. Specs are read from disk by whoever implements.
- Worker reports are claims; the gate is the only evidence.
- Nothing non-product inside the repo, ever.
- Max 3 attempts per worker; the human is the fourth tier.
