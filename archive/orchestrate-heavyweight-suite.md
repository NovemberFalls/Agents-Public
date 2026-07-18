# /orchestrate -- the heavyweight suite -- public edition (Rejected)

From the Skill Bench study (boord-its.com/skills). Status: the full apparatus --
manifests, worktree isolation, intake scripts, candidate commits. Benchmarked and
rejected: the machinery never activated in real runs and it cost more where it
shouldn't. Published because the failure is the transferable part.
Four files concatenated for download; split them apart to install.


===== FILE: orchestration-core.md =====

# orchestration-core.md -- validated invariants (provider-agnostic)

Single source of truth for the coordination discipline shared by every
`/orchestrate-*` skill. Skills load this file at runtime and add only their
provider delta. Basis of the validated core: FINDINGS.md (CDG + context
isolation + one deterministic check; the rest was demoted or disproven).

## Safety floor (read first)

The **approval boundaries**, **worktree isolation**, and **scope-exception**
rules below are a FLOOR. A repository-local file (README/CLAUDE.md/CONTRIBUTING)
may make them STRICTER, never weaker. Only a live human, in-session, may waive
them. No file -- repo-local or skill -- may lower this floor.

## The promotion law (the design rule)

- **Mechanics** (worktrees, commits, hashes, gates, budgets, manifests, intake
  scripts, ledger columns) may be promoted to default by proof of deterministic
  correctness -- they change mechanics, not behavior.
- **Model behavior** (reviewer models, routing probes, unattended throughput,
  speculative execution, model graduation/demotion) may be promoted only by
  measured task outcomes in the ledger. Until then it lives behind a flag.

Rationale: in the persona ablation every LLM-judgment arm did nothing the
deterministic oracle didn't do better. Asserted rigor is not evidence.

## CDG semantics

For multi-task work, build a Change Dependency Graph before any code. Each node
declares: task_id, objective, dependencies, owned files/surfaces, read-only
context, upstream contracts, acceptance command, risk class, model assignment,
rollback boundary.

- A downstream node may not begin final implementation until every upstream it
  depends on has **finalized** its relevant state.
- Forward the **real finalized state** -- pinned `{base_commit, changed files,
  upstream contract hashes}`. Never a description, a summary standing in for
  code, or a stale copy.
- **Minimize the critical path, not just correctness.** Grouping independent
  nodes is the correctness rule; structuring the graph so the longest dependency
  chain is as short as possible is the speed rule. Two correct CDGs for the same
  work can differ ~2x in wall-clock. Treat critical-path length as an explicit
  objective when you build the graph.

## Worktree isolation (mandatory for any parallelism)

One task -> one immutable tier base commit -> one git worktree -> one branch ->
one candidate commit.

