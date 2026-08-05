# Design brief — `/orch-plan`, `/orch-qa`, `/orch-plan-ralph`

**Status:** OPEN — questions awaiting decision, nothing built.
**Owner:** the team writing the skills. Single owner, start to finish.
**Decider:** Len. Every `ANSWER:` line below is his to fill or delegate; the team
raises gaps this brief missed rather than guessing past them.

## How to use this document

Each question carries a **recommendation** — a default the team can accept with one
word so only the genuinely contested calls cost a conversation. Fill the `ANSWER:` line.
An unanswered question is not a blocker: build against the recommendation, and record
the assumption in the plan artifact where it can be found later. Questions this brief
failed to ask are the more valuable find — add them in §7.

---

## 1 · The requirement, as stated

`/orch-plan` runs a fully comprehensive audit of an idea and ends in a **backlog**:
grouped into sections, prioritized, with explicit QA sections, such that as
`/orch-code-anth` builds, it knows when to emit a `/orch-qa` document.

QA produces **two documents**:

1. the **master list** — every QA item, and
2. the **passed ledger** — every item that has passed, and when.

Regression / back-testing is first-class: when a change requires testing beyond what
it directly touched, that wider set must actually get tested.

Planning covers: **Concept / Goal / Drift / Infrastructure / Software / Target.**

`/orch-plan-ralph` is what most people should run on pass 1 — identical to `/orch-plan`,
except that in the repo where it runs it also produces a full ralph loop, so
`/orch-code-anth` can make one massive first pass and stand up as much as it can.

---

## 2 · The load-bearing question — what makes a PASS expire?

Automatic regression scoping only works if a pass record carries enough information to
invalidate itself. Everything else in the QA design is downstream of this decision.

**Recommendation.** Each entry in the passed ledger pins **commit SHA + the paths that
item's test actually exercises**. When a later `/orch-code-anth` run touches those paths,
the item returns to the master list as `REGRESSION-DUE`, carrying the reason and the
triggering diff.

This makes the regression set *computed*, the same move `/orch-code-anth` already makes
for diffs: the orchestrator understands the change and emits it as data rather than
delegating the judgment. Without it, "regression is highly relevant" degrades into a
model deciding how paranoid to feel on a given run — which is unmeasurable and therefore
uncrownable.

**2.1 — Is the ledger the mechanism, or only the record?**
Mechanism means it drives what gets retested. Record means a human reads it and decides.
*Recommendation: mechanism.*
`ANSWER:`

**2.2 — What is the invalidation trigger?**
Path-touch is precise but under-tests indirect coupling (a change to a shared type that
breaks a caller the test never named). Module- or package-level is coarse: it over-tests,
which is cheap for `MACHINE` items and expensive for `HUMAN` ones.
*Recommendation: path-touch for `MACHINE`, module-level for `HUMAN` — precision where
retesting is free, caution where it costs a person's afternoon.*
`ANSWER:`

**2.3 — Is the passed ledger append-only?**
*Recommendation: yes.* It is evidence. An expired pass produces a NEW `REGRESSION-DUE`
row in the master list; the historical pass keeps its original timestamp rather than
being edited away. This is what makes "when did this last pass, and against what
commit" answerable months later.
`ANSWER:`

**2.4 — Can an item be retired?**
A test for a deleted feature should stop generating regression work without vanishing
from the record.
*Recommendation: a `RETIRED` state with a reason and a date, never a deletion.*
`ANSWER:`

---

## 3 · QA item classes

`/qa-update` today assumes a human runs the tests and writes PASS / FAIL / notes. A
comprehensive audit will generate many items a script can verify outright.

**3.1 — Does the master list tag each item `MACHINE` vs `HUMAN`?**
*Recommendation: yes.* `MACHINE` items run in the gate every time at ~0 marginal cost,
which makes regression nearly free for that class. `HUMAN` items — visual, UX, feel —
are the only ones that need a person, and the only ones where §2's expiry logic governs
real spend. Untagged, "passed" stops telling you what kind of evidence backs it, and the
two classes average into a number that means nothing.
`ANSWER:`

**3.2 — Can a `MACHINE` item auto-record its own pass?**
*Recommendation: yes, and only that class.* A green gate writes the ledger entry
directly. A `HUMAN` item is only ever marked passed by a human. A model must never
write a pass for something nobody ran — that is the failure mode that makes the entire
ledger worthless, and it should be structurally impossible rather than discouraged.
`ANSWER:`

**3.3 — What states exist?**
*Recommendation:* `PENDING`, `PASS`, `FAIL`, `RETEST`, `BLOCKED`, `REGRESSION-DUE`,
`RETIRED`. `RETEST` and `BLOCKED` already exist in `/qa-update` — keep the names.
`ANSWER:`

---

## 4 · The emit trigger

