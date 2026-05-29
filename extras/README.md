# extras/ — preserved, but NOT the validated core

Everything in this folder was part of the original, more elaborate design. It is kept for reference and honesty — **none of it is the validated core.** The core is the `/orchestrate` loop at the repo root: the CDG + subagents + one deterministic check. See [../FINDINGS.md](../FINDINGS.md) for what was tested and why these pieces were demoted.

## What's here, and why it's here and not there

- **`advisory-board/`, `writing-team/`, `ttrpg-team/`** — the same orchestration pattern applied to non-code domains (project-strategy review, manuscript review, game-rules pressure-testing). Legitimate ideas, but **never validated in a controlled test**, and the breadth diluted the one thing that was. Useful if you want to adapt the pattern beyond code.
- **`swarm.md`** — the optional director / cross-team layer. For a single project, `/orchestrate` is invoked directly; this layer added coordination overhead without validated benefit.
- **`orchestration-loop.md`** — the older, heavier loop with the full mandatory-gate battery. Superseded by the lean `/orchestrate` loop; kept so you can see what was trimmed and why.
- **`board-review.md`** — the advisory board's scoring formula and process (pairs with `advisory-board/`).
- **`sample-review/`** — a worked advisory-board review of a fictional project.

## The short version

We thought this material was the value. The eval said otherwise: the elaborate ceremony cost tokens without earning them, and the rich personas made no measurable difference. The rockstar was the dependency graph. If you only adopt one thing from this repo, adopt the [`/orchestrate`](../.claude/commands/orchestrate.md) loop — not this folder.
