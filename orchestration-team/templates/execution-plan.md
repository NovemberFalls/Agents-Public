---
template: execution-plan
version: 1
---

# Execution Plan — [PROJECT] / [SCOPE]
**Date:** [YYYY-MM-DD]
**Requested by:** [human | /orchestrate | /fix]
**Audit reference:** [path to consolidated-report.md]
**Orchestrator:** Reviewing and signing

---

## Scope Summary

**In scope:** [what will be implemented in this run]
**Out of scope:** [explicitly deferred — with reason]
**Audit findings addressed:** [N of M total findings]

---

## Change Inventory

| # | Change | Files Touched | Audit Finding | Priority |
|---|--------|--------------|---------------|----------|
| 1 | [description] | [file list] | [finding reference] | P0/P1/P2 |
| 2 | [description] | [file list] | [finding reference] | P0/P1/P2 |
| ... | | | | |

---

## Change Dependency Graph

```
[file/component A] ←depends on── [file/component B]
[file/component C] ←depends on── [file/component B]
[file/component D] ──independent
```

Dependencies identified:
- Change [N] must precede Change [M] because: [reason — e.g., M modifies server.py which imports from the file N modifies]
- Change [X] and Change [Y] are independent — can parallelize

---

## Execution Tiers

### Tier 1 — Parallel (no inter-dependencies)

| Specialist | Task | Files | Model | Rationale |
|-----------|------|-------|-------|-----------|
| [name] | [task] | [files] | [Opus/Sonnet] | [why this model] |
| [name] | [task] | [files] | [Opus/Sonnet] | [why this model] |

*Code Reviewer reviews after: [list of Opus specialists in this tier]*

### Tier 2 — Sequential (requires Tier 1 complete)

*Integration context passed from Tier 1: [list of files whose post-Tier-1 state is passed as input]*

| Specialist | Task | Files | Model | Rationale |
|-----------|------|-------|-------|-----------|
| [name] | [task] | [files] | [Opus/Sonnet] | [why this model] |

*Code Reviewer reviews after: [list of Opus specialists in this tier]*

### Tier [N] — [Parallel/Sequential]

*... repeat as needed ...*

### Final Tier — Testing (always last)

| Specialist | Task | Coverage |
|-----------|------|---------|
| Test Engineer | Write/update tests for all changes | [list what needs testing] |

---

## File Ownership Matrix

*No file should appear in more than one column in any single tier.*

| File | Tier 1 Owner | Tier 2 Owner | Tier 3 Owner |
|------|-------------|-------------|-------------|
| [file] | [specialist] | — | — |
| [file] | — | [specialist] | — |

**Conflicts detected:** [none | list with resolution]

---

## Risk Assessment

| Risk | Likelihood | Mitigation |
|------|-----------|-----------|
| [risk] | [H/M/L] | [how the Orchestrator is handling it] |

---

## Estimated Iteration Surface

Tiers: [N]
Specialists: [list]
Code Reviewer reviews required: [N Opus tasks]
Approximate rounds if clean: [N]
Early stop conditions: [what would cause the Orchestrator to halt and escalate to human]

---

## Human Approval Gate

**This plan requires human approval before Tier 1 begins** if any of the following are true:
- [ ] Any change has a blast radius > 5 files
- [ ] Any irreversible change (database migration, file deletion, config overwrite)
- [ ] Any change to auth or security systems
- [ ] Scope is ambiguous or audit reference is missing

**The Orchestrator's assessment:** [proceed | pause for human approval]
