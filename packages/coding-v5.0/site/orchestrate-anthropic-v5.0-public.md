---
name: orchestrate
description: Run the v5.0 orchestration loop — computed SOLO/SWARM scale gate, a DIFFABLE/GENERATIVE apply-tier split, plan-as-data, model lanes, deterministic gates. On mechanical fan-out the orchestrator computes the exact change and a stdlib applier lands it; no worker model in the edit path.
---

# /orchestrate — v5.0 apply-tier (computed-diff · deterministic apply · lane discipline)

Count the work, print a SOLO/SWARM verdict, obey it. Split the work into DIFFABLE
(expressible as verbatim text swaps) and GENERATIVE (everything else). Compute the
DIFFABLE changes yourself and let a deterministic applier land them — no worker model in
the mechanical path. Gate on a deterministic check, never on a model's opinion.

**Operating principle.** The orchestrator is the brain. When it already understands the
exact change, it pushes that change out as data rather than delegating the *understanding*
to a worker. Application of a verbatim diff is deterministic — it does not need a model.

Save as `~/.claude/commands/orchestrate.md` (invoke `/orchestrate <task>`) or
`~/.claude/skills/orchestrate/SKILL.md`. Self-contained: no companion files, no harness,
no prior version. Free to use and adapt; no warranty.

*Measurements, losing runs, and known limits — deliberately not shipped in this file —
are at <https://boord-its.com/skills>.*

---

## §0 · The apply-tier gate (decide before choosing SOLO/SWARM)

After the §1 inventory, ask one added question of the work: **is a node's change
EXPRESSIBLE as localized, verbatim text swaps against files that already exist?**

- **DIFFABLE** — logging/API migrations, signature threading, rename sweeps, config
  edits, mechanical refactors: the change is N independent site-edits with a computable
  before/after. These are the apply-tier's target.
- **GENERATIVE** — new files, structural rewrites, algorithm design, anything whose
  output isn't a swap against existing text. A model implements these; the apply-tier
  does not apply.

Print: `APPLY-TIER: <DIFFABLE n=<sites> | GENERATIVE | MIXED c=<diffable>/<generative>>`

MIXED is normal: the CRITICAL/GENERATIVE core (e.g. a shared contract rewrite) is
implemented by the orchestrator; the DIFFABLE fan-out (the dozens of call-site
migrations that depend on it) routes to the apply-tier. That is the same split between
pinned-contract core and downstream sites the earlier versions drew — v5.0 just makes
the downstream deterministic instead of a worker swarm.

## §1 · Inventory

Read the task and the spec/source **before** deciding anything. COUNT: sites, files,
read-volume, and nodes by RISK — CRITICAL (shared contracts, auth, money, concurrency,
migrations), WORKHORSE (real implementation, contained blast radius), MUNDANE
(mechanical, low-judgment). The inventory is numbers, not vibes; the gate below consumes
them.

## §2 · Scale gate

Print the computed gate before any work:

```
GATE: SOLO|SWARM — sites=… files=… read≈…K nodes=… mix=C/W/M
```

SWARM when the work genuinely splits into independent nodes AND the read-volume or site
count exceeds what one context should carry (rule of thumb: ≳8 independent nodes, or
≳50K of reading that no single node needs in full). Otherwise SOLO — below the crossover
a swarm costs more than it saves. Tiebreak toward SOLO. The apply-tier does not change
WHEN to swarm; it changes HOW the DIFFABLE portion is executed.

## §3 · SOLO path

In-session checklist discipline plus the §5 gate. If the SOLO job is DIFFABLE and large,
use the apply-tier (§4.9) on yourself: compute the blocks, apply deterministically, gate.
This is where the speed and cost win shows up even without a swarm.

## §4 · SWARM path

Plan-as-data (the plan is written to a scratch file, not narrated inline), worker
grouping by node, briefs that pin the contract, a landing protocol, the gate, and an
escalation ladder.

**THE MANDATE:** the orchestrator does not hand-implement GENERATIVE work to save
effort. The apply-tier is not an exception — it is a *deterministic* execution of work
the orchestrator has fully computed, which is categorically different from the
orchestrator quietly doing a worker's judgment job.

### §4.9 · The apply-tier (for the DIFFABLE portion only)

When the plan marks a node/cluster DIFFABLE:

1. **Compute, don't delegate.** The orchestrator reads the target files and the binding
   spec and emits one **SEARCH/REPLACE block per site**, in exactly this format:

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
   Approximate SEARCH is a defect worse than no diff — measured: a worker handed a lossy
   "exact" patch scored BELOW the same worker reading the spec. Emit this as plan
   data to a scratch file, never narrated inline.

