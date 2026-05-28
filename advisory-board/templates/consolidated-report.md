---
project: "{{PROJECT}}"
review_date: "{{YYYY-MM-DD}}"
version: "{{VERSION_OR_COMMIT}}"
readiness_score: 0
previous_score: null
tags: [consolidated, review, "{{PROJECT}}"]
---

# {{PROJECT}} — Board Review
**Date:** {{YYYY-MM-DD}} | **Version:** {{VERSION_OR_COMMIT}}
**Readiness Score: {{SCORE}} / 10** | **Previous: {{PREV_SCORE}}** | **Δ {{CHANGE}}**

---

## Review Team

| Agent | Role | Score | Model |
|-------|------|-------|-------|
| [Alexandra](../agents/01-alexandra-cfo.md) | CFO | {{score}} / 10 | Opus |
| [Marcus](../agents/02-marcus-cmo.md) | CMO | {{score}} / 10 | Sonnet |
| [Priya](../agents/03-priya-cpo.md) | CPO | {{score}} / 10 | Opus |
| [Dr. Reyes](../agents/04-dr-reyes-cto.md) | CTO | {{score}} / 10 | Opus |
| [Sophie](../agents/05-sophie-uiux.md) | UI/UX | {{score}} / 10 | Sonnet |
| [Chen](../agents/06-chen-auditor.md) | Code Auditor | {{score}} / 10 | Sonnet |
| [Jordan](../agents/07-jordan-gaps.md) | Gap Analyst | {{score}} / 10 | Sonnet |
| [Kai](../agents/08-kai-devops.md) | DevOps/SRE | {{score}} / 10 | Sonnet |
| [Viktor](../agents/09-viktor-cso.md) | CSO | {{score}} / 10 | Opus |
| [Evelyn](../agents/10-evelyn-legal.md) | Legal | {{score}} / 10 | Opus |

---

## Readiness Score Calculation

| Domain | Agent(s) | Weight | Score | Weighted |
|--------|----------|--------|-------|---------|
| Technical Foundation | CTO + Code Auditor | 20% | {{avg}} | {{weighted}} |
| Market Readiness | CMO + Gap Analyst | 20% | {{avg}} | {{weighted}} |
| Product Quality | CPO + UI/UX | 20% | {{avg}} | {{weighted}} |
| Business Viability | CFO | 15% | {{score}} | {{weighted}} |
| Security & Risk | CSO | 10% | {{score}} | {{weighted}} |
| Infrastructure | DevOps | 10% | {{score}} | {{weighted}} |
| Legal & Compliance | Legal | 5% | {{score}} | {{weighted}} |
| **TOTAL** | | **100%** | | **{{FINAL_SCORE}}** |

**Score Interpretation:**
- 1–4: Not yet viable for public/paying users
- 5–6: Beta — functional but not ready for revenue
- 7–8: Near-ready — specific gaps remain
- 9–10: Market-ready to exceptional

---

## Executive Brief

> *3–5 sentences synthesizing the board's collective view. What is the honest state of this product? What is the most important thing to address? What is genuinely impressive?*

---

## Owner Responses on Record

*Context provided by the project owner prior to this review. Agents have read these — this section confirms what strategic context was in scope when scores were given.*

*If no owner-responses.md exists for this project, write: "No owner responses on file for this review cycle."*

| Response | Source Finding | Owner Position | Acknowledged By |
|----------|---------------|----------------|-----------------|
| [Brief summary of owner response] | [Agent, date] | [Intent / correction / context] | [Agents who factored this in] |

> *Owner responses do not override agent findings. Where an agent's conclusion differs from the owner's stated intent, the agent's reasoning is preserved in their individual review file.*

---

## Consensus Findings

*Issues or strengths where 3+ agents independently flagged the same concern or strength.*

### Consensus Strengths
- **[Title]:** [Description] — flagged by [Agent A, Agent B, Agent C]
- **[Title]:** [Description] — flagged by [Agent A, Agent B]

### Consensus Risks
> [!danger] [Title]
> **Flagged by:** [Agent A, Agent B, Agent C]
> **Summary:** [Description of the cross-domain issue]
> **Combined impact:** [Why multiple domains flagging this amplifies the risk]

---

## Cross-Agent Conflicts

*Where agents disagree. These require owner judgment to resolve.*

### Conflict 1: [Topic]
- **[Agent A]'s view:** [Position]
- **[Agent B]'s view:** [Position]
- **Synthesis:** [How to think about resolving this tension]
- **Recommended resolution:** [Owner should decide X based on Y]

---

## Top 10 Action Items

*Cross-domain priorities, ordered by combined impact × urgency. Each maps to at least one agent recommendation.*

| # | Action | Domain(s) | Effort | Agents |
|---|--------|-----------|--------|--------|
| 1 | [Action description] | [Domain] | [S/M/L] | [Agent(s)] |
| 2 | [Action description] | [Domain] | [S/M/L] | [Agent(s)] |
| 3 | [Action description] | [Domain] | [S/M/L] | [Agent(s)] |
| 4 | [Action description] | [Domain] | [S/M/L] | [Agent(s)] |
| 5 | [Action description] | [Domain] | [S/M/L] | [Agent(s)] |
| 6 | [Action description] | [Domain] | [S/M/L] | [Agent(s)] |
| 7 | [Action description] | [Domain] | [S/M/L] | [Agent(s)] |
| 8 | [Action description] | [Domain] | [S/M/L] | [Agent(s)] |
| 9 | [Action description] | [Domain] | [S/M/L] | [Agent(s)] |
| 10 | [Action description] | [Domain] | [S/M/L] | [Agent(s)] |

---

## Competitive Landscape (Aggregated)

*Compiled from Marcus (CMO) and Jordan (Gap Analyst) reviews.*

### Direct Competitors

| Product | Company | Positioning | Notable Strength | Our Advantage | Source |
|---------|---------|-------------|-----------------|---------------|--------|
| [Name] | [Company] | [Tagline/angle] | [What they do well] | [How we compare] | [URL] |

### Feature Gap Summary

| Capability | This Product | Market Leaders | Gap Severity |
|-----------|--------------|----------------|-------------|
| [Feature] | ✅/❌/⚠️ | ✅ | Critical/Notable/Acceptable |

### Market Opportunity

*Where is there white space competitors are not occupying that this product could own?*

---

## Score History

| Date | Score | Key Change |
|------|-------|------------|
| {{YYYY-MM-DD}} | {{SCORE}} | Initial review |

---

## Next Review Trigger

*What milestone, date, or event should trigger the next review cycle?*

- [ ] [Milestone: e.g., Phase 9 complete, first paying customer, public launch]
- [ ] [Date: e.g., 30 days from this review]
- [ ] [Event: e.g., significant architecture change, new competitor launch]

---

## Agent Review Links

| Agent | Review File |
|-------|-------------|
| Alexandra (CFO) | [Full Review](alexandra-cfo.md) |
| Marcus (CMO) | [Full Review](marcus-cmo.md) |
| Priya (CPO) | [Full Review](priya-cpo.md) |
| Dr. Reyes (CTO) | [Full Review](dr-reyes-cto.md) |
| Sophie (UI/UX) | [Full Review](sophie-uiux.md) |
| Chen (Auditor) | [Full Review](chen-auditor.md) |
| Jordan (Gaps) | [Full Review](jordan-gaps.md) |
| Kai (DevOps) | [Full Review](kai-devops.md) |
| Viktor (CSO) | [Full Review](viktor-cso.md) |
| Evelyn (Legal) | [Full Review](evelyn-legal.md) |
