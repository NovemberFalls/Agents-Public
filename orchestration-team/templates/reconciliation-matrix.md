---
template: reconciliation-matrix
version: 1
---

# Implementation Reconciliation Matrix — [PROJECT]
**Date:** [YYYY-MM-DD]
**Scope:** [what was implemented]
**Audit reference:** [path to consolidated-report.md]
**Signed off by:** Nadia

---

## Readiness Score Delta

| Score | Source | Date |
|-------|--------|------|
| [X.X] | Board review (before implementation) | [audit date] |
| [estimated delta] | Nadia's post-implementation assessment | [today] |

*Note: Estimated delta is Nadia's projection. Next board review will produce an official updated score.*

---

## Reconciliation Matrix

### Implemented ✅

| # | Audit Finding | Agent | Finding Priority | Implementation | File:Line | Verified By |
|---|--------------|-------|-----------------|---------------|-----------|------------|
| 1 | [finding text] | [agent] | P0/P1/P2 | [what was done] | [file:line] | [Atlas / Nadia] |
| 2 | [finding text] | [agent] | P0/P1/P2 | [what was done] | [file:line] | [Atlas / Nadia] |

### Partially Implemented ⚠️

| # | Audit Finding | What Was Done | What Remains | Reason for Gap |
|---|--------------|--------------|-------------|----------------|
| 1 | [finding] | [partial impl] | [remaining work] | [reason — scope, dependency, etc.] |

### Deferred ❌

| # | Audit Finding | Agent | Priority | Reason for Deferral | Next Sprint |
|---|--------------|-------|----------|--------------------|-|
| 1 | [finding] | [agent] | P1/P2 | [explicit reason] | [yes/no/unknown] |

### Scope Creep 🔍

| # | Change Made | Justification | Reviewed By | Approved |
|---|------------|--------------|-------------|---------|
| 1 | [description] | [why it was necessary] | [Atlas / Nadia] | [yes/no] |

*(Scope creep requires explicit justification. Any change not traceable to an audit finding must appear here.)*

---

## Files Changed

| File | Change Type | Lines Δ | Specialist | Tier |
|------|------------|---------|-----------|------|
| [path] | [add/modify/delete] | [+N/-M] | [name] | [N] |

**Total files modified:** [N]
**Net lines changed:** [+N/-M]

---

## Tests Written / Modified

| File | Tests Added | Tests Modified | Covers |
|------|------------|---------------|--------|
| [path] | [N] | [N] | [brief description] |

**Test suite status:** [all passing / N failing — list]

---

## Open Items

Things not resolved in this implementation run that require future attention:

| # | Item | Urgency | Notes |
|---|------|---------|-------|
| 1 | [description] | [H/M/L] | [context] |

---

## Human Reviewer Checklist

Before approving this implementation, please verify:

- [ ] **P0 findings** — [list of P0 findings implemented] — spot-check the code at the cited file:line
- [ ] **Auth changes** (if any) — test the happy path and the rejection path manually
- [ ] **Scope creep** items — are you comfortable with additions made beyond the audit scope?
- [ ] **Deferred items** — are you OK with these being deferred? (change urgency rating if not)
- [ ] **Test suite** — confirm all tests pass (`[test command]`)
- [ ] **Manual smoke test** — [specific scenario to test manually, e.g., "launch the app, create a session, verify it appears in the session list"]

**If approved: [commit instructions]**
**If changes needed: [how to request revisions]**

---

## Nadia's Sign-Off

**Implementation complete:** [yes / no — reason if no]
**Quality assessment:** [summary — honest assessment of the implementation quality]
**Recommended next sprint:** [what should be tackled in the next /dev-implement run, based on remaining deferred items and any new findings from this implementation]
