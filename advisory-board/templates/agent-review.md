---
project: "{{PROJECT}}"
agent: "{{AGENT_NAME}}"
role: "{{AGENT_ROLE}}"
date: "{{YYYY-MM-DD}}"
version: "{{VERSION_OR_COMMIT}}"
score: 0
tags: [review, "{{PROJECT}}", "{{AGENT_ROLE_TAG}}"]
---

# {{AGENT_NAME}} — {{PROJECT}} Review
**Date:** {{YYYY-MM-DD}} | **Version:** {{VERSION_OR_COMMIT}} | **Model:** {{MODEL}}

---

## Executive Summary

> *2–4 sentences. The single most important takeaway from this review. What is the state of this product from this agent's domain perspective? If someone reads nothing else, what must they know?*

---

## Strengths

> *What is genuinely working well within this domain? Be specific — credit what deserves credit.*

- **[Strength title]:** [Description with specific evidence]
- **[Strength title]:** [Description with specific evidence]
- **[Strength title]:** [Description with specific evidence]

---

## Critical Findings

> [!danger] P0 — [Finding Title]
> **What:** [Specific description of the issue]
> **Where:** [File, feature, or area of the product]
> **Risk:** [What happens if this is not addressed]
> **Recommendation:** [Specific, actionable fix]

> [!warning] P1 — [Finding Title]
> **What:** [Specific description of the issue]
> **Where:** [File, feature, or area of the product]
> **Risk:** [What happens if this is not addressed]
> **Recommendation:** [Specific, actionable fix]

*[Add additional findings as needed. Remove unused severity levels.]*

---

## Significant Gaps

*Issues that are not immediate blockers but represent meaningful risk or missed opportunity. Organized by priority.*

### Gap 1: [Title]
**Description:** [What is missing or suboptimal]
**Compared to:** [What best practice, competitor, or standard this falls short of]
**Impact:** [What this costs the product if unaddressed]
**Recommendation:** [What to do about it]

### Gap 2: [Title]
*[Repeat as needed]*

---

## Observations & Minor Findings

*Lower-priority findings, good practices that aren't quite there, and informational notes.*

> [!note] [Observation title]
> [Description]

---

## Competitor References

*Named competitors, tools, or standards referenced in this review.*

| Reference | Relevance | Source/URL |
|-----------|-----------|------------|
| [Competitor/Standard name] | [Why referenced — what they do better/differently] | [URL or "Training data"] |

---

## Recommendations — Prioritized

*Consolidated action list, ordered by impact × urgency.*

| Priority | Recommendation | Effort | Impact |
|----------|---------------|--------|--------|
| P0 | [Action] | [S/M/L] | [Critical/High/Medium] |
| P1 | [Action] | [S/M/L] | [High/Medium] |
| P2 | [Action] | [S/M/L] | [Medium/Low] |

---

## Domain Score

**Score: {{X}} / 10**

| Criteria | Weight | Score | Notes |
|----------|--------|-------|-------|
| [Domain criterion 1] | [%] | [1–10] | [Brief justification] |
| [Domain criterion 2] | [%] | [1–10] | [Brief justification] |
| [Domain criterion 3] | [%] | [1–10] | [Brief justification] |
| **Overall** | 100% | **{{X}}** | |

**Score rationale:** [2–3 sentences explaining why this score was given. What would move it up? What would move it down?]

---

## Key Question for Next Review

> *The single most important question that, if answered, would most change this score in the next cycle.*
