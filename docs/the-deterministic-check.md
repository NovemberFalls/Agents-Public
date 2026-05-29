# The Deterministic Check — the one gate that earned its place

This is the single verification gate in the validated core. It is the thing that **worked**, so here is how to actually use it.

## The rule

After the integrated result is assembled (whether one specialist did it or several tiers did), gate it with **something that has an exit code**: a typecheck, a test suite, or a build. A non-zero exit is a hard block — fix and re-run before anything reaches a human or a commit. That's it. One gate.

## Why deterministic, not an LLM "review"

This isn't a stylistic preference — it's what the eval showed ([../examples/eval/](../examples/eval/)). When we tested LLM "reviewer" arms against a planted-bug fixture, **every arm hallucinated the same false positive** ("`hmac.new` doesn't exist" — it does), regardless of how rich its persona was. Meanwhile the deterministic `mypy` oracle is what actually caught the real integration break (a consumer reading a field the model had renamed).

> A reviewer persona produces an *opinion*. A typecheck / test / build produces a *fact*. Gate on the fact.

LLM review passes and hygiene sweeps can still be useful add-ons — but they are optional, and they don't replace the deterministic gate.

## How to wire it

Pick the strongest exit-code check your stack offers and run it on the integrated changes:

| Stack | Deterministic check |
|------|---------------------|
| TypeScript | `tsc --noEmit` (+ the test suite) |
| Python (typed) | `mypy` (+ `pytest`) |
| Go | `go build ./... && go vet ./...` (+ `go test`) |
| Rust | `cargo check` (+ `cargo test`) |
| Any | the project's existing build + test command |

The check must run **on the integrated state** — all the tiers' output combined — not on each change in isolation. Integration breakage only shows up when the pieces meet.

## The exact setup that caught the bug (Python + Pydantic)

In the CDG eval, the contract was a Pydantic model whose fields one file renamed and another consumed. Plain `mypy` missed it (the consumer's variable was inferred as `Any`); `mypy` **with the Pydantic plugin** caught it. The setup:

```ini
# mypy_eval.ini
[mypy]
plugins = pydantic.mypy
ignore_missing_imports = True
follow_imports = silent
```

```bash
# Gate: non-zero exit blocks. Scope to the changed files + the model they depend on.
mypy --config-file mypy_eval.ini api/models.py api/routers/pvp.py api/routers/characters.py
```

A renamed field with a stale consumer produces, deterministically:

```
error: "CombatWindowTotals" has no attribute "pvp_kills"  [attr-defined]
```

That single line — not a reviewer's prose — is what flips a run from "looks fine" to "blocked."

## Where it sits in `/orchestrate`

It's step 4 of the [loop](../.claude/commands/orchestrate.md): after the tiers finalize, run the check on the integrated result; non-zero blocks; then reconcile and hand to the human. Wire the same command into CI or a pre-commit hook if you want the gate enforced at the harness level rather than relying on the agent to run it.
