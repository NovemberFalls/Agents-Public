# /orch-code-anth — v5.0 apply-tier (computed-diff · deterministic apply · lane discipline)

STATUS: **LIVE — the coding skill (graduated 2026-07-26).** v5.0 = v4.1 + a
**deterministic apply-tier** for mechanical fan-out (orchestrator computes the exact
change, emits verbatim SEARCH/REPLACE, a stdlib applier lands it). It is a strict
**superset** of v4.1: on GENERATIVE work the apply-tier never fires and behavior is
identical (confirmed 3/3, 22/22 on arena_feature); on DIFFABLE work it wins decisively.
So v5.0 **replaces** v4.1 as the single coding skill — never worse, up to ~2× faster
and cheaper. v4.1 is retired locally, preserved in the Agents-Public repo + backups as
rollback. It is a **tier-split crown, not an absolute one**: v5.0 *beats* v4.1 on
diffable work and *equals* it on generative. Graduated on the mechanism (k=25) and the
whole skill (k=3) — the multi-fixture arena at full k remains the standing bar for any
future challenger.

## The v5.0 thesis (owner-originated 2026-07-26)

**The orchestrator is the brain. When it already understands the exact change, it should
push that change out as data — not delegate the *understanding* to a worker model.** The
worker's job on mechanical/rule-dense edits is APPLICATION, and application of a verbatim
diff is deterministic — it does not need a model at all.

### Evidence (arena_refactor migration + arena_feature generative)

**Mechanism, isolated (68-site fan-out, core pre-done, opus/low, k=25):** v5.0 raw
22/25, wall p50 102s, $0.46/run — vs v4.1 in-place 24/25, 173s, $1.19. ~1.7× faster,
~2.6× cheaper; output band ±15% vs 5×. (Both close to 100% via the mandatory gate +
the §4.9 escalation loop.)

**Whole skill, end-to-end (full fixture, nothing pre-done, self-routed, k=3):** v5.0
3/3 16/16 at $1.91/336s — vs v4.1 3/3 16/16 at $3.85/624s. **1.9× faster, 2.0× cheaper,
correctness-equal** (v4.1 grinds 45–130 Edit-turns; v5.0 emits once + applies).

**Generative regression (arena_feature, generative-heavy, k=3):** v5.0 3/3, 22/22 —
clean superset, no regression where the apply-tier never fires.

Apply fidelity: 532/532 blocks clean across the mechanism runs; the 3 v5.0 misses were
detected + typed (2 fidelity, 1 rule), recovered to 16/16 at ~$0.01/run amortized.

The apply half is a string match (not model-dependent); the correctness half is Opus's
planning, which lands 16/16 on its scope. Evidence: Agents-Public `FINDINGS.md` §4.7 +
this session's raw runs (`bench/results/` h2h_api_* and the v5 gauntlet/whole-skill rows).

### Why FORMAT is load-bearing (the failures that shaped this)

- Opus hand-written **unified diff** → line-number drift → `git apply` REJECTS; fuzzy
  `patch` recovers only 13/16.
- **Lossy old/new pairs** (not copied verbatim from the file) → 5/16 deterministic,
  8/16 even with a model applying. **A bad diff is WORSE than no diff**: a worker handed
  a flawed "exact" patch scored *below* the same worker interpreting the spec (8/16 <
  10/20). Do not emit approximate edits.
- **SEARCH/REPLACE with verbatim SEARCH** (copied byte-for-byte from the file Opus just
  read) removes drift entirely → 532/532 clean apply. This is the only sanctioned format.

---

## §0 · The apply-tier gate (NEW — decide before choosing SOLO/SWARM)

After the §1 inventory, ask one added question of the work: **is a node's change
EXPRESSIBLE as localized, verbatim text swaps against files that already exist?**

- **DIFFABLE** — logging/API migrations, signature threading, rename sweeps, config
  edits, mechanical refactors: the change is N independent site-edits with a computable
  before/after. These are the v5.0 apply-tier's target.
- **GENERATIVE** — new files, structural rewrites, algorithm design, anything whose
  output isn't a swap against existing text. These stay on the v4.1 paths (a model
  implements; the apply-tier does not apply).

Print: `APPLY-TIER: <DIFFABLE n=<sites> | GENERATIVE | MIXED c=<diffable>/<generative>>`

MIXED is normal: the CRITICAL/GENERATIVE core (e.g. a shared contract rewrite) is
implemented by Opus as in v4.1; the DIFFABLE fan-out (the dozens of call-site migrations
that depend on it) routes to the apply-tier. This is the same split v4.1 already draws
between the pinned-contract core and its downstream sites — v5.0 just makes the
downstream deterministic instead of a worker swarm.

## §1 · Inventory — unchanged from v4.1

[Read the task and spec/source. COUNT sites, files, read-volume, nodes-by-RISK
(CRITICAL / WORKHORSE / MUNDANE). See v4.1 §1 — carried verbatim.]

## §2 · Scale gate — unchanged from v4.1

[`GATE: SOLO|SWARM — sites=… files=… read≈…K nodes=… mix=C/W/M`, thresholds and
tiebreak per v4.1 §2. The apply-tier does not change WHEN to swarm — it changes HOW the
DIFFABLE portion of a swarm is executed.]

## §3 · SOLO path — unchanged from v4.1

[In-session checklist discipline + §5 gate. If the SOLO job is DIFFABLE and large, the
orchestrator MAY still use the apply-tier (§4.9) on itself: compute the blocks, apply
deterministically, gate — this is where the 3×/4× win shows up even without a swarm.]

## §4 · SWARM path

