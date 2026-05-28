---
template: code-review
version: 1
---

# Code Review — [SPECIALIST] / Tier [N]

[CODE REVIEW]
**Reviewer:** Code Reviewer
**Date:** [YYYY-MM-DD]
**Project:** [project]
**Specialist report reviewed:** [specialist role, task identifier]

---

## Verdict

**VERDICT: APPROVED | REVISE**

*(If REVISE: Required Changes section must be completed. If APPROVED: confirm each check passed below.)*

---

## 1. Correctness vs. Task Brief

**Result:** PASS | FAIL

[Did the implementation do exactly what the task brief specified? Quote the task brief's "Done looks like" statement and evaluate against it.]

---

## 2. API Contract Integrity

**Result:** PASS | FAIL

[Were all call sites updated? Check: renamed functions, changed signatures, new required parameters, changed return types. List specific locations checked.]

Locations verified:
- [file:line]: [what was checked, result]

*(If PASS: "No API contract changes detected, or all call sites verified updated.")*

---

## 3. Integration Context Compliance

**Result:** PASS | FAIL

[Cross-check the specialist's "Integration Context Compliance" table against the task brief's "Integration Context" section. Are the claimed compliance points accurate? Did the specialist actually use the new APIs from previous tiers?]

Specific check:
- [integration requirement from brief] → [what specialist said] → [Code Reviewer's verification: match/mismatch]

---

## 4. Regression Risk

**Result:** ACCEPTABLE | CONCERN

[Enumerate specific regression risks. For each risk the specialist identified, evaluate whether the mitigation is sufficient. Add any risks the specialist missed.]

- [risk]: [assessment]
- [risk]: [assessment]

---

## 5. Security Flags (for non-Security-Engineer specialists)

**Result:** NONE | FLAG

[Any new user-controlled input entering an unsafe context? New public endpoint without auth? Secret logged? This is not a full security review — flag obvious issues for the Security Engineer's awareness.]

*(If NONE: "No new security surface identified.")*

---

## 6. Test Coverage

**Result:** ADEQUATE | INSUFFICIENT

[Did the specialist produce a "What the Test Engineer should test" section? Are the specified tests specific enough to actually catch a regression? Are negative cases specified?]

*(If INSUFFICIENT: list what's missing from the test specification)*

---

## Required Changes (if REVISE)

**Each item must be specific, actionable, and tell the specialist exactly what to fix and where.**

1. **[Issue title]**
   - Location: [file:line]
   - Problem: [precise description]
   - Required fix: [exactly what to change]
   - Why: [why this matters — integration risk, correctness, etc.]

2. **[Issue title]**
   - Location: [file:line]
   - Problem: [precise description]
   - Required fix: [exactly what to change]
   - Why: [why this matters]

---

## Code Reviewer Notes for the Orchestrator (if escalating)

*(Only populated if iteration limit reached without resolution)*

**Impasse description:** [what was asked, what was delivered, why the Code Reviewer can't approve, what decision is needed from the Orchestrator]

[/CODE REVIEW]
