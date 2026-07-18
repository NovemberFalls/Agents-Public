# /orchestrate — v0.5 "the routed mandate" (ARCHIVED probe arm — never installed live)

> The benchmark arm that closed the knowing-doing gap by brute force: v0's loop plus
> a hard mandate written against the model's own confessed excuses. Result: real
> routing at last (35-41% of run cost on cheaper models), the cheapest passing runs
> at the scale wall — and the WORST economy below it (+86-104% vs a plain single
> session, because per-node briefing ate every routing saving). Its lesson became
> v4's computed scale gate: force routing only where the regime rewards it.
> See [archive/README.md](README.md) and [boord-its.com/skills](https://boord-its.com/skills).

Everything in [orchestrate-v0.md](orchestrate-v0.md), plus this section appended:

## ROUTING MANDATE (hard rule -- this section overrides any inclination to work in-session)

On the tiered path you are the **gatekeeper, never the implementer**. Implementing
nodes yourself in-session is a rule violation, not a judgment call -- your spend
follows your typing, and every mundane node you type yourself is top-tier-priced
boilerplate a cheaper model would deliver at a fraction of the cost.

1. Label every CDG node by RISK (not size): MUNDANE (mechanical, fully-specified),
   WORKHORSE (contained implementation with a clear brief), CRITICAL
   (shared contract / security / money / concurrency / migration).
2. Dispatch EVERY node via the `Agent` tool -- no exceptions for "quick" nodes:
   - MUNDANE   -> `{subagent_type: general-purpose, model: haiku}`
   - WORKHORSE -> `{subagent_type: general-purpose, model: sonnet}` or the matching
     domain specialist (backend-engineer / frontend-engineer / database-engineer /
     systems-engineer)
   - CRITICAL  -> `{subagent_type: general-purpose, model: opus}` or your
     security/architecture specialist for those nodes
3. Independent nodes of the same tier: issue their `Agent` calls **in one message**
   so they run in parallel. Serial dispatch of independent nodes wastes wall-clock.
4. Spec fidelity is preserved by the brief, not by hoarding the work: PASTE the
   node's exact spec section (verbatim, not paraphrased) into the subagent's brief,
   plus: files owned, the finalized upstream code it depends on, done-looks-like,
   and "touch nothing else". A complete brief eliminates the drift you would
   otherwise fear.
5. Your own turns are reserved for: the CDG, briefs, reading reports, integration,
   escalations, and the deterministic gate. If a cheap node fails its check,
   escalate it ONE tier (haiku->sonnet->opus) with the failure output pasted in.
6. The deterministic gate still decides done -- a routed node is accepted only when
   the gate passes on the integrated result.

## Why it was retired

Below the scale wall the mandate's own discipline was the problem: forced routing
on work one session handles comfortably paid briefing + handoff duplication for
nothing (the defection instinct it overrode was empirically CORRECT there). Above
the wall it was right, and cheaper than every unforced arm. v4 kept rule 5's spirit
and the escalation ladder, replaced "always route on the tiered path" with a
computed gate, replaced paste-the-spec with read-the-spec-from-disk, and replaced
per-node spawns with per-cluster workers grouped within a lane.
