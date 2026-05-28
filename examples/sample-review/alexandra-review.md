# Alexandra — CFO Review: Lumina

> Fictional example for illustration — not a real project, company, or person.

---

```
[AGENT REVIEW]
Agent: Alexandra
Role: CFO — Financial Viability
Project: Lumina (fictional open-source Markdown note-taking app)
Review cycle: Initial
Score: 5 / 10
Confidence: Medium (open-source project; limited financial documentation available)
```

---

## Summary

Lumina is a well-built open-source tool without a financial model. That is a deliberate choice, and not inherently wrong — many open-source projects operate sustainably on volunteer contribution and sponsorship. But Lumina's maintainer has stated an intent to offer a hosted sync service as an optional paid feature, and that intent brings financial sustainability questions into scope.

The current picture: zero revenue, indeterminate operating costs, no pricing model, and an optional sync feature that is the implied monetization path but is not yet ready for production. The project is sustainable today because it has no real costs. It will not be sustainable once sync infrastructure is running.

This is a project that needs a business model alongside its architecture, and the business model work has not started.

---

## Strengths

**Open-source as a distribution moat.** The decision to open-source the core is strategically sound for a note-taking tool. Trust is the primary purchase criterion in this category — users store their personal and professional data in these tools. Open-source code is auditable, which is a genuine differentiator against closed-source competitors. This lowers user acquisition cost and increases retention if the product is good.

**Low cost baseline.** The local-first architecture means the product can serve its core value proposition — offline Markdown editing with a clean plugin system — with minimal infrastructure cost. The project can run for years on minimal or no revenue before the sync feature requires real infrastructure.

**Optional sync as a viable monetization path.** The "pay for sync" model is proven in this category. Users who care about cross-device access will pay for it; users who only need local storage get the tool for free. The segmentation is natural and does not penalize the primary use case.

---

## Gaps

### Gap 1 — No pricing model for sync (severity: HIGH)

The sync feature is described as "optional paid" in the project roadmap, but there is no pricing model: no proposed price point, no tier structure, no consideration of whether pricing will be per-user, per-device, or storage-based. A pricing decision is not a small decision — it signals who the product is for, and the wrong price will suppress adoption of the one feature that funds the project.

**Recommendation:** Define a pricing model before the sync feature launches. At minimum: the monthly price, the storage limit (if any), and the device limit (if any). Research comparable tools in the category and position deliberately, not arbitrarily.

### Gap 2 — No infrastructure cost modeling (severity: HIGH)

The sync feature requires server infrastructure. There is no analysis of what that infrastructure costs at different user scales. This matters because the sync feature cannot launch at a price point that is sustainable unless someone has modeled the unit economics: what does one active sync user cost per month to serve?

Without this analysis, the team may launch sync at a price that works at 100 users and loses money at 10,000 users, or — equally problematic — price it so high that adoption is suppressed.

**Recommendation:** Before setting a sync price, model the infrastructure cost per active user at three scales: 100, 1,000, and 10,000 monthly active sync users. Use this model to derive the minimum price per user required to break even, then price with that floor as a constraint.

### Gap 3 — Contribution sustainability (severity: MEDIUM)

Open-source projects fail financially not because they cannot monetize but because they cannot retain contributors. The project currently has three active contributors including the primary maintainer. There is no contributor compensation model, no sponsorship program, and no explicit plan for how the project sustains engineering capacity as the maintainer's available time changes.

**Recommendation:** Evaluate GitHub Sponsors or an equivalent sponsorship mechanism. Even modest monthly sponsorships create financial signal and give the maintainer visible recognition for their work. Over time, sponsorships can fund part-time contributor bounties for specific features.

### Gap 4 — No financial reporting baseline (severity: LOW)

If the project accepts sponsorships or subscription revenue, it will need basic financial reporting: revenue, costs, allocation of funds. There is no current infrastructure for this (which is appropriate for a zero-revenue project). But the infrastructure should be designed before revenue arrives, not after.

**Recommendation:** Decide now whether the project will operate as an individual maintainer, a fiscal sponsor arrangement, or a formal entity. Each has different overhead and different options for accepting and distributing funds. The decision is low-stakes today and high-stakes once there is revenue to manage.

---

## Financial Viability Score

| Dimension | Assessment | Weight |
|-----------|-----------|--------|
| Revenue model | Exists in concept (sync subscription); not designed in detail | |
| Unit economics | No infrastructure cost model for the intended paid feature | |
| Runway | Open-source; costs are near-zero today, non-trivial once sync runs | |
| Cost structure | Light and appropriate for current stage | |
| Financial controls | Not yet needed; will be needed before revenue | |

**Score: 5 / 10**

The score reflects that the project has a plausible path to financial sustainability but has not done the work to validate it. The monetization concept is sound; the execution is not designed. A 1-point increase would require a pricing model and infrastructure cost model. A 2-point increase would require both of those plus evidence that the pricing model generates enough revenue to cover operating costs at a realistic user scale.

---

## Top Recommendations

1. (HIGH) Model sync infrastructure cost per active user before setting a price.
2. (HIGH) Define the sync pricing model before the feature launches.
3. (MEDIUM) Evaluate GitHub Sponsors or equivalent to begin building financial sustainability.
4. (LOW) Decide on the project's legal/financial structure before revenue arrives.

```
[/AGENT REVIEW]
```