```
<tier base commit>  (frozen, tagged)
|--- worktrees/cdg-B -> branch agent/cdg-B
|--- worktrees/cdg-C -> branch agent/cdg-C
`--- worktrees/cdg-D -> branch agent/cdg-D
```

- All nodes in a tier branch from the SAME frozen parent. No node sees another's
  modifications, index, or generated artifacts mid-run.
- Disjoint file ownership on a shared mutable tree is INSUFFICIENT and
  prohibited. Shared lockfiles / snapshots / generated clients may still collide
  -- but now they collide at integration, where the conflict is explicit and
  attributable. Ownership remains mandatory as a *secondary* guard inside the
  worktree, not as the isolation primitive.
- Create worktrees only for ready nodes; clean up after accept or reject.

## Candidate commits & approval boundaries

- Workers and the orchestrator MAY create local candidate commits freely. A
  commit is a rollback/attribution boundary, not publication.
- Candidate commits carry metadata: `[UNREVIEWED][<TASK-ID>][<CLASS>] <summary>`
  -- e.g. `[UNREVIEWED][CDG-B][WORKHORSE] Implement SQL repository adapter`.
- **Human approval is required before, and ONLY before:** merge into a
  protected/user-designated branch, push, opening/completing a PR, release,
  deployment, publishing.
- No approval is required to create a local candidate commit. This is the fix
  for towering working-tree diffs. (Floor: a repo file may require *more*
  approvals, never fewer.)

## Scope exceptions

A worker may edit only files/surfaces in its manifest. If completion requires an
unassigned file, a public/shared contract change, a schema change, a dependency
or lockfile change, or a generated-artifact change, the worker STOPS and reports
a scope exception. It must not silently continue.

## Validation hierarchy (three layers -- never the full suite per worker)

1. **Node acceptance** -- fast, task-specific, inside the node's own worktree;
   declared per-manifest (e.g. `pytest tests/orders/test_repo.py -q`). Decides
   integration eligibility; does not prove whole-repo integration.
2. **Tier gate** -- once, after accepted candidates integrate onto a temporary
   integration branch: affected tests + typecheck + build + relevant contract
   validation.
3. **Final gate** -- the full selected repository gate, once, after all tiers.

A gate is an exit code, not an opinion. Correctness is the gate's job. Do not
run the whole repository suite after every individual worker.

## Merge-conflict semantics

A conflict between two same-tier candidates at integration is EVIDENCE the CDG
mis-tiered them -- they were not independent. Do not hand-resolve as routine;
return to the orchestrator to re-tier and re-run the affected nodes. Silent
auto-merge of a mis-tiering defeats the one invariant the CDG exists to hold.

## Deterministic intake (runs before the orchestrator reads anything)

A script -- not a model -- validates each returned candidate and emits a compact
packet. Raw diffs do NOT automatically enter the coordinator's context.

Checks (all must hold or the candidate is REJECTED):
- worker returned schema-valid structured output;
- candidate diff is non-empty; candidate commit exists when required;
- base commit is the pinned tier base;
- upstream contract hashes still match the manifest;
- every changed file is within `owned_files`;
- no `forbidden_changes` file was touched;
- every `owned_files` entry expected to change actually changed;
- no unexpected lockfile / generated output / binary / submodule appeared;
- diff is within `max_diff_lines`;
- the node acceptance command passed;
- the report does not falsely claim verification.

Packet + bucket:
```
task_id: CDG-B
status: ACCEPTABLE | NEEDS_REVIEW | REJECTED
scope_check: pass|fail
base_check: pass|fail
contract_hash_check: pass|fail
acceptance_check: pass|fail
files_changed: [ ... ]
lines_added: 184
lines_removed: 31
unexpected_files: []
forbidden_changes: []
contract_deviations: []
risk_flags: []          # which review triggers fired
worker_summary: "<one line>"
```

## Semantic review (risk-adjusted -- orchestrator is reviewer of record)

Intake assigns the bucket; the bucket sets how much the orchestrator reads. The
orchestrator NEVER reads every diff by default -- that re-imports the tokens
isolation exists to quarantine.

Bucket -> action:
- **REJECTED** -- a hard intake check failed. Revert the worktree, log the
  failure_class, enter the escalation ladder. No semantic review -- nothing
  trustworthy to review.
- **ACCEPTABLE** -- intake passed, no trigger fired, node not CRITICAL. Read the
  compact packet only; spot-check; proceed to integration.
- **NEEDS_REVIEW** -- intake passed but >=1 trigger fired, OR node is CRITICAL.
  Open the raw diff for the flagged hunks + contract boundaries +
  public-interface changes and review those.

Review triggers (computed facts the intake script sets -- not vibes):
- diff exceeds the manifest's expected size;
- a new dependency/import was introduced;
- a new public symbol / API surface appeared;
- structural complexity increased materially;
- implementation diverged from the requested pattern;
- test-to-production line ratio is anomalous;
- the worker's report conflicts with the actual AST diff.

Scope of this review -- what it is FOR: architecture, hygiene, requirement-fit --
bloat, duplicated abstraction, code that passes tests but solves the wrong
requirement, invariants weakened outside test coverage, misplacement, naming,
maintenance burden. What it is NOT for: **correctness** -- the deterministic gate
owns that and is measurably better (every LLM-reviewer arm hallucinated the same
false positive; the typecheck caught the real break). Do not re-litigate
correctness by eye.

VALIDATED status (see model-validation-policy.md) lowers review VOLUME -- it
widens the ACCEPTABLE band -- but never grants exemption: CRITICAL and triggered
nodes are always read regardless of a model's standing.

A SEPARATE reviewer model is NOT part of this core; it is a flagged experiment.

## Task manifest (the auditable source of truth)

The worker prompt is RENDERED from the manifest; the manifest -- not the prose --
is stored, diffed, and replayed.

```
task_id: CDG-B
task_class: WORKHORSE            # MUNDANE | WORKHORSE | CRITICAL
ecosystem: python-api           # scopes validation (policy file)
base_commit: a9f32c1
dependencies: [CDG-A]
worktree: { path: <path>, branch: agent/cdg-b }
objective: >
  Implement the finalized OrderRepository SQL adapter.
