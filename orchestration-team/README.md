# Orchestration Team

The implementation counterpart to the Advisory Board. Where the board reviews and scores, this team builds. The Swarm coordinates across projects and board sessions; the Orchestrator leads every implementation run — it never writes code, it coordinates, sequences, and reviews.

---

## Team

| Agent | Role | Model | Profile |
|-------|------|-------|---------|
| **Swarm** | Director & Cross-Team Orchestrator | Opus | [00-swarm.md](agents/00-swarm.md) |
| **Orchestrator** | Principal Engineer / Orchestrator | Opus always | [01-orchestrator.md](agents/01-orchestrator.md) |
| **Code Reviewer** | Senior Code Reviewer | Opus always | [02-reviewer.md](agents/02-reviewer.md) |
| **Backend Engineer** | Backend Engineer (Python/FastAPI/Node) | Sonnet / Opus | [03-backend-engineer.md](agents/03-backend-engineer.md) |
| **Frontend Engineer** | Frontend Engineer (React/TS/CSS) | Sonnet | [04-frontend-engineer.md](agents/04-frontend-engineer.md) |
| **Security Engineer** | Security Engineer | Opus always | [05-security-engineer.md](agents/05-security-engineer.md) |
| **Test Engineer** | Test Engineer | Sonnet | [06-test-engineer.md](agents/06-test-engineer.md) |
| **DevOps Engineer** | DevOps / Infrastructure | Sonnet | [07-devops-engineer.md](agents/07-devops-engineer.md) |
| **Database Engineer** | Database Engineer | Sonnet / Opus (migrations) | [08-database-engineer.md](agents/08-database-engineer.md) |
| **Systems Engineer** | Python Systems & Infra | Sonnet / Opus (new daemons) | [09-systems-engineer.md](agents/09-systems-engineer.md) |
| **Hygiene Auditor** | Code Hygiene Auditor | Sonnet | [10-hygiene-auditor.md](agents/10-hygiene-auditor.md) |

All agents are spawned via Claude Code's native `Agent` tool using `subagent_type` (registered at `~/.claude/agents/`). Each spawn is synchronous: the task brief goes inline in the prompt; the specialist's final message is the completion report.

---

## Team Structure

**The Swarm** is the cross-team director. It coordinates when multiple independent workstreams need to run in parallel (e.g., a web app, an API service, a CLI tool — each in its own Orchestrator team), or when an advisory board review feeds into an implementation cycle. For a single-project implementation, you can invoke the Orchestrator directly without the Swarm.

**The Orchestrator** is the principal engineer orchestrator. It is always the first agent engaged for any implementation run. It builds a Change Dependency Graph (CDG) before any specialist writes a line of code, groups changes into tiers, and coordinates all specialists through to the human review package.

**The 9 specialists** (Code Reviewer through Hygiene Auditor) are each invoked by the Orchestrator as their domain is needed. The Code Reviewer reviews Opus-model output before it reaches the Orchestrator. The Hygiene Auditor runs hygiene sweeps after every tier — mandatory, no exceptions.

---

## How It Works

**The isolation problem solved:** When many changes are needed that could impact each other, the Orchestrator builds a Change Dependency Graph before any code is written. Changes are grouped into tiers — only truly independent changes run in parallel. Each tier's finalized output becomes the explicit input context for the next tier. No specialist ever works with stale information about what another specialist changed.

```
Board Review (advisory board) → consolidated findings
       ↓
Orchestrator reads findings → builds CDG → plans tiers
       ↓
Tier 1 (parallel): independent changes → Code Reviewer review → Orchestrator review
       ↓  (per-tier keyword scan: auto-invoke Security Engineer on auth/secrets/network changes)
       ↓  (Phase 2.5 smoke gate: Test Engineer probes live surface if infra/deploy/redundancy in scope)
       ↓  (Hygiene Auditor sweep — MANDATORY, no exceptions)
       ↓  (integration snapshot passed down)
Tier 2 (sequential): dependent changes → Code Reviewer → Orchestrator → Phase 2.5 smoke → Hygiene Auditor
       ↓
Test Engineer: tests for all changes
       ↓
Code Reviewer: full integration sweep
       ↓
Hygiene Auditor: final cross-tier hygiene sweep
       ↓
Orchestrator: reconciliation matrix + human review package
       ↓
Human approval → commit
```

**Redundancy-class changes (HA, failover, DR, backup restore) require a live drill in Phase 2.5** — baseline → induce failure → verify failover → restore. A drill failure blocks the tier regardless of code-review outcome.

**Key invariants:**
1. The Orchestrator is always engaged — no implementation without it
2. No file touched by two specialists in the same tier
3. Tier N specialists receive Tier N-1's finalized state as explicit context
4. All Opus output reviewed by the Code Reviewer before reaching the Orchestrator
5. The Hygiene Auditor runs after every tier and a final cross-tier sweep — no exceptions, including lightweight tiers
6. Phase 2.5 smoke gate runs on any tier with infra / deploy / public surface / redundancy in scope
7. The Security Engineer is auto-invoked by keyword scan (auth, secrets, NSG, Key Vault, tunnel, etc.) — specialists do not self-gate
8. Max 3 iterations per task — then escalate to human
9. Nothing is committed without human approval

---

## Commands

| Command | When to Use |
|---------|-------------|
| `/orchestrate [project] [scope]` | Multiple findings, coordinated changes, any security work |
| `/fix [project] [issue]` | Single issue, ≤3 files, no downstream dependencies |

---

## Templates

| Template | Purpose |
|----------|---------|
| [execution-plan.md](templates/execution-plan.md) | The Orchestrator's tier plan — produced before any code is written |
| [task-brief.md](templates/task-brief.md) | What the Orchestrator gives each specialist |
| [specialist-report.md](templates/specialist-report.md) | What specialists return to the Orchestrator/Code Reviewer |
| [code-review.md](templates/code-review.md) | The Code Reviewer's APPROVED/REVISE review |
| [reconciliation-matrix.md](templates/reconciliation-matrix.md) | Final human-facing output |
| [task-file.md](templates/task-file.md) | Owner-authored task description for the Orchestrator |
| [project-brain-template.md](agents/project-brain-template.md) | The Swarm's per-project shared-context snapshot — eliminates redundant codebase exploration across runs |

---

## Relationship to Advisory Board

The advisory board reviews and scores. This team implements. The handoff is explicit: the Orchestrator reads the board's consolidated report as its primary input. The reconciliation matrix maps every implementation back to a board finding. After implementation, the next board review cycle will re-score and verify the delta.

**Advisory board → findings → orchestration team → implementation → board re-review → score delta**
