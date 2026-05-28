# Sample Advisory Board Review — Lumina (Fictional Example)

> Fictional example for illustration — not a real project, company, or person.

---

This directory contains a worked example of the advisory board review process applied to a fictional open-source project called **Lumina**.

Lumina is an imaginary open-source Markdown note-taking application: a desktop app with local-first storage, optional end-to-end encrypted sync, and a plugin system for custom renderers. It has no affiliation with any real product or company.

The purpose of this example is to show:

1. What an individual agent review looks like in practice (see `dr-reyes-review.md` and `alexandra-review.md`)
2. How individual scores are consolidated into a weighted Readiness Score (see `consolidated-report.md`)
3. The level of specificity and actionability expected in advisory board findings

---

## Files in This Directory

| File | Contents |
|------|----------|
| `README.md` | This file — context and explanation |
| `dr-reyes-review.md` | Dr. Reyes (CTO) review of Lumina |
| `alexandra-review.md` | Alexandra (CFO) review of Lumina |
| `consolidated-report.md` | Partial consolidated report with weighted Readiness Score |

Note: only two of the ten board members are shown here. A full review would include all ten agents.

---

## About the Scoring

The weighted Readiness Score formula from `docs/board-review.md`:

```
Score = (CTO × 0.10) + (Auditor × 0.10) + (CMO × 0.10) + (Gaps × 0.10)
      + (CPO × 0.10) + (UX × 0.10) + (CFO × 0.15) + (CSO × 0.10)
      + (DevOps × 0.10) + (Legal × 0.05)
```

In the `consolidated-report.md`, all ten agent scores are shown (including illustrative scores for the eight agents not fully written out in this example). The full formula is applied to compute a final score.

---

## Using This Example

- Read `dr-reyes-review.md` to understand the depth and structure expected from a technical board member.
- Read `alexandra-review.md` to see how the CFO perspective differs from the CTO's — same project, different concerns.
- Read `consolidated-report.md` to see how conflicts and consensus emerge across multiple independent reviewers, and how the weighted formula is applied.

When authoring your own agents, use these examples as a calibration target for specificity and tone.