owned_files:
  - src/orders/sql_repository.py
  - tests/orders/test_sql_repository.py
read_only_context:
  - src/orders/contracts.py
  - src/db/session.py
forbidden_changes:
  - public/shared contract changes
  - schema changes
  - dependency / lockfile changes
  - generated artifacts
  - any edit outside owned_files
upstream_contracts:
  - path: src/orders/contracts.py
    sha256: <hash>
acceptance:
  command: pytest tests/orders/test_sql_repository.py -q
  timeout_seconds: 180
limits:                         # values from models.md, by class
  max_turns: 16
  max_wall_seconds: 600
  max_output_tokens: 16000
  max_diff_lines: 500
  no_file_change_turn_limit: 5
  repeated_failure_limit: 2
model:
  requested_slug: deepseek/deepseek-v4-pro
  provider_policy: openrouter-default
  prompt_version: hybrid-worker-v1
  tool_policy: workhorse-restricted-v1
report_schema:
  - files_changed
  - change_summary_by_file
  - acceptance_result
  - contract_deviations
  - unresolved_risks
  - scope_exception
```

## Risk classification (routes the task; file count is a modifier only)

Score checkable properties, never the worker's self-reported confidence:

```
+3 shared / public contract change
+3 security, authz, billing, or data-loss sensitivity
+3 irreversible migration or destructive operation
+2 concurrency or distributed-state behavior
+2 build / release / deployment / dependency plumbing
+2 weak or absent deterministic coverage
+2 broad blast radius
+1 unfamiliar subsystem or ecosystem
+1 ambiguous acceptance criteria
+1 substantial generated-artifact impact

