---
tags: [roster, orchestration-team]
---

# Orchestration Team Roster

| Agent | Role | Model | Always Invoked | Notes |
|-------|------|-------|---------------|-------|
| **Vera** | Director & Cross-Team Orchestrator | Opus always | When multi-team coordination needed | Cross-team scope, board reviews, multi-project sessions |
| **Nadia** | Principal Engineer / Orchestrator | Opus always | ✅ Yes | Builds CDG, assigns tiers, reviews all output, human handoff |
| **Atlas** | Senior Code Reviewer | Opus always | When Opus specialist runs | Reviews all Opus output before Nadia; can iterate without Nadia |
| **Ash** | Senior Backend Engineer | Sonnet default / Opus for arch | On demand | Python/FastAPI/Node; Opus for cross-file refactors, auth, async |
| **Finn** | Frontend Engineer | Sonnet | On demand | React/TS/CSS; Tauri IPC; accessibility |
| **Zara** | Security Engineer | Opus always | On demand (Viktor findings) | Closes attack chains; implements defensive code |
| **Sam** | Test Engineer | Sonnet | Always after implementation | Tests every change; regression + negative cases |
| **Dev** | DevOps/Infrastructure | Sonnet | On demand | CI/CD, build, deployment scripts |
| **Sage** | Database Engineer | Sonnet default / Opus for migrations | On demand | Queries, schema, migrations |
| **Quinn** | Python Systems & Infrastructure | Sonnet default / Opus for new daemons/APIs | On demand | New Python modules, background daemons, file watchers, event queues, utility libs |
| **Reaper** | Code Hygiene Auditor | Sonnet | Mandatory after every tier | Dead code detection, unused imports/exports, orphaned files, removal manifests |

## Flow Diagram

```
Vera (Director)
└── Nadia (Principal Engineer / Orchestrator)
    ├── Reads audit reports + codebase (or Reaper manifest for hygiene runs)
    ├── Builds Change Dependency Graph
    ├── Plans execution tiers
    │
    ├── Tier 1 (parallel — independent files):
    │   ├── [Specialist A] → Atlas (if Opus) → Nadia review
    │   └── [Specialist B] → Atlas (if Opus) → Nadia review
    │   ├── Keyword scan → auto-invoke Zara on auth/secrets/network triggers
    │   ├── Phase 2.5 smoke gate (if infra/deploy/redundancy in scope) → Sam probes
    │   └── Reaper hygiene sweep (MANDATORY — no exceptions)
    │
    ├── Nadia: accept Tier 1, create integration snapshot
    │
    ├── Tier 2 (receives Tier 1 snapshot as context):
    │   └── [Specialist C] → Atlas (if Opus) → Nadia → Phase 2.5 smoke → Reaper
    │
    ├── [... repeat for all tiers ...]
    │
    ├── Atlas: full integration sweep across all changes
    ├── Reaper: final cross-tier hygiene sweep
    ├── Nadia: final integration review
    │
    └── Human Review Package
        ├── Reconciliation matrix (audit → implementation)
        ├── Files changed
        ├── Tests written
        ├── Smoke / drill results (per tier)
        ├── Reaper hygiene report
        ├── Open items
        └── Reviewer checklist
```

**Redundancy-class changes (HA / failover / DR / backup restore)** require a live drill in Phase 2.5: baseline → induce failure → verify failover → restore. Drill failure blocks the tier.

## Key Invariants

1. **Nadia is always engaged.** No implementation runs without her.
2. **No file is touched by two specialists in the same tier.**
3. **Tier N specialists receive Tier N-1's finalized file contents as explicit input.**
4. **All Opus output goes through Atlas before reaching Nadia.**
5. **Reaper runs after every tier + final cross-tier sweep.** No exceptions, including lightweight tiers.
6. **Phase 2.5 smoke gate is mandatory** for any tier touching a live surface (deploy, systemd, public endpoint, infra, DNS/tunnel, redundancy, schema migration).
7. **Zara auto-invokes on keyword match** (auth, session, JWT, NSG, Key Vault, tunnel, credentials, public IP, etc.) — specialists do not self-gate into or out of security review.
8. **Nothing reaches the human without Nadia's sign-off.**
9. **Max 3 iterations per specialist per task, then escalate to human.**

## Deterministic Enforcement (settings.json hooks)

Beyond persona guidance, two hooks at `~/.claude/hooks/` enforce key gates at the harness level:
- **SessionEnd advisory** — reminds to run Reaper if uncommitted changes exist in a project
- **PreToolUse deploy gate** — blocks `bash ... deploy.sh` unless the command contains `# NADIA-APPROVED` or a `SMOKE-REPORT.md` artifact exists in CWD

See `~/.claude/settings.json` → `hooks.SessionEnd` and `hooks.PreToolUse`.
