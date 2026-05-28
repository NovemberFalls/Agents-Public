# Orchestration Team

The implementation counterpart to the Advisory Board. Where the board reviews and scores, this team builds. Vera coordinates across projects and board sessions; Nadia leads every implementation run — she never writes code, she coordinates, sequences, and reviews.

---

## Team

| Agent | Role | Model | Profile |
|-------|------|-------|---------|
| **Vera** | Director & Cross-Team Orchestrator | Opus | [00-vera-director.md](agents/00-vera-director.md) |
| **Nadia** | Principal Engineer / Orchestrator | Opus always | [01-nadia-orchestrator.md](agents/01-nadia-orchestrator.md) |
| **Atlas** | Senior Code Reviewer | Opus always | [02-atlas-reviewer.md](agents/02-atlas-reviewer.md) |
| **Ash** | Backend Engineer (Python/FastAPI/Node) | Sonnet / Opus | [03-ash-backend.md](agents/03-ash-backend.md) |
| **Finn** | Frontend Engineer (React/TS/CSS) | Sonnet | [04-finn-frontend.md](agents/04-finn-frontend.md) |
| **Zara** | Security Engineer | Opus always | [05-zara-security.md](agents/05-zara-security.md) |
| **Sam** | Test Engineer | Sonnet | [06-sam-tester.md](agents/06-sam-tester.md) |
| **Dev** | DevOps / Infrastructure | Sonnet | [07-dev-devops.md](agents/07-dev-devops.md) |
| **Sage** | Database Engineer | Sonnet / Opus (migrations) | [08-sage-database.md](agents/08-sage-database.md) |
| **Quinn** | Python Systems & Infra | Sonnet / Opus (new daemons) | [09-quinn-systems.md](agents/09-quinn-systems.md) |
| **Reaper** | Code Hygiene Auditor | Sonnet | [10-reaper-hygiene.md](agents/10-reaper-hygiene.md) |

All agents are spawned via Claude Code's native `Agent` tool using `subagent_type` (registered at `~/.claude/agents/`). Each spawn is synchronous: the task brief goes inline in the prompt; the specialist's final message is the completion report.

---

## Team Structure

**Vera** is the cross-team director. She coordinates when multiple independent workstreams need to run in parallel (e.g., a web app, an API service, a CLI tool — each in its own Nadia team), or when an advisory board review feeds into an implementation cycle. For a single-project implementation, you can invoke Nadia directly without Vera.

**Nadia** is the principal engineer orchestrator. She is always the first agent engaged for any implementation run. She builds a Change Dependency Graph (CDG) before any specialist writes a line of code, groups changes into tiers, and coordinates all specialists through to the human review package.

**The 9 specialists** (Atlas through Reaper) are each invoked by Nadia as their domain is needed. Atlas reviews Opus-model output before it reaches Nadia. Reaper runs hygiene sweeps after every tier — mandatory, no exceptions.

---

## How It Works

**The isolation problem solved:** When many changes are needed that could impact each other, Nadia builds a Change Dependency Graph before any code is written. Changes are grouped into tiers — only truly independent changes run in parallel. Each tier's finalized output becomes the explicit input context for the next tier. No specialist ever works with stale information about what another specialist changed.

```
Board Review (advisory board) → consolidated findings
       ↓
Nadia reads findings → builds CDG → plans tiers
       ↓
Tier 1 (parallel): independent changes → Atlas review → Nadia review
       ↓  (per-tier keyword scan: auto-invoke Zara on auth/secrets/network changes)
       ↓  (Phase 2.5 smoke gate: Sam probes live surface if infra/deploy/redundancy in scope)
       ↓  (Reaper hygiene sweep — MANDATORY, no exceptions)
       ↓  (integration snapshot passed down)
Tier 2 (sequential): dependent changes → Atlas → Nadia → Phase 2.5 smoke → Reaper
       ↓
Sam: tests for all changes
       ↓
Atlas: full integration sweep
       ↓
Reaper: final cross-tier hygiene sweep
       ↓
Nadia: reconciliation matrix + human review package
       ↓
Human approval → commit
```

**Redundancy-class changes (HA, failover, DR, backup restore) require a live drill in Phase 2.5** — baseline → induce failure → verify failover → restore. A drill failure blocks the tier regardless of code-review outcome.

**Key invariants:**
1. Nadia is always engaged — no implementation without her
2. No file touched by two specialists in the same tier
3. Tier N specialists receive Tier N-1's finalized state as explicit context
4. All Opus output reviewed by Atlas before reaching Nadia
5. Reaper runs after every tier and a final cross-tier sweep — no exceptions, including lightweight tiers
6. Phase 2.5 smoke gate runs on any tier with infra / deploy / public surface / redundancy in scope
7. Zara is auto-invoked by keyword scan (auth, secrets, NSG, Key Vault, tunnel, etc.) — specialists do not self-gate
8. Max 3 iterations per task — then escalate to human
9. Nothing is committed without human approval

---

## Commands

| Command | When to Use |
|---------|-------------|
| `/dev-implement [project] [scope]` | Multiple findings, coordinated changes, any security work |
| `/dev-fix [project] [issue]` | Single issue, ≤3 files, no downstream dependencies |

---

## Templates

| Template | Purpose |
|----------|---------|
| [execution-plan.md](templates/execution-plan.md) | Nadia's tier plan — produced before any code is written |
| [task-brief.md](templates/task-brief.md) | What Nadia gives each specialist |
| [specialist-report.md](templates/specialist-report.md) | What specialists return to Nadia/Atlas |
| [atlas-review.md](templates/atlas-review.md) | Atlas's APPROVED/REVISE review |
| [reconciliation-matrix.md](templates/reconciliation-matrix.md) | Final human-facing output |
| [task-file.md](templates/task-file.md) | Owner-authored task description for Nadia |
| [project-brain-template.md](agents/project-brain-template.md) | Vera's per-project shared-context snapshot — eliminates redundant codebase exploration across runs |

---

## Relationship to Advisory Board

The advisory board reviews and scores. This team implements. The handoff is explicit: Nadia reads the board's consolidated report as her primary input. The reconciliation matrix maps every implementation back to a board finding. After implementation, the next board review cycle will re-score and verify the delta.

**Advisory board → findings → orchestration team → implementation → board re-review → score delta**
