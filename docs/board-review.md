# Advisory Board Review

The advisory board is a standing panel of 10 specialist agents. They evaluate projects from distinct vantage points — financial, technical, market, product, security, legal, and operational. Together they produce a weighted **Readiness Score** from 1 to 10.

The board reviews, scores, and recommends. It does not implement. Implementation is the orchestration team's responsibility.

---

## Board Members

| # | Agent | Role | Domain | Model | Weight |
|---|-------|------|--------|-------|--------|
| 1 | Alexandra | CFO | Financial Viability | Opus | 15% |
| 2 | Marcus | CMO | Market & Positioning | Sonnet | 10% |
| 3 | Priya | CPO | Product Strategy | Opus | 10% |
| 4 | Dr. Reyes | CTO | Technical Architecture | Opus | 10% |
| 5 | Sophie | UI/UX | Design & Experience | Sonnet | 10% |
| 6 | Chen | Code Auditor | Quality & Debt | Sonnet | 10% |
| 7 | Jordan | Gap Analyst | Competitive Intel | Sonnet | 10% |
| 8 | Kai | DevOps/SRE | Reliability & Operations | Sonnet | 10% |
| 9 | Viktor | CSO | Security & Risk | Opus | 10% |
| 10 | Evelyn | Legal | Compliance & Risk | Opus | 5% |

---

## Scoring Domains and Weights

| Domain | Board Members | Combined Weight |
|--------|--------------|-----------------|
| Technical Foundation | Dr. Reyes (CTO) + Chen (Code Auditor) | 20% |
| Market Readiness | Marcus (CMO) + Jordan (Gap Analyst) | 20% |
| Product Quality | Priya (CPO) + Sophie (UI/UX) | 20% |
| Business Viability | Alexandra (CFO) | 15% |
| Security & Risk | Viktor (CSO) | 10% |
| Infrastructure | Kai (DevOps/SRE) | 10% |
| Legal & Compliance | Evelyn (Legal) | 5% |

---

## Readiness Score Formula

Each board member assigns a score from 1 to 10 for their domain. The weighted Readiness Score is:

```
Score = (CTO × 0.10) + (Auditor × 0.10) + (CMO × 0.10) + (Gaps × 0.10)
      + (CPO × 0.10) + (UX × 0.10) + (CFO × 0.15) + (CSO × 0.10)
      + (DevOps × 0.10) + (Legal × 0.05)
```

Note: the total weights sum to 1.00. CTO and Code Auditor each carry 10% and together cover the Technical Foundation domain at 20%. The CFO carries Business Viability alone at 15%, reflecting the weight of financial sustainability as a standalone gate.

### Score Legend

| Range | Interpretation |
|-------|---------------|
| 1–2 | Proof of concept — significant foundational work required before evaluation |
| 3–4 | Early alpha — core concept exists but major gaps across multiple domains |
| 5–6 | Beta — functional, investable, but not ready for broad launch |
| 7–8 | Near market-ready — minor gaps; targeted remediation before launch |
| 9 | Market-ready — strong across all domains; normal launch risk |
| 10 | Exceptional — best-in-class execution; uncommon |

A score of 9 or 10 does not mean perfect. It means the board has no blocking concerns and the project is ready for the next stage. Gaps still exist — they are just not blocking.

---

## Per-Domain Rubric

Each board member scores against their own rubric, which is defined in their persona file. Common rubric dimensions:

**Alexandra (CFO):** Unit economics, runway, cost structure, revenue model, financial controls.

**Marcus (CMO):** Market positioning, ICP clarity, differentiation, go-to-market readiness, messaging.

**Priya (CPO):** Product-market fit signal, roadmap coherence, feature prioritization, user feedback loops.

**Dr. Reyes (CTO):** Architecture soundness, scalability, technical debt load, engineering practices, build vs. buy decisions.

**Sophie (UI/UX):** User flow clarity, accessibility, design consistency, onboarding experience, friction points.

**Chen (Code Auditor):** Code quality, test coverage, dependency hygiene, documentation, maintainability.

**Jordan (Gap Analyst):** Competitive landscape, feature gaps, positioning blind spots, substitution risk.

**Kai (DevOps/SRE):** Deployment reliability, observability, incident response readiness, infrastructure maturity.

**Viktor (CSO):** Threat model completeness, vulnerability surface, secrets management, data protection.

**Evelyn (Legal):** Licensing compliance, terms of service, data handling obligations, regulatory exposure.

---

## How a Review Run Works

### Inputs

The board receives a project context package. This typically includes:

- A description of the project, its current stage, and the review's purpose
- Any materials the maintainer wants to share (architecture diagrams, positioning docs, prior review findings)
- Owner responses to the previous review cycle (if this is a re-review)

Owner responses are read first by every board member before they score. An intentional design decision that looks like a gap is different from an unrecognized one — context changes how a finding is weighted.

### Independent review

Each board member reviews independently. They do not see each other's scores or findings before completing their own review. This prevents anchoring and groupthink.

Each member produces an `[AGENT REVIEW]` block following the template in `advisory-board/templates/agent-review.md`. The review includes:

- A score (1–10) for their domain
- Key findings (strengths and gaps)
- Recommendations (actionable, prioritized)
- Confidence level in their assessment

### Consolidation

After all 10 reviews are complete, a consolidation pass produces the board report:

- The weighted Readiness Score computed from all 10 individual scores
- Consensus findings — items where multiple board members independently raised the same concern
- Conflicts — items where board members disagree and why
- Top 3 actions — the highest-priority items across the full board
- Score delta — if this is a re-review, the change from the prior cycle

The consolidated report template is in `advisory-board/templates/consolidated-report.md`.

### Handoff to implementation

The consolidated report is the primary input for an implementation run. Nadia reads it and maps every finding to a node in the Change Dependency Graph. The reconciliation matrix at the end of implementation maps every finding back to either IMPLEMENTED, PARTIAL, DEFERRED, or SCOPE CREEP — closing the loop between board review and implementation.

After implementation, the board can re-review and produce a score delta: the change in Readiness Score attributable to the implementation cycle.

---

## Review Cadence

The board is designed for periodic, structured review — not continuous monitoring. A typical pattern:

1. **Initial review:** board evaluates the project cold. Produces baseline score and findings.
2. **Owner response:** the maintainer documents which findings they agree with, which they contest, and their plans.
3. **Implementation cycle:** orchestration team addresses the highest-priority findings.
4. **Re-review:** board evaluates the updated project. Score delta shows what moved and by how much.

There is no fixed cadence — it depends on the pace of changes. A fast-moving project might review monthly; a stable project quarterly or before major releases.

---

## See Also

- Individual agent personas: `advisory-board/agents/`
- Review templates: `advisory-board/templates/`
- Worked example: `examples/sample-review/`