2. **Apply deterministically — no worker model.** A stdlib applier: for each block, find
   the SEARCH text in the named file; apply iff it matches **exactly once**. Record
   `applied / nomatch / nonunique` counts. A clean run is `applied == blocks, nomatch=0,
   nonunique=0`. This step costs ~0 tokens and ~0 seconds and is 100% reproducible.

   **The applier is a companion download to this skill** — `apply_blocks.py`, stdlib only,
   no dependencies. Save it next to this file, e.g. `~/.claude/tools/orch-apply/`:

   ```
   python ~/.claude/tools/orch-apply/apply_blocks.py plan.blocks --root . --json apply.json
   ```

   Exit `0` = all blocks applied · `1` = residue to escalate (step 3) · `2` = malformed
   blocks (fix the emit, never force it). `--dry-run` reports without writing; `--atomic`
   refuses partial application.

   **Do NOT write your own and do NOT have a model apply the blocks.** Both defeat the
   mechanism: a model handed a flawed "exact" patch scored 8/16, *below* the same model
   working from the spec at 10/20. An approximate applier is worse than none.

   If the applier is not present, **say so and stop** — do not fall back to in-place
   editing, which discards the entire speed and cost advantage of this tier.

3. **Residual → escalate, don't guess.** Any `nomatch` (the SEARCH wasn't verbatim) or
   `nonunique` (insufficient context) block does NOT get force-applied. Hand it to a
   single cheap worker with the block and the file — "apply this one edit" — or bounce
   it back to the orchestrator to re-emit with more context. Deterministic first; model
   only for the residue.

4. **Gate as always (§5).** The deterministic apply changes nothing about the gate — the
   script, not the block counts, decides done. A verbatim-clean apply is necessary, not
   sufficient: the orchestrator can still mis-rule a REPLACE (a planning miss), which
   only the oracle/gate catches.

### §4.9a · Fleet reuse (the scale multiplier)

Because the SEARCH/REPLACE set is data and the apply is deterministic, the SAME computed
diff applies to N repositories at ~0 marginal cost. For fleet-wide mechanical migrations,
compute once; apply everywhere. The compute is spent on understanding ONCE, not
re-litigated per target. (Caveat: targets that have drifted from the read state produce
`nomatch` residue — that is the mechanism working, not failing. Escalate per §4.9.3.)

### §4.4′ · Lanes

| tier | v4.1 | v5.0 |
|---|---|---|
| CRITICAL / GENERATIVE core | `opus` worker | `opus` (orchestrator implements, unchanged) |
| DIFFABLE fan-out | `haiku`/`sonnet` worker interprets + applies | **orchestrator computes blocks → deterministic apply** |
| DIFFABLE residue (nomatch/nonunique) | — | one `sonnet` apply, or orchestrator re-emit |

The worker model tier stops mattering for DIFFABLE work — application is deterministic.
The local-model finding corroborates: a *faithful* diff flipped a local 30B from 0/4 to
5/5 on a slice. Where a worker's capability matters at all is only the residue.

## §5 · The gate

A deterministic check decides done — a test, a build, a script, a grep that must return
zero. Not a model's opinion of its own work, and not the apply counts. If there is no
deterministic check, write one before declaring the work finished.

## §6 · Destructive interlock

A computed diff touching auth, money, concurrency, or migrations is STILL destructive. It
is presented as a plan with a rollback path and never auto-applied without human
approval.

## §7 · Reconcile & hand off

- Routing table: DIFFABLE nodes with `blocks applied / nomatch / nonunique`, plus any
  residue escalations.
- **Avoid towering commits.** Each node / DIFFABLE cluster lands as its own local
  candidate commit — a rollback and attribution boundary, not publication — tagged
  `[UNREVIEWED][<node>][<CLASS>] <summary>`. Do NOT accumulate the whole fan-out into one
  giant working-tree diff; the apply-tier's per-node data already gives you the
  boundaries, so commit along them. No human approval is required to create a local
  candidate commit; approval is still required ONLY before merge to a protected branch,
  push, PR, release, or deploy (§6). In auto-approve/headless mode, leave the tree
  uncommitted rather than towering it.

## §8 · Hygiene

Commit only with human approval; in auto-approve mode leave the tree uncommitted.

## Invariants

- The apply-tier is ONLY for DIFFABLE nodes; GENERATIVE work is never faked as a diff.
- SEARCH text is verbatim-from-disk or the block is invalid. Approximate diffs are banned.
- Deterministic apply never force-applies a non-unique or no-match block; residue
  escalates.
- The gate, not the apply counts, is the evidence. A clean apply of a wrong REPLACE is
  still a failure the gate must catch.
- The orchestrator does not hand-implement GENERATIVE work to save effort (THE MANDATE).
- Nothing is pushed, merged, or deployed without human approval.
