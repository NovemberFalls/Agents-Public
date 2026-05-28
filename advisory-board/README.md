---
tags: [advisory-board, review]
---

# Advisory Board

A standing board of 10 specialists that evaluates projects across technical, business, market, security, and legal dimensions. Each agent has a unique personality, scope, and scoring rubric. Together they produce a weighted **Readiness Score (1–10)** per project per review cycle.

---

## Board Members

| Agent | Role | Model | Weight | Profile |
|-------|------|-------|--------|---------|
| **Alexandra** | CFO — Financial Viability | Opus | 15% | [01-alexandra-cfo.md](agents/01-alexandra-cfo.md) |
| **Marcus** | CMO — Market & Positioning | Sonnet | 10% | [02-marcus-cmo.md](agents/02-marcus-cmo.md) |
| **Priya** | CPO — Product Strategy | Opus | 10% | [03-priya-cpo.md](agents/03-priya-cpo.md) |
| **Dr. Reyes** | CTO — Technical Architecture | Opus | 10% | [04-dr-reyes-cto.md](agents/04-dr-reyes-cto.md) |
| **Sophie** | UI/UX — Design & Experience | Sonnet | 10% | [05-sophie-uiux.md](agents/05-sophie-uiux.md) |
| **Chen** | Code Auditor — Quality & Debt | Sonnet | 10% | [06-chen-auditor.md](agents/06-chen-auditor.md) |
| **Jordan** | Gap Analyst — Competitive Intel | Sonnet | 10% | [07-jordan-gaps.md](agents/07-jordan-gaps.md) |
| **Kai** | DevOps/SRE — Reliability | Sonnet | 10% | [08-kai-devops.md](agents/08-kai-devops.md) |
| **Viktor** | CSO — Security & Risk | Opus | 10% | [09-viktor-cso.md](agents/09-viktor-cso.md) |
| **Evelyn** | Legal & Compliance | Opus | 5% | [10-evelyn-legal.md](agents/10-evelyn-legal.md) |

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

**Commands:** `/board-review-project [project]` · `/board-review [project] [agent]` · `/board-consolidate [project]`

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

See [examples/sample-review/](../examples/sample-review/) for a worked example on a fictional project.

---

## Relationship to Implementation Teams

The advisory board reviews and scores. Implementation teams act on findings. The handoff is explicit: leads read the consolidated report as their primary input. After implementation, the next board review cycle re-scores and verifies the score delta.

**Advisory board → findings → implementation team → implementation → advisory re-review → score delta**
