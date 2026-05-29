---
tags: [advisory-board, review]
---

# Advisory Board

A standing board of 10 specialists that evaluates projects across technical, business, market, security, and legal dimensions. Each agent has a unique personality, scope, and scoring rubric. Together they produce a weighted **Readiness Score (1–10)** per project per review cycle.

---

## Board Members

| Agent | Role | Model | Weight | Profile |
|-------|------|-------|--------|---------|
| **CFO Advisor** | CFO — Financial Viability | Opus | 15% | [01-cfo-advisor.md](agents/01-cfo-advisor.md) |
| **CMO Advisor** | CMO — Market & Positioning | Sonnet | 10% | [02-cmo-advisor.md](agents/02-cmo-advisor.md) |
| **CPO Advisor** | CPO — Product Strategy | Opus | 10% | [03-cpo-advisor.md](agents/03-cpo-advisor.md) |
| **CTO Advisor** | CTO — Technical Architecture | Opus | 10% | [04-cto-advisor.md](agents/04-cto-advisor.md) |
| **UI/UX Lead** | UI/UX — Design & Experience | Sonnet | 10% | [05-uiux-lead.md](agents/05-uiux-lead.md) |
| **Code Auditor** | Code Auditor — Quality & Debt | Sonnet | 10% | [06-code-auditor.md](agents/06-code-auditor.md) |
| **Gap Analyst** | Gap Analyst — Competitive Intel | Sonnet | 10% | [07-gap-analyst.md](agents/07-gap-analyst.md) |
| **DevOps/SRE Advisor** | DevOps/SRE — Reliability | Sonnet | 10% | [08-devops-sre.md](agents/08-devops-sre.md) |
| **CSO Advisor** | CSO — Security & Risk | Opus | 10% | [09-cso-advisor.md](agents/09-cso-advisor.md) |
| **Legal Advisor** | Legal & Compliance | Opus | 5% | [10-legal-advisor.md](agents/10-legal-advisor.md) |

---

## Scoring Weights

| Domain | Agent(s) | Weight |
|--------|----------|--------|
| Technical Foundation | CTO + Code Auditor | 20% |
| Market Readiness | CMO + Gap Analyst | 20% |
| Product Quality | CPO + UI/UX | 20% |
| Business Viability | CFO | 15% |
| Security & Risk | CSO | 10% |
| Infrastructure | DevOps | 10% |
| Legal & Compliance | Legal | 5% |

**Formula:**
```
(CTO × 0.10) + (Auditor × 0.10) + (CMO × 0.10) + (Gaps × 0.10) +
(CPO × 0.10) + (UX × 0.10) + (CFO × 0.15) + (CSO × 0.10) +
(DevOps × 0.10) + (Legal × 0.05)
```

---

## How a Review Works

1. Each agent reads the project context + their own memory notebook
2. **Owner responses are loaded first** — read the owner-responses file for the current project if present; this provides strategic context agents must consider
3. Each agent completes the agent-review template, reconciling all standing issues from their memory
4. All reviews are consolidated into a single weighted board report
5. The consolidated report includes an Owner Responses section so the record is clear

**Process:** invoke each board member, then consolidate per `../board-review.md`.

---

## Owner Responses

After each audit, the owner writes an `owner-responses.md` in that audit's date folder. It lives alongside the consolidated report it's responding to.

When the next audit runs, agents read the previous date folder — they see both the consolidated report and the owner's responses together as a complete record of that cycle.

Owner responses do not override findings — but they change how gaps should be interpreted. An intentional design choice that looks like a gap is different from an unrecognized one.

See [templates/owner-responses.md](templates/owner-responses.md) for the format.

---

## Templates

| Template | Purpose |
|----------|---------|
| [agent-review.md](templates/agent-review.md) | What each agent produces per review cycle |
| [agent-memory.md](templates/agent-memory.md) | Persistent memory notebook per agent per project |
| [consolidated-report.md](templates/consolidated-report.md) | Board synthesis — weighted score, consensus, conflicts, top actions |
| [owner-responses.md](templates/owner-responses.md) | Owner context and responses to prior findings |

See [sample-review/](../sample-review/) for a worked example on a fictional project.

---

## Relationship to Implementation Teams

The advisory board reviews and scores. Implementation teams act on findings. The handoff is explicit: leads read the consolidated report as their primary input. After implementation, the next board review cycle re-scores and verifies the score delta.

**Advisory board → findings → implementation team → implementation → advisory re-review → score delta**