§4.1–§4.8 are **carried verbatim from v4.1** (plan-as-data, worker grouping, THE MANDATE,
lanes, briefs, landing protocol, the gate, escalation ladder). THE MANDATE still holds:
the orchestrator does not hand-implement GENERATIVE work to save effort. The apply-tier is
not an exception to the mandate — it is a *deterministic* execution of work the
orchestrator has fully computed, which is categorically different from the orchestrator
secretly doing a worker's judgment job.

### §4.9 · The apply-tier (NEW — for the DIFFABLE portion only)

When the plan marks a node/cluster DIFFABLE:

1. **Compute, don't delegate.** The orchestrator (Opus) reads the target files and the
   binding spec and emits one **SEARCH/REPLACE block per site**, in exactly this format:

   ```
   FILE: <path from repo root>
   <<<<<<< SEARCH
   <exact current line(s), copied VERBATIM from the file — byte-for-byte, same indent;
    include enough surrounding lines to be UNIQUE if a bare line repeats>
   =======
   <replacement line(s) per the spec rules>
   >>>>>>> REPLACE
   ```

   The SEARCH text MUST be verbatim from disk — that is the entire fidelity mechanism.
   Approximate SEARCH is a defect worse than no diff (see evidence). This is emitted as
   plan data to the scratch dir (`plan.blocks`), never narrated inline.

2. **Apply deterministically — no worker model.** A stdlib applier: for each block, find
   the SEARCH text in the named file; apply iff it matches **exactly once**. Record
   `applied / nomatch / nonunique` counts. A clean run is `applied == blocks, nomatch=0,
   nonunique=0`. This step costs ~0 tokens and ~0 seconds and is 100% reproducible.

3. **Residual → escalate, don't guess.** Any `nomatch` (Opus's SEARCH wasn't verbatim)
   or `nonunique` (insufficient context) block does NOT get force-applied. It is handed
   to a single cheap worker (sonnet) with the block + the file, "apply this one edit;"
   OR bounced back to Opus to re-emit that block with more context. Deterministic-first;
   model only for the residue. (In the validation run the residue was zero.)

4. **Gate as always (§4.7).** The deterministic apply changes nothing about the gate —
   the script, not the block counts, decides done. Verbatim-clean apply is necessary,
   not sufficient: Opus can still mis-RULE a REPLACE (a planning miss), which only the
   oracle/gate catches. The 15→16 gap in early runs was a planning/ scope issue caught
   exactly here.

### §4.9a · Fleet reuse (the scale multiplier)

Because the SEARCH/REPLACE set is data and the apply is deterministic, the SAME computed
diff applies to N repositories/instances at ~0 marginal cost. For fleet-wide mechanical
migrations, Opus computes once; apply runs everywhere. This is the "scale through Opus"
case: the compute is spent on understanding ONCE, not re-litigated per target.

### §4.4′ · Lanes — reframed for v5.0

| tier | v4.1 | v5.0 |
|---|---|---|
| CRITICAL / GENERATIVE core | `opus` worker | `opus` (orchestrator implements, unchanged) |
| DIFFABLE fan-out | `haiku`/`sonnet` worker interprets + applies | **orchestrator computes blocks → deterministic apply** |
| DIFFABLE residue (nomatch/nonunique) | — | one `sonnet` apply, or Opus re-emit |

The worker model tier stops mattering for DIFFABLE work — application is deterministic.
The local lane finding corroborates: a *faithful* diff flipped the local 30B from 0/4 to
5/5 on a slice; where its lane matters at all is only the residue.

## §5 · SOLO gate — unchanged. §6 · Destructive interlock — unchanged (a computed diff
touching auth/money/concurrency/migrations is STILL destructive; it is presented as a
plan with rollback and never auto-applied without human approval).

### §7 · Reconcile & hand off

- Add to the routing table: DIFFABLE nodes with `blocks applied / nomatch / nonunique`
  and any residue escalations.
- **Avoid towering commits.** Each CDG node / DIFFABLE cluster lands as its own local
  candidate commit — a rollback/attribution boundary, not publication — tagged
  `[UNREVIEWED][<node>][<CLASS>] <summary>`. Do NOT accumulate the whole apply-tier
  fan-out into one giant working-tree diff; the apply-tier's per-node data already gives
  the boundaries, so commit along them. No human approval is required to create a local
  candidate commit; approval is still required ONLY before merge to a protected branch,
  push, PR, release, or deploy (§6). In auto-approve/headless mode, leave the tree
  uncommitted per §8 rather than towering it.

§8 · Hygiene — unchanged (commit only with human approval; in auto-approve mode leave the
tree uncommitted).

## Invariants (v4.1 + v5.0)

- All v4.1 invariants hold.
- The apply-tier is ONLY for DIFFABLE nodes; GENERATIVE work is never faked as a diff.
- SEARCH text is verbatim-from-disk or the block is invalid. Approximate diffs are banned.
- Deterministic apply never force-applies a non-unique/no-match block; residue escalates.
- The gate, not the apply counts, is the evidence. A clean apply of a wrong REPLACE is
  still a failure the gate must catch.
- PROPOSED until the arena clears it at k=25. Do not route production traffic here yet.

## Open questions for the arena (pre-registered)

1. Correctness at k=25 across fixtures (does 16/16 hold, and on GENERATIVE-heavy work
   where the apply-tier does NOT apply — is v5.0 ever WORSE than v4.1?).
2. Does the DIFFABLE/GENERATIVE call itself become a new defect surface (mis-labeling a
   generative node as diffable → bad blocks)?
3. Opus effort for the emit step (low held 16/16 on scope here; high did not improve it).
4. Fleet-reuse correctness: does one computed diff stay correct across drifted targets,
   or does target drift reintroduce the nomatch residue at scale?
