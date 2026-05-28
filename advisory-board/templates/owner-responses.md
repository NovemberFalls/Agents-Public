---
project: "{{PROJECT}}"
last_updated: "{{YYYY-MM-DD}}"
tags: [owner-responses, "{{PROJECT}}"]
---

# Owner Responses — {{PROJECT}}

This file is read by all board agents **before** they begin their review. It provides strategic context, corrections, and clarifications from the project owner that should inform how findings are interpreted and scored.

**How agents should use this:**
- Owner responses do not override your independent assessment
- They DO change how you interpret intentional gaps vs. unrecognized ones
- If a response is directly relevant to your domain, acknowledge it in your review
- If a response contradicts what you observe in the code, flag the discrepancy — don't silently accept it
- **An owner saying "I'm not doing this" is not a resolution.** Continue to flag unresolved findings at their original severity until the underlying risk is actually gone. Owner deferral is context, not a close. If a finding is deferred repeatedly, escalate urgency — do not reduce it.

---

## Project-Level Context

*Strategic intent, constraints, and non-obvious context that applies to all agents across all reviews.*

> *[Example: This project is not intended to generate revenue. Its primary goal is brand awareness and demonstrating technical capability. Score business viability relative to this goal, not against a SaaS revenue benchmark.]*

---

## Responses to Prior Findings

*Specific responses to concerns raised in previous board reviews. Each response is linked to its source.*

### [YYYY-MM-DD] — [Finding Title]

**Source:** [agent-slug(s)] in [YYYY-MM-DD] review
**Original concern:** [One sentence summarizing what the board flagged]

**Owner response:**
[Explanation, correction, or strategic context. Be specific — vague responses do not help agents recalibrate.]

**What to evaluate next cycle:**
[What should the board check to see if this response holds up, was implemented, or the concern was valid despite the response]

---

*Add additional responses below using the same structure. Oldest responses at the bottom; most recent at the top.*