`/orch-code-anth` must know *when* to emit a `/orch-qa` document. This should be a rule,
not a judgment call.

**4.1 — What is the trigger?**
Candidates: per CDG node, per completed tier, per plan section, or on gate-green.
*Recommendation: per plan section, at gate-green.* That matches the commit boundaries
§7 already draws, so the QA document, the candidate commit, and the rollback boundary
all coincide — one artifact per boundary, and per-node noise for MUNDANE work is avoided.
`ANSWER:`

**4.2 — Is `/orch-qa` a third skill, or an output format the others emit?**
The requirement describes it both ways.
*Recommendation: a skill that owns both documents' schemas.* `/orch-code-anth` emits
*through* it rather than reimplementing the format — the same single-implementation rule
that governs the shared applier (`tools/apply_blocks.py`). Two writers of one format is
how the format drifts.
`ANSWER:`

**4.3 — Does `/qa-update` survive, fold in, or get replaced?**
It already does the FAIL → fix → RETEST cycle, and it works.
*Recommendation: fold it in as the update path, keeping its semantics.* Do not write a
second thing that does the same job with different words.
`ANSWER:`

---

## 5 · The plan sections

Concept / Goal / Drift / Infrastructure / Software / Target is clear except one.

**5.1 — Is Drift a planning-time observation or a living ledger?**
Write-once means: here is where the idea has already wandered from the original concept.
Living means: it is updated every pass as the build diverges, and becomes the natural
input to a re-plan.
*Recommendation: living.* It is worth more, but it requires `/orch-plan` to be
**re-runnable against an existing plan without clobbering it** — merge-on-rerun, not
write-once. Decide now; it changes the artifact's whole contract.
`ANSWER:`

**5.2 — Priority axes.**
`/orch-code-anth` already routes on RISK (`CRITICAL` / `WORKHORSE` / `MUNDANE`) and
APPLY-TIER (`DIFFABLE` / `GENERATIVE`).
*Recommendation: reuse both, add sequencing (`P0…P3` or dependency order) and nothing
else.* A third independent axis invented at planning time is ceremony the coder cannot
route on.
`ANSWER:`

**5.3 — Backlog item altitude.**
The existing `/orch-plan` flags this as an open question: too coarse loses routing
signal, too fine is ceremony.
*Recommendation: one item = one thing that can be gated.* If you cannot name the check
that proves it done, it is too coarse; if the check is the same as its neighbour's, it
is too fine.
`ANSWER:`

**5.4 — Where do the artifacts live, and are they committed?**
*Recommendation: repo root, alongside the existing `QA_PLAN.md` convention, and
committed.* Evidence that is not in git cannot be cited later.
`ANSWER:`

---

## 6 · Ralph

**6.1 — What terminates the loop?**
Candidates: iteration cap, token budget, gate-green, backlog exhausted, or no-progress
detection.
*Recommendation: all five, whichever fires first, with the reason recorded.* A first-pass
stand-up run that cannot converge needs a stop that is not "the human notices."
`ANSWER:`

**6.2 — Does §6 (destructive interlock) still apply inside the loop?**
"Stand up as much as it can" and the interlock pull against each other.
*Recommendation: yes, unconditionally.* A ralph loop reaching auth, money, concurrency,
or migrations stops and presents a plan with rollback. An autonomous loop is exactly
where an interlock matters most, and exactly where it is most tempting to weaken it.
`ANSWER:`

**6.3 — Is the loop resumable?**
*Recommendation: yes* — state in the repo, so a killed run resumes rather than restarts.
`ANSWER:`

**6.4 — Is `/orch-plan-ralph` otherwise identical to `/orch-plan`?**
As stated, yes: same skill, plus the loop artifact.
*Recommendation: one engine with a flag, not two files.* Two files that are "the same
except" diverge — that is the bloat this program keeps having to fight.
`ANSWER:`

**6.5 — What does the loop produce, concretely?**
Prompt file, driver script, state file, log?
*Recommendation: name the exact file set in the skill,* so "produces a full ralph loop"
is verifiable rather than interpretive.
`ANSWER:`

---

## 7 · Gaps this brief did not ask about

The team adds them here. This section is the point of the handoff — the questions above
are the ones already visible.

- 

---

## 8 · Why this is worth building carefully

`/orch-plan` is `PROPOSED`, not crowned, and its own file says why: planning "has no
hidden oracle — its proof is downstream." The QA ledger **is** that oracle. Plan-then-
build versus build-direct, measured as *QA items passing without rework on first
submission*, is a real number with a real denominator.

So: design the two documents so that number falls out of them for free. If first-pass
pass-rate has to be reconstructed by hand later, it will not be, and `/orch-plan` stays
PROPOSED forever on vibes.

Per the program's own rule — report cost per SUCCESSFUL run, never per attempt.
