# Enforcement hooks — turn the routing rules into denied tool calls (optional)

The [`/orchestrate`](../.claude/commands/orchestrate.md) skill text carries the
routing behavior on its own — that is what the benchmarks test. This layer is the
mechanical backstop for daily-driver use: while a swarm plan is declared, the rules
stop being prose and become **denied tool calls**.

What it enforces (only while a plan is active — zero effect otherwise):

1. **The mandate.** The orchestrator's own product-file `Edit`/`Write` calls are
   denied while the batch window is closed — the orchestrator does not implement;
   workers do. (Workers pass by session identity, or by the open/close batch
   window.)
2. **The floor.** Every `Agent` spawn must carry an explicit `model`, and a spawn
   whose description names a planned worker may not run *below* its planned lane.
   Escalating up after a failure is always allowed — that's the ladder.
3. **The ceiling.** A worker's *first* spawn may not run *above* its planned lane
   unless the plan names the promoting trap (`workers[i].trap`). Silent up-laning is
   how cheap lanes die — measured twice: the v4.0 grouping defect, and the routing
   drift that appears when the orchestrator runs at lower reasoning effort
   (FINDINGS, Round 3). Attempt ≥ 2 is exempt (that's the escalation ladder);
   attempts are counted in the marker's spawn log.

**Fail-open by design.** No active marker → every call allowed; any internal error →
allowed. The hook adds friction inside a declared swarm, never risk outside one.

## Install

1. Copy this `hooks/` directory somewhere stable.
2. Merge [`settings-snippet.json`](settings-snippet.json) into your
   `~/.claude/settings.json`, replacing `<ABSOLUTE-PATH-TO>` with the real path.
3. The orchestrator drives the lifecycle via `orch_declare.py` (Bash) at the plan
   checkpoints:

```
python orch_declare.py --repo <abs repo> declare --plan <abs plan.json>
python orch_declare.py --repo <abs repo> open      # dispatching a batch
python orch_declare.py --repo <abs repo> close     # batch landed
python orch_declare.py --repo <abs repo> repair    # ladder-exhausted repair only
python orch_declare.py --repo <abs repo> clear     # run over -> enforcement off
```

State lives outside the repo in `<TEMP>/orch-active/`; deleting it (or `clear`)
disables everything instantly.

## Tests

`python test_orch_enforce.py` — 18 cases, run against the real hook as a subprocess
with an isolated fake `%TEMP%`: mandate denies/allows, floor, ceiling, ladder
exemption, fail-open on malformed input and missing plans.

## Known residual gap

An orchestrator that opens the batch window and edits in the same breath defeats
check 1. The deny message plus the declare audit trail turn that into a visible,
deliberate act instead of silent drift — which is the point. If your Claude Code
version predates JSON `permissionDecision` hook output, switch `_deny` to
exit-code-2 + stderr.
