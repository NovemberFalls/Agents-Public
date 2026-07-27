# /orch-anth-5.0-mega — v5.0 director tier (recursive opus-low sub-orchestration)

STATUS: **PROPOSED — mechanism proved, not yet run end-to-end.** This adds a *director
tier* above the v5.0 coding orchestrator (`/orch-anth-5.0`): an opus/low **director**
partitions a large, multi-domain task and spawns one opus/low **sub-orchestrator per
partition** — each running the full `/orch-anth-5.0` loop on its slice — then integrates
and runs a single final whole-repo gate. It is a *director* role expressed as a coding
skill rather than a persona.

**What is proven, and what is not.** The *mechanism* is validated: a spawned subagent can
itself spawn subagents, so the director → sub-orchestrator → worker chain (3 tiers) is
real (see Feasibility). What is NOT yet measured is whether it *pays* — the value trial is
open (§5). Publishing it here as a proved-working pattern with a high expected payoff on
genuinely multi-domain, partitionable work; not as a graduated default. Default to
`/orch-anth-5.0`. Reach for mega only when §0 holds.

## Feasibility (probed 2026-07-26)

The v5.0 invariant *"only top-level sessions hold the `Agent` tool; workers never fan out"*
is a **design convention, not a platform limit.** Direct probe: a spawned subagent
successfully spawned a sub-subagent that returned — nested spawn works to at least the
depth mega needs (director → sub-orchestrator → worker = 3 tiers). So the mechanism is
real. Mega deliberately relaxes that one convention while keeping every *safety* invariant
it was protecting (§2–§4, §6).

## §0 · When mega applies (all must hold — else use /orch-anth-5.0)

1. **Genuinely partitionable.** The task decomposes into ≥2 sub-mandates with **disjoint
   file/domain ownership** — no two partitions write the same file. If ownership can't be
   made disjoint, mega does not apply; the collision would just move up a tier.
2. **Big enough to matter.** The combined task exceeds what one orchestrator handles well —
   it blows a single orchestrator's context/read budget, OR wall-clock is the binding
   constraint and the partitions can run in parallel. A task one `/orch-anth-5.0` run
   handles comfortably must NOT go to mega (cost, §5).
3. **Shared surface is small and separable.** Cross-partition surfaces (a shared contract,
   schema, lockfile, generated client) are the PARTITION BOUNDARY — done ONCE at the
   director tier as a serialized pre-step, never duplicated inside sub-orchestrators.

Print: `MEGA-GATE: <APPLIES p=<partitions> | DECLINE reason=<...>>`. DECLINE routes to
plain `/orch-anth-5.0`.

## §1 · Director tier (opus/low)

The director does NOT implement. It:

1. **Reads + partitions.** Builds the top-level CDG, then cuts it into P partitions with
   disjoint write-ownership. Any node touching a cross-partition shared surface is pulled
   OUT of every partition and handled as a director-tier pre-step (§2).
2. **Serialized shared pre-step.** The director (or a single sub-orchestrator run FIRST and
   integrated before the others start) lands the shared contract/schema. This is the
   pinned core — the v5.0 CRITICAL/GENERATIVE-core rule, lifted one tier up. No parallel
   partition may depend on an unlanded shared surface.
3. **Fans out.** Spawns one sub-orchestrator per partition, each running `/orch-anth-5.0`
   in its OWN git worktree (isolation), given its partition brief + file-ownership manifest
   + acceptance gate. Isolated worktrees make parallel writers unable to collide at the
   filesystem.
4. **Integrates + final-gates.** Merges accepted worktrees onto one integration branch and
   runs the SINGLE final whole-repo gate. Sub-gates are necessary, not sufficient.

## §2 · One-writer-per-file — now a CROSS-TIER invariant

v5.0's "one writer per file per batch" must hold across the WHOLE tree, not just within one
orchestrator:

- Partitions have **disjoint file-ownership manifests**, assigned by the director.
- Each sub-orchestrator runs in an **isolated worktree** — the isolation primitive, so a
  mistaken cross-partition write collides at integration (explicit, attributable) rather
  than silently corrupting a shared tree.
- A sub-orchestrator needing a file outside its manifest STOPS and reports a scope
  exception UP to the director — it never reaches into another partition.

## §3 · Gates — per tier, single final authority

- **Node/tier gates:** each sub-orchestrator runs its own inside its worktree (v5.0 §4.7).
- **Final gate:** the DIRECTOR runs the whole-repo gate once, after integration. A green
  sub-gate proves a partition self-consistent; only the final gate proves the integrated
  repo. The gate is an exit code, not the sum of sub-reports.

## §4 · The apply-tier is orthogonal (unchanged)

Mega changes WHO orchestrates, not HOW work lands. Inside each partition the
sub-orchestrator still runs the full v5.0 split: DIFFABLE → verbatim SEARCH/REPLACE →
deterministic apply; GENERATIVE → implement; residue → escalate. Fleet-reuse composes: the
director can compute one diff and hand the same block set to every partition/target.

## §5 · Cost — the reason this is not the default (the open trial)

Every tier multiplies spend. Director + P sub-orchestrators + their workers is strictly
MORE total tokens than one `/orch-anth-5.0` run. Mega wins ONLY when **wall-clock is the
constraint and the partitions are truly parallel** — the P sub-orchestrators run
concurrently, so wall-time ≈ the slowest partition, not the sum. If the partitions aren't
parallelizable, or the task fits one orchestrator, mega spends more for no gain. The open
value trial: on a genuinely partitionable task, measure the wall-clock win against the
token multiple, and confirm gate/writer discipline survives the extra tier. Always print
the cost/latency trade in MEGA-GATE.

## §6 · Destructive interlock · reconcile · hygiene

- Destructive interlock holds at EVERY tier: a computed diff touching
  auth/money/concurrency/migrations is presented as a plan with rollback, never
  auto-applied without human approval — whoever computed it.
- **Avoid towering commits:** each partition's sub-orchestrator commits along its own node
  boundaries (`[UNREVIEWED][<partition>/<node>][<CLASS>]`); the director does NOT collapse
  P partitions into one mega-commit.
- Reconcile: the director's matrix rolls up each partition's routing table + the final
  integrated gate. Commit only with human approval.

## Invariants

- All v5.0 invariants hold within each partition.
- Mega DELIBERATELY relaxes "only top-level fans out" — but keeps every safety invariant it
  was protecting: one-writer-per-file (now cross-tier, via worktrees), gate-is-truth
  (single final authority), scope-exceptions-escalate-up, no-towering-commits per partition.
- Partitions must be write-disjoint. Shared surfaces are a boundary handled once at the
  director tier, never duplicated into partitions.
- PROPOSED, mechanism-proved, value-unbenched. Needs one real end-to-end trial before it
  earns arena entry; arena before it earns default on any workload.

## Open questions (pre-registered)

1. Does recursive opus-low sub-orchestration beat one `/orch-anth-5.0` run on wall-clock
   for a genuinely parallel, partitionable task — by how much, at what token multiple?
2. Does gate/writer discipline survive the extra tier, or does integration surface
   collisions a single orchestrator would have avoided?
3. Does director partitioning become a new defect surface (a bad cut splitting a coupled
   change across partitions)?
4. Depth: is 3 tiers the practical ceiling, or does coordination overhead kill it first?
