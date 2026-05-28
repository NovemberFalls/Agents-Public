---
template: specialist-report
version: 1
---

# Specialist Report — [SPECIALIST] / Tier [N]
**Returning to:** [Atlas (if Opus) | Nadia (if Sonnet)]
**Date:** [YYYY-MM-DD]
**Project:** [project]
**Task brief reference:** [task identifier]

---

## Status

**Status:** COMPLETE | BLOCKED | PARTIAL

*(If BLOCKED or PARTIAL: describe exactly what is blocking you and what you need. Do not speculate or try to work around — return immediately so Nadia can make the decision.)*

---

## Model Used

**Model:** [Opus | Sonnet]
**Rationale:** [Why this model was used — confirm it matches what Nadia specified, or explain deviation]

---

## Files Modified

| File | Lines Changed | Summary of Change |
|------|--------------|-----------------|
| [path] | [e.g., 42–67, 103–105] | [one-line description] |
| [path] | [lines] | [description] |

**Files read but not modified:**
- [path]: [why read — e.g., "confirmed API interface hadn't changed"]

---

## Integration Context Compliance

**This section is mandatory — Nadia will reject reports that omit it.**

For each item in the Integration Context section of the task brief:

| Previous-Tier Change | My Compliance | Evidence |
|---------------------|--------------|---------|
| [change described in brief] | ✅ Compliant | [specific evidence — e.g., "line 87: uses `Depends(require_auth)` not `request.session.get('user')`"] |
| [change described in brief] | ✅ Compliant | [specific evidence] |

*(If any item is non-compliant: mark ❌ and explain why — this will result in REVISE from Atlas or Nadia)*

---

## Changes Summary

[Clear, precise description of what was changed and why. Not a repeat of the task — a description of the implementation decisions made.]

**Key decisions:**
- [Decision 1]: [why this approach over alternatives]
- [Decision 2]: [why]

---

## Adversarial Test (Security tasks only — Zara)

[Description of re-exploitation attempt with fix in place, and why it now fails]

---

## Potential Regression Points

[What could this change break that was previously working? Be specific. Atlas will check these explicitly.]

- [risk 1]: [how it's mitigated or why it's acceptable]
- [risk 2]: [how it's mitigated]

*(If none: state "No regression risk identified" with brief justification)*

---

## What Sam Should Test

[Specific test cases Sam must write. These are requirements, not suggestions.]

**Regression tests (must be RED before this change, GREEN after):**
1. [specific scenario and assertion]
2. [specific scenario and assertion]

**New behavior tests (GREEN only after this change):**
1. [specific scenario and assertion]

**Negative/error path tests:**
1. [specific scenario — e.g., "unauthenticated WebSocket connection attempt returns 401"]

---

## Integration Notes for Other Specialists

[Anything a downstream specialist (Tier N+1) needs to know about how this change affects their work. Nadia will include this in their task brief.]

---

## Open Questions

[Anything unresolved that requires Nadia's decision. Do not make assumptions — return with the question.]

1. [question]: [context, why it matters, options considered]

*(If none: state "No open questions")*

---

## Self-Assessment

**Confidence level:** HIGH | MEDIUM | LOW
**Reason:** [Why this confidence level — be honest. Low confidence is not penalized; undisclosed low confidence that causes a later failure is.]

**Would benefit from:** [Anything that would increase confidence — e.g., "Sam testing the WebSocket auth path since I can't run the full PTY stack in this context"]
