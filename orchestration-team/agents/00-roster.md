---
tags: [orchestration-team, roster]
---

# Orchestration Team Roster

| Agent | Role | Model | Always Invoked | Notes |
|-------|------|-------|---------------|-------|
| **[Orchestrator](01-orchestrator.md)** | Principal Engineer / Orchestrator | Opus always | ✅ Yes | Builds CDG, assigns tiers, reviews all output, human handoff |
| **[Code Reviewer](02-reviewer.md)** | Senior Code Reviewer | Opus always | When Opus specialist runs | Reviews all Opus output before the Orchestrator; can iterate without the Orchestrator |
| **[Backend Engineer](03-backend-engineer.md)** | Senior Backend Engineer | Sonnet default / Opus for arch | On demand | Python/FastAPI/Node; Opus for cross-file refactors, auth, async |
| **[Frontend Engineer](04-frontend-engineer.md)** | Frontend Engineer | Sonnet | On demand | React/TS/CSS; Tauri IPC; accessibility |
| **[Security Engineer](05-security-engineer.md)** | Security Engineer | Opus always | On demand (CSO Advisor findings) | Closes attack chains; implements defensive code |
| **[Test Engineer](06-test-engineer.md)** | Test Engineer | Sonnet | Always after implementation | Tests every change; regression + negative cases |
| **[DevOps Engineer](07-devops-engineer.md)** | DevOps/Infrastructure | Sonnet | On demand | CI/CD, build, deployment scripts |
| **[Database Engineer](08-database-engineer.md)** | Database Engineer | Sonnet default / Opus for migrations | On demand | Queries, schema, migrations |
| **[Systems Engineer](09-systems-engineer.md)** | Python Systems & Infrastructure | Sonnet default / Opus for new daemons/APIs | On demand | New Python modules, background daemons, file watchers, event queues, utility libs |
| **[Hygiene Auditor](10-hygiene-auditor.md)** | Code Hygiene Auditor | Sonnet | Optional (unvalidated) | Dead code detection, unused imports/exports, orphaned files, removal manifests |

## Flow Diagram

```
Orchestrator (Principal Engineer / Orchestrator)   # top of the core flow; the optional Swarm/Director layer lives in extras/
    ├── Reads audit reports + codebase (or Hygiene Auditor manifest for hygiene runs)
    ├── Builds Change Dependency Graph
    ├── Plans execution tiers
    │
    ├── Tier 1 (parallel — independent files):
    │   ├── [Specialist A] → Code Reviewer (if Opus) → Orchestrator review
    │   └── [Specialist B] → Code Reviewer (if Opus) → Orchestrator review
    │   ├── Keyword scan → auto-invoke Security Engineer on auth/secrets/network triggers
    │   ├── Phase 2.5 smoke gate (if infra/deploy/redundancy in scope) → Test Engineer probes
    │   └── Hygiene Auditor sweep (optional)
    │
    ├── Orchestrator: accept Tier 1, create integration snapshot
    │
    ├── Tier 2 (receives Tier 1 snapshot as context):
    │   └── [Specialist C] → Code Reviewer (if Opus) → Orchestrator → Phase 2.5 smoke → Hygiene Auditor
    │
    ├── [... repeat for all tiers ...]
    │
    ├── Code Reviewer: full integration sweep across all changes
    ├── Hygiene Auditor: final cross-tier hygiene sweep
    ├── Orchestrator: final integration review
    │
    └── Human Review Package
        ├── Reconciliation matrix (audit → implementation)
        ├── Files changed
        ├── Tests written
        ├── Smoke / drill results (per tier)
        ├── Hygiene report
        ├── Open items
        └── Reviewer checklist
```

**Redundancy-class changes (HA / failover / DR / backup restore)** require a live drill in Phase 2.5: baseline → induce failure → verify failover → restore. Drill failure blocks the tier.

## Key Invariants

These are the validated rules — the small core that earned its keep (see [../../FINDINGS.md](../../FINDINGS.md)).

1. **The Orchestrator is always engaged.** No implementation runs without it; it always coordinates.
2. **No file is touched by two specialists in the same tier.**
3. **Tier N specialists receive Tier N-1's finalized file contents as explicit input.**
4. **One deterministic verification check (typecheck / test suite / build) runs before human review.** A non-zero exit blocks.
5. **Max 3 iterations per specialist per task, then escalate to human.**
6. **Nothing is committed without human approval.**

## Optional, unproven add-ons

The following are available knobs, but they are **unvalidated** — never tested in a controlled experiment, and not part of the recommended core (see [../../FINDINGS.md](../../FINDINGS.md)). The validated gate is the deterministic check above, not any of these:

- **Hygiene Auditor sweep** — an optional dead-code/hygiene pass; not required after every tier, and there is no carve-out either way since it is optional.
- **Phase 2.5 smoke gate** — an optional probe for tiers touching a live surface (deploy, systemd, public endpoint, infra, DNS/tunnel, redundancy, schema migration).
- **Code Reviewer (LLM review) pass** — an optional review of Opus output before the Orchestrator.
- **Keyword-triggered Security Engineer review** — an optional auto-invoke on auth/session/secrets/network keywords.

## Deterministic Enforcement (optional)

Beyond persona guidance, you can optionally wire deploy gates via your own Claude Code hooks (configured in your `settings.json`) to enforce key gates at the harness level. For example:
- **SessionEnd advisory** — remind to run the Hygiene Auditor if uncommitted changes exist in a project
- **PreToolUse deploy gate** — block a deploy command unless it carries an explicit approval marker or a smoke-test artifact exists

These are optional and not shipped with this repo; configure them to match your own workflow.