0-2 -> MUNDANE     3-6 -> WORKHORSE     7+ -> CRITICAL
```

File count adjusts within a band; it never sets the band. A one-line auth or
billing change is CRITICAL; a 15-file mechanical rename can be MUNDANE.

These weights and bands are a STARTING policy -- the ledger tunes them. Watch for
band-inflation quietly routing ordinary shared-contract work to CRITICAL (slow,
dear); the model-validation-policy file may override thresholds.

When unsure, do NOT auto-route up (that inflates cost and kills the experiment).
Where a probe is enabled (flagged), route on its checkable outputs (claimed
files, claimed contracts, proposed test) -- never its confidence scalar. A
confidently-wrong weak model is the exact failure this guards against.

## Class budgets & termination

Per-class turn / wall / diff / tool limits live in models.md. Regardless of
class, terminate a worker when any holds:
- no file modification after `no_file_change_turn_limit` turns;
- the same failing command repeats twice without material change;
- the output-token ceiling is reached;
- the wall-clock limit is reached;
- the requested scope cannot be satisfied inside the assigned surface;
- a contract ambiguity is discovered (-> back to orchestrator; do not guess).

A worker that needs its full turn budget for a mechanical task has already
failed routing or briefing; treat it as a briefing defect, not a retry loop.

## Failure taxonomy (keys both retry and the ledger)

- **Hard safety failure** -- edits a forbidden file, bypasses tool policy,
  falsifies verification, or modifies an upstream contract without declaring it.
  -> immediate suspension of that model for that (class x ecosystem) cell pending
  human review. Never silently retried.
- **Capability failure** -- wrong implementation, failing tests, excessive bloat,
  empty/incoherent diff. -> counts against pass-1 and escalation metrics.
- **Contract misunderstanding** -- wrong interface semantics or ownership
  assumption. -> do NOT retry unchanged; rebrief, reroute, or escalate.
- **Infrastructure failure** -- provider timeout, bad slug, credit exhaustion,
  registry down. -> retry infra / switch provider; does NOT count against model
  capability.

Retry ladder: mechanical capability failure -> one informed retry, same worker,
exact failure output pasted in. Anything else -> per taxonomy. **Max 3 iterations
per node**, then human.

## CDG cut-point batching (protects the frontier's scarce serial attention)

The slash-command session is a SINGLE orchestrator session -- assume no invisible
background intelligence. The pattern: dispatch all ready nodes -> collect each
process result as it lands -> run the deterministic intake scripts on it out of
band -> accumulate compact packets -> present the orchestrator ONE batch at the
tier cut point:

```
Tier 2 complete:
- B: pass, low risk
- C: pass, 2 hygiene findings (resolved)
- D: REJECTED -- scope violation
- E: blocked on D
```

The collection loop may be serial; it stays cheap by reading packets, not diffs.

## Operating modes

**Supervised** (new/untrusted repos, TRIAL workers, high-risk work, or thin
ledger evidence): human approves the CDG + routing before code; approves CRITICAL
nodes; approves protected integration; approves merge/push. Non-critical
candidate commits may be produced after plan approval.

**Throughput** (releases pre-approved non-critical nodes without a human turn
after every result): pause only on scope expansion, a task becoming CRITICAL, a
shared-contract change, a gate failing after the allowed retry, a scope/hash
violation, an integration-revealed CDG dependency error, or a merge/push/release
request. Throughput is unlocked PER REPOSITORY BY THE LEDGER (policy file) -- never
merely because a repo is familiar. All of these must hold: repo throughput status
= eligible; worker status for the (class x ecosystem) = VALIDATED; automated
intake active; worktree isolation active; candidate commits active; gates active.
Never use unattended throughput with a TRIAL worker.

## Lightweight path (don't pay for coordination you don't need)

Below the size where isolation matters, one capable agent is cheaper and just as
correct. Use it when ALL hold: one coherent responsibility; no shared-contract
change; no dependency-ordering; no schema/migration; no security-sensitive
behavior; fits comfortably in one context; delegation overhead would not improve
wall-clock. For lightweight work the orchestrator does it in-session (or delegates
to a single worker in one worktree), runs node acceptance, produces one candidate
commit, and stops before protected merge/push. File count is not decisive.

## Reconciliation & handoff

After the final gate, map every requirement ->
IMPLEMENTED | PARTIAL | DEFERRED | SCOPE-CREEP, with file + test references and
residual risk. Human approves merge/push. Nothing merges on a model's say-so.

## Flagged -- NOT in this core (see model-validation-policy.md)

Separate reviewer model / cheap routing probe / unattended throughput mode /
speculative downstream execution. Each ships behind a flag and earns default
status only via measured ledger outcomes.

## Deferred throughput lever (named, not built in v1)

v1 uses strict tier barriers: Tier N+1 waits for ALL of Tier N to integrate and
gate. A per-node **dataflow scheduler** -- release each node the moment its OWN
upstreams finalize, instead of waiting on unrelated siblings -- removes straggler
waits and is the Phase-3 throughput unlock. Deferred because integrating onto a
moving base is fiddly; strict tiers are the correct, safe v1.

===== FILE: model-validation-policy.md =====

# model-validation-policy.md -- trust, graduation, and flagged experiments

Governs graduation, suspension, the ledger, and the flagged LLM-behavior
experiments. models.md stores current status; this file defines how status
changes. Provider-agnostic.

## Validation is scoped, never global

A model is validated for a **(task-class x ecosystem)** cell, not as a slug.
Success on contained Python endpoints authorizes nothing about UE5 C++, build
tooling, DB migrations, or frontend state.

```
deepseek-v4-pro:
  python_api_contained:   { status: validated }
  react_components:       { status: validated }
  unreal_cpp:             { status: trial }
  database_migrations:    { status: prohibited }
