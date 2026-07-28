# /orch-code-anth-mega — v5.0 director tier (recursive opus-low sub-orchestration)

STATUS: **PROPOSED — experimental, NOT LIVE, unbenched.** This adds a *director tier*
above the v5.0 coding orchestrator: an opus/low **director** that partitions a large,
multi-domain task and spawns one opus/low **sub-orchestrator per partition** — each of
which runs the full `/orch-code-anth` loop on its slice — then integrates and runs a
single final whole-repo gate. It is Vera's role (cross-team/multi-domain director)
expressed as a coding skill rather than a persona.

Do NOT route production traffic here. Default to `/orch-code-anth`. Reach for mega only
when the conditions in §0 actually hold.

## Feasibility (probed 2026-07-26)

The v5.0 invariant "only top-level sessions hold the `Agent` tool; workers never fan out"
is a **design convention, not a harness limit.** Direct probe: a spawned subagent
(tools: `*`) successfully spawned a sub-subagent that returned — nested spawn works to at
least the depth mega needs (director → sub-orchestrator → worker = 3 tiers). So the
mechanism is real; the open question is whether it PAYS (see §5) and whether gate/writer
discipline survives the extra tier (see §3–§4). That is what the one trial must answer.

## §0 · When mega applies (all must hold — else use /orch-code-anth)

1. **Genuinely partitionable.** The task decomposes into ≥2 sub-mandates with **disjoint
   file/domain ownership** — no two partitions write the same file. If ownership can't be
   made disjoint, mega does not apply; the collision would just move up a tier.
2. **Big enough to matter.** The combined task exceeds what one orchestrator handles well
   — either it blows a single orchestrator's context/read budget, OR wall-clock is the
   binding constraint and the partitions can run in parallel. A task a single
   `/orch-code-anth` run handles comfortably must NOT go to mega (cost, §5).
3. **Shared surface is small and separable.** Cross-partition surfaces (a shared contract,
   schema, lockfile, generated client) are the PARTITION BOUNDARY — they are done ONCE at
   the director tier as a serialized pre-step, never duplicated inside sub-orchestrators.

Print: `MEGA-GATE: <APPLIES p=<partitions> | DECLINE reason=<...>>`. DECLINE routes to
plain `/orch-code-anth`.

## §1 · Director tier (opus/low)

The director does NOT implement. It:

1. **Reads + partitions.** Builds the top-level CDG, then cuts it into P partitions with
   disjoint write-ownership. Any node touching a cross-partition shared surface is pulled
   OUT of every partition and handled as a director-tier pre-step (§2).
2. **Serialized shared pre-step.** The director (or a single sub-orchestrator, run FIRST
   and integrated before the others start) lands the shared contract/schema. This is the
   pinned core — exactly the v5.0 CRITICAL/GENERATIVE-core rule, lifted one tier up. No
   parallel partition may depend on an unlanded shared surface.
3. **Fans out.** Spawns one sub-orchestrator per partition:
   `Agent({ subagent_type: "<v5.0 orchestrator>", model: "opus"|low, isolation: "worktree", prompt: "<partition brief + its file-ownership manifest + acceptance gate>" })`.
   Each sub-orchestrator runs `/orch-code-anth` in its OWN git worktree so parallel
   writers cannot collide at the filesystem.
4. **Integrates + final-gates.** Merges accepted worktrees onto one integration branch and
   runs the SINGLE final whole-repo gate. Sub-gates are necessary, not sufficient.

## §2 · One-writer-per-file — now a CROSS-TIER invariant

v5.0's "one writer per file per batch" must hold across the WHOLE tree, not just within
one orchestrator. Enforcement:

- Partitions have **disjoint file-ownership manifests**, assigned by the director.
- Each sub-orchestrator runs in an **isolated worktree** (`isolation: "worktree"`) — the
  isolation primitive, so a mistaken cross-partition write collides at integration
  (explicit, attributable) rather than silently corrupting a shared tree.
- A sub-orchestrator that needs a file outside its manifest STOPS and reports a scope
  exception UP to the director — it never reaches into another partition. Same rule v5.0
  workers already follow, one tier higher.

## §3 · Gates — per tier, single final authority

- **Node/tier gates:** each sub-orchestrator runs its own, inside its worktree (v5.0 §4.7,
  unchanged).
- **Final gate:** the DIRECTOR runs the whole-repo gate once, after integration. A green
  sub-gate proves a partition self-consistent; only the director's final gate proves the
  integrated repo. The gate is an exit code, not the sum of sub-reports.

## §4 · The apply-tier is orthogonal (unchanged)

Mega changes WHO orchestrates, not HOW work lands. Inside each partition the
sub-orchestrator still does the full v5.0 split: DIFFABLE → compute verbatim
SEARCH/REPLACE → deterministic apply; GENERATIVE → implement; residue → escalate. The
§4.9a fleet-reuse case composes naturally: the director can compute one diff and hand the
same block set to every partition/target.

## §5 · Cost — the reason this is not the default

Every tier multiplies spend. Director context + P sub-orchestrator contexts + their
workers is strictly MORE total tokens than one `/orch-code-anth` run. Mega only wins when
**wall-clock is the constraint and the partitions are truly parallel** — the P
sub-orchestrators run concurrently, so wall-time ≈ the slowest partition, not the sum.
If the partitions aren't parallelizable, or the task fits one orchestrator, mega spends
more for no wall-clock gain. Always print the cost/latency trade in the MEGA-GATE line.

## §6 · Destructive interlock + §7 reconcile + §8 hygiene

- Destructive interlock (v5.0 §6) holds at EVERY tier: a computed diff touching
  auth/money/concurrency/migrations is presented as a plan with rollback, never
  auto-applied without human approval — whether the director or a sub-orchestrator
  computed it.
- **Avoid towering commits (v5.0 §7):** each partition's sub-orchestrator commits along
  its own node boundaries (`[UNREVIEWED][<partition>/<node>][<CLASS>]`); the director does
  NOT collapse P partitions into one mega-commit. Attribution stays per-node across tiers.
- Reconcile: the director's matrix rolls up each partition's routing table + the final
  integrated gate. §8 hygiene unchanged (commit only with human approval).

## Invariants

- All v5.0 invariants hold within each partition.
- Mega DELIBERATELY relaxes "only top-level fans out" — but keeps every safety invariant
  it was protecting: one-writer-per-file (now cross-tier, via worktrees), gate-is-truth
  (single final authority), scope-exceptions-escalate-up, and no-towering-commits.
- Partitions must be write-disjoint. Shared surfaces are a boundary handled once at the
  director tier, never duplicated into partitions.
- PROPOSED and unbenched. Needs one real trial (does it PAY on a genuinely partitionable
  task) before it earns arena entry, and arena k before it earns default on any workload.

## Open questions for the trial / arena (pre-registered)

1. Does recursive opus-low sub-orchestration beat a single `/orch-code-anth` run on
   wall-clock for a genuinely parallel, partitionable task — and by how much, at what
   token multiple?
2. Does gate/writer discipline actually survive the extra tier, or does integration
   surface collisions a single orchestrator would have avoided?
3. Does the director's partitioning become a new defect surface (a bad cut that splits a
   coupled change across partitions)?
4. Depth limit: is 3 tiers (director → sub-orch → worker) the practical ceiling, or does
   context/coordination overhead kill it before then?
