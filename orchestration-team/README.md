# Orchestration Team

The implementation counterpart to the Advisory Board. Where the board reviews and scores, this team builds. The Orchestrator leads an implementation run — it never writes code, it coordinates, sequences, and gates the result with one deterministic check.

> **What's validated vs. optional.** The recommended core is small: a Change Dependency Graph, context isolation via subagents, and **one deterministic verification check** (typecheck / test suite / build) — with a single agent as the default until a task outgrows one context window. The richer machinery here — the full roster of finely-differentiated specialists, the Swarm/Director cross-team layer, and the extra gate battery (per-tier hygiene sweep, keyword-triggered security review, smoke gate, LLM code-review pass) — was **never validated in a controlled test** and is offered as optional scaffolding, not as mandatory process. See [../FINDINGS.md](../FINDINGS.md).

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

**The Orchestrator** is the principal engineer orchestrator and the center of the validated core. It builds a Change Dependency Graph (CDG) before any specialist writes a line of code, groups changes into tiers, forwards each tier's finalized state to the next, and gates the integrated result with one deterministic check before the human review package.

**The Swarm (optional, unvalidated)** is the cross-team director. As designed, it coordinates when multiple independent workstreams run in parallel (a web app, an API service, a CLI tool — each in its own Orchestrator team), or when a board review feeds into an implementation cycle. This cross-team layer was never validated in a controlled test; for a single-project implementation — and for most work — invoke the Orchestrator directly without the Swarm.

**The specialists** are each invoked by the Orchestrator as their domain is needed. Distinct roles are useful for *consistency and predictability* — you can reason about what each will focus on — but the finely-differentiated roster is scaffolding, not a validated source of value. The Code Reviewer (LLM review) and Hygiene Auditor passes are **optional add-ons**, not mandatory; they do not replace the deterministic check, which is the one validated gate.

---

## How It Works

**The isolation problem solved (validated):** When many changes are needed that could impact each other, the Orchestrator builds a Change Dependency Graph before any code is written. Changes are grouped into tiers — only truly independent changes run in parallel. Each tier's finalized output becomes the explicit input context for the next tier. No specialist ever works with stale information about what another specialist changed. This dependency-ordered finalized-state-forwarding is the mechanism that was validated (0/3 → 3/3 on integration correctness).

The validated flow:

```
Orchestrator reads brief → explores codebase → builds CDG → plans tiers
       ↓
Tier 1 (parallel): independent changes, each specialist in its own context window
       ↓  (integration snapshot — Tier 1's FINALIZED state — passed down)
Tier 2 (sequential): dependent changes receive Tier 1's finalized state directly
       ↓
ONE deterministic verification check (typecheck / test suite / build — exit code is the gate)
       ↓
Orchestrator: reconciliation matrix + human review package
       ↓
Human approval → commit
```

**Optional add-on gates (unvalidated, off by default):** layered on top of the flow above if you find them useful — a per-tier keyword scan that auto-invokes the Security Engineer on auth/secrets changes, a Test Engineer smoke gate that probes a live surface before a tier is accepted, a per-tier Hygiene Auditor sweep, and an LLM Code Reviewer pass on specialist output. None of these was validated in a controlled test, and none substitutes for the deterministic check above (an LLM review is an opinion; the deterministic check is a fact). A live drill for redundancy-class changes (HA, failover, DR, backup restore — baseline → induce failure → verify failover → restore) is an optional smoke-gate variant in the same category.

**Key invariants (validated core):**
1. The Orchestrator coordinates the run — it sequences and gates, it does not write code
2. No file touched by two specialists in the same tier
3. Tier N specialists receive Tier N-1's finalized state as explicit context (not a guess)
4. The integrated result passes **one deterministic check** (typecheck / test suite / build) before human review
5. Max 3 iterations per task — then escalate to human
6. Nothing is committed without human approval

**Optional, unproven add-ons (not invariants):** the original design treated several extra gates as mandatory — a Hygiene Auditor sweep after *every* tier plus a final cross-tier sweep, a mandatory Phase 2.5 smoke gate on any infra/deploy/public-surface/redundancy tier, a Code Reviewer pass on all Opus-model output, and a keyword-scan that auto-invokes the Security Engineer. None of these was validated in a controlled test. Keep them as optional knobs, not requirements; the deterministic check (invariant 4) is the one validated guardrail. See [../FINDINGS.md](../FINDINGS.md).

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
