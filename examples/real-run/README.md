# Real Orchestration Run — Hardening This Repository (Metered)

> **This is not fictional.** The numbers below are the harness-reported token usage from the actual orchestration run that produced this repository — the session that genericized every agent to role-based names, fixed the frontmatter, rewrote the docs, and built the [conceptual Verdant walkthrough](../orchestrated-run/). The repo documents its own creation.

For the clean, step-by-step illustration of *how* the loop works (CDG → tiers → gates), read [`../orchestrated-run/`](../orchestrated-run/) — that one is a deliberately simple fictional task. This file is the opposite: a messy real run, with real costs, measured.

---

## What the run did

A single Orchestrator (the main session) coordinated **16 subagent spawns** across an audit phase, two implementation tiers, and a set of review/hygiene gates, to take the repository from "private export with personal-named personas" to "role-genericized, schema-correct, AAA release." The Orchestrator wrote almost no content itself — it planned, delegated, reviewed reports, and integrated.

## The numbers (metered)

Every row's **tokens / tool calls / duration** is reported by the Claude Code harness for that subagent's isolated window. Grouped by phase.

| # | Subagent (role) | What it did | Tokens | Tool calls | Duration |
|---|-----------------|-------------|-------:|-----------:|---------:|
| 1 | Security Engineer | Leak/PII sweep (tree + git history) | 40,969 | 28 | 2m29s |
| 2 | Hygiene Auditor | Initial hygiene sweep | 92,665 | 56 | 4m12s |
| 3 | (research) | Verify Claude Code subagent frontmatter spec | 59,099 | 7 | 0m33s |
| 4 | Editor — orchestration team | Genericize 11 agents + templates | 184,992 | 160 | 18m45s |
| 5 | Editor — advisory board | Genericize 10 agents + templates | 123,868 | 133 | 8m03s |
| 6 | Editor — writing team | Genericize 5 agents + fix roster links | 55,204 | 29 | 3m16s |
| 7 | Editor — TTRPG team | Genericize 17 agents + fix links/count | 111,176 | 73 | 8m43s |
| 8 | Hygiene Auditor | Tier 1 hygiene gate | 63,245 | 38 | 3m17s |
| 9 | Editor — docs | Genericize architecture/loop/board docs | 55,841 | 38 | 3m50s |
| 10 | Editor — contributing | Fix CONTRIBUTING + authoring schema | 32,865 | 16 | 1m41s |
| 11 | Editor — examples | Genericize the board-review example | 38,744 | 31 | 1m55s |
| 12 | Security Engineer | Final leak re-sweep | 37,058 | 27 | 1m57s |
| 13 | Hygiene Auditor | Final full-repo hygiene sweep | 94,902 | 120 | 5m09s |
| 14 | Code Reviewer | Integration + technical-accuracy review | 106,492 | 34 | 2m40s |
| 15 | Editor — remediation | Fix the findings from the gates | 53,954 | 57 | 2m46s |
| 16 | Hygiene Auditor | Hygiene gate on the Verdant example | 40,388 | 25 | 2m16s |
| | **Totals** | **16 spawns** | **1,191,462** | **872** | **~71m cumulative** |

*(Tiers 1 — rows 4–7 — and Tier 2 — rows 9–11 — were issued in parallel, so wall-clock was far less than the ~71m cumulative agent runtime. Row 4 alone ran ~19 minutes.)*

## What this demonstrates

**Context isolation, measured.** Those **1,191,462 tokens** and **872 tool calls** were processed inside **subagent windows**. What crossed back into the Orchestrator's own window was only the report blocks — **roughly 13,000 tokens of report text** (estimated from the returned messages). So on the order of **~99% of the run's token processing never entered the coordinating window**; the Orchestrator carried the plan and the summaries, not the work.

**The task was too big for one window.** ~1.19M tokens of processing is multiples of any single context window. A monolithic agent attempting this run would have hit compaction repeatedly — lossy summarization mid-task, the exact "stale context" failure this repo exists to prevent. The Orchestrator's window stayed in the low tens of thousands throughout and never compacted.

**Right-sized models, in practice.** The two leak sweeps, the integration review, and the hygiene gates ran on capable models where correctness mattered; the bulk genericization editing ran on cheaper specialists. The expensive tier was spent where it bought something.

**Parallelism.** Rows 4–7 (four team-genericization editors) ran concurrently, as did rows 9–11. That is the wall-clock "streamline development" win, orthogonal to tokens.

## What's metered vs. estimated

The credibility of a ledger is in being honest about its instrument.

- **Metered (exact, harness-reported):** every per-subagent token count, tool-call count, and duration in the table; the 1,191,462 / 872 totals.
- **Estimated (labeled as such):** the ~13,000 tokens of returned report text (measured from the text of the report blocks, not a separate meter); the resulting ~99% / ~90× isolation figure therefore inherits that estimate.
- **Not measurable here:** the Orchestrator's own main-thread peak context (Claude Code does not expose a live readout of the parent window's size — "low tens of thousands" is an estimate from what it actually held); the input/output/cached split within each subagent's total (only the total is reported).

No number here is inflated to flatter the thesis. The honest headline is the **metered** one: *16 isolated windows, ~1.19M tokens, ~872 tool calls — coordinated from a single window that never compacted.*

## Sanitization

This run operated only on the **public** `Agents-Public` repository, so there is almost nothing to sanitize: the table reports agent **roles**, **token counts**, and **task descriptions**, never the contents of any private project. (The subagents' briefs internally referenced a sanitization policy that names private projects; those names are not reproduced here — only what each agent *did* and what it *cost*.)

## Relation to the Verdant walkthrough

- [`../orchestrated-run/`](../orchestrated-run/) — *fictional, illustrative.* Shows the **mechanism**: dependency graph, tiers, file-ownership, a clean per-window model. Easy to follow.
- This file — *real, metered.* Shows the **cost**: what the mechanism actually consumed on a genuine, large, multi-agent run.

Read the walkthrough to understand the loop; read this to believe the token argument.