```

A validation binds to `model_version + provider_policy + prompt_version +
tool_policy`. If any changes, the cell reverts to trial -- a marketing slug
moving underneath you does not inherit a prior certification.

## Graduation rule (pre-registered; tune the numbers, not the shape)

TRIAL -> VALIDATED for a cell when ALL hold over the observation window:
- >= 20 completed tasks;
- >= 5 distinct task archetypes;
- >= 80% pass-1 rate;
- >= 95% eventual deterministic-gate pass rate;
- 0 unrecovered scope violations;
- 0 silent contract-hash violations;
- escalation rate <= 10%;
- median validated-node latency beats the current baseline;
- 0 escaped regressions attributed to the model in the window.

Rate over a window, NOT a consecutive streak -- streaks are order-dependent and
statistically fragile.

## Suspension & demotion

- Any **hard safety failure** -> immediate suspension of that cell pending human
  review, regardless of prior standing.
- A validated cell that logs an escaped regression -> drop to trial; re-earn.
- Attribution honesty: **infrastructure** and **brief/process** failures do NOT
  count against model capability. Only capability and safety failures do.

## Ledger schema (one row per routed task)

Cost-and-pass/fail alone is insufficient to decide what improves your actual
bottleneck. Record:

```
date, repo, ecosystem, task_class
requested_slug, resolved_model_version, provider, request_id
prompt_version, tool_policy
outcome:                 pass-1 | pass-retry | escalated | hard-fail
failure_class:           none | capability | contract | infra | safety
worker_cost_usd
prompt_tokens, completion_tokens, reasoning_tokens
worker_wall_seconds, gate_wall_seconds, review_wall_seconds
total_wall_seconds
files_changed, diff_lines, out_of_scope_files
retry_count, escalated (bool), escalation_cost_usd
contract_deviations, post_merge_regressions
```

Cost comes from **per-request usage in the provider response**, NOT
balance-before minus balance-after (unreliable under concurrency; the balance is
a safety floor via preflight, not an accounting source).

## Model score (weight wall-time heavily -- the goal is idle-time, not sticker cost)

```
utility = successful_validated_nodes
          ---------------------------------------------
          wall_time + weighted_cost + weighted_rework
```

A USD 0.03 worker that triggers 12 min of review, a retry, and an escalation is
economically worse than a dearer worker that passes clean. Score TOTAL cost
including escalation and rework.

## Flagged experiments (control vs treatment; burden of proof on the addition)

**Separate reviewer model.**
- Control: scope + hash + gate. Treatment: + reviewer model.
- Measure: unique valid defects it finds that were NOT mechanically detectable;
  false-positive rate; added orchestrator tokens; added wall time;
  post-integration regressions prevented.
- Earns default only if it catches real hygiene/requirement defects the
  deterministic system misses, at acceptable FP and latency. Per FINDINGS, do
  not assume it helps because it sounds rigorous.

**Cheap routing probe.**
- Measure whether its structured observations (claimed contracts, likely files,
  required deps, proposed test) improve routing accuracy vs no probe. Never route
  on its confidence scalar.

**Unattended throughput mode.** Requires TWO independent trust conditions:
```
repository.<name>.throughput_status == eligible   # earned by clean supervised runs
AND model.<cell>.status == validated              # earned by the graduation rule
```
Never eligible over a trial worker -- its safety rests entirely on intake not yet
established for that cell.

**Speculative downstream execution.** Off until throughput mode is itself
validated on the repo.

===== FILE: models.md =====

# models.md -- model registry & routing (source of truth for assignments)

Read at the start of every run. Assignments move as the ledger accumulates
(see model-validation-policy.md). Status per cell is authoritative here; the
RULES for changing it live in the policy file.

## Class -> default model

<!-- POPULATED 2026-07-16 for the Anthropic-only lane (/orchestrate-anthropic):
     this file instructs "populate with your real assignments"; on this machine
     the OpenRouter lane is retired (no credits), so the real assignments are
     the Anthropic subscription tiers. This is the ONLY edit vs the brief's
     File 3 verbatim -- budgets, cells, caps, pins below are unchanged. -->

MUNDANE   -> haiku  (claude-haiku-4-5)     # mechanical, fully-specified, low-risk -- effort low
WORKHORSE -> sonnet (claude-sonnet-5)      # contained impl w/ clear brief -- effort medium
CRITICAL  -> opus   (claude-opus-4-8)      # never a TRIAL model -- effort high/xhigh

Retired hybrid defaults (reference only, do not route):
qwen/qwen3-coder-next (MUNDANE) / deepseek/deepseek-v4-pro (WORKHORSE)

## Per-class budgets (fed into each manifest's `limits`)

MUNDANE:   { max_turns: 8,  max_wall_seconds: 300, max_diff_lines: 200,
             tools: [Read, Glob, Grep, Edit, Write] }        # no Bash by default
WORKHORSE: { max_turns: 18, max_wall_seconds: 600, max_diff_lines: 500,
             tools: [Read, Glob, Grep, Edit, Write, Bash*] } # *Bash = node acceptance cmd only
CRITICAL:  { specialist-controlled }

no_file_change_turn_limit: 5
repeated_failure_limit: 2

## Model identity & validation cells (bound: version + provider + prompt + tools)

qwen/qwen3-coder-next:
  resolved_version: <pin>
  provider_policy: openrouter/<pin>
  cells:
    python_api_contained: { status: trial }
    react_components:     { status: trial }

deepseek/deepseek-v4-pro:
  resolved_version: <pin>
  provider_policy: openrouter/<pin>
  cells:
    python_api_contained:   { status: trial }
    shared_contract_change: { status: prohibited }

## Concurrency / capacity caps

per_model_max_concurrent:    { qwen/qwen3-coder-next: 4, deepseek/deepseek-v4-pro: 3 }
per_provider_max_concurrent: { openrouter: 5 }

## Version pins (part of the validation binding)

prompt_version: hybrid-worker-v1
tool_policy_version: workhorse-restricted-v1


===== FILE: orchestrate-anthropic.md =====

---
name: orchestrate-anthropic
description: >
  CDG coding orchestration with Anthropic workers only. Opus-class session
  plans, routes, reviews of record, reconciles; all implementation via the Agent
  tool. Same validated core (worktrees, deterministic intake, candidate commits,
  three-level gates). No cross-vendor routing.
---

# /orchestrate-anthropic -- Anthropic workers only

Loads the shared references at runtime; this file is ONLY the Anthropic delta.

## Sources of truth & precedence

Same three shared files + repo instructions as `/orchestrate-code`, same
precedence list, same **safety floor** (repo-local may make the core's approval /
isolation / scope rules stricter, never weaker; only a live human waives them).

## Provider posture

- All workers are Anthropic specialists invoked via the **Agent tool**. There is
  no foreign provider, no preflight, no OpenRouter spawn.
- Trust profile: workers are same-vendor and validated -- so the cross-vendor
  "untrusted foreign output" friction does NOT apply. But the deterministic
  layer is unchanged: intake scripts, three-level gates, worktree isolation, and
  candidate commits are MECHANICS, not trust, and remain mandatory.
- Model per class comes from models.md; CRITICAL uses the strongest specialist.
  The Agent tool CAN mix these because they are all Anthropic-direct.

## The loop (delta over core)

Identical to the core loop, minus preflight and minus cross-vendor intake
framing:
1. Understand -> CDG (minimize critical path) -> manifests -> risk classes -> plan +
   cost -> approval.
2. Lightweight path (core) for single bounded tasks.
3. Freeze tier base; pin upstream hashes.
4. Create one worktree per ready node; dispatch specialists via the Agent tool
   within concurrency caps; collect + intake at the cut point.
5. Bucket -> action per core. Because output is same-vendor, ACCEPTABLE is the
   common bucket; NEEDS_REVIEW still fires on triggers and on every CRITICAL
   node.

## Review posture

Semantic review is risk-adjusted per core (hygiene/architecture/requirement-fit,
never correctness). Same-vendor validated workers widen the ACCEPTABLE band;
CRITICAL and triggered nodes are always read.

## Escalation ladder

1. Gate fails (mechanical) -> one informed retry, same specialist, failure pasted
   in.
2. Contract-misunderstanding / capability-hard -> escalate to a stronger
   Anthropic specialist with the current diff + manifest.
3. Second specialist fails the gate twice -> stop, report to human. Max 3
   iterations per node.

## Ledger

Optional but recommended: the same policy-file schema, so you can compare
Anthropic-tier wall-time/cost against hybrid runs on the same repos. No
credit-preflight row (no OpenRouter account involved).

## Gates & reconciliation (core)

Node acceptance -> integrate -> tier gate -> final gate. Same-tier merge conflict ->
re-tier. Requirement matrix; human approves merge/push.
