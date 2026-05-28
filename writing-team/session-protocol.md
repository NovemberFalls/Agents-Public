# Writing Review Board — Session Protocol

Defines how the review board convenes, produces findings, and routes them.

---

## Session Type: Chapter Review

**Trigger**: `/review CXX` — invoked after enhance (or after draft if skipping enhance)
**Who**: All 5 agents read in parallel
**Input**: The chapter file + all relevant world context
**Output**: Consolidated review report

---

## Session Flow

### Phase 1 — Parallel Read (all agents, simultaneous)

All 5 agents read the chapter and relevant context files independently.
**Vael reads FIRST and ALONE** — her report must be uncontaminated by craft analysis.
The other 4 agents may cross-reference each other's domains but produce independent reports.

Context files loaded per review (adapt to your project's file structure):
- The chapter being reviewed (enhanced version preferred, draft if no enhance exists)
- The draft version (if both exist — for Cael's overshoot detection)
- Your project's Story State document
- Your project's Geography/Map document
- Your project's Character Tracker
- Your project's Book Map / plot outline
- Your project's POV Characters document
- Relevant character bibles for the POV character in this chapter
- Your project's Writing Rules document
- Previous chapter (for handoff validation)
- Racial/faction description files (for Wren and Morrow)

### Phase 2 — Report Generation (all agents, simultaneous)

Each agent produces their report in their specified output format.
Reports are independent — no agent reads another's report before writing their own.

### Phase 3 — Consolidation

The system produces a **Review Summary** that:
1. Lists all CRITICAL findings (from any agent) — these should be addressed
2. Lists all WARNINGS — these are judgment calls for the human
3. Notes where agents AGREE (high confidence finding)
4. Notes where agents DISAGREE (needs human resolution)
5. Gives an overall VERDICT: READY TO LOCK / REVISE FIRST / NEEDS REWRITE

---

## Routing

| Finding Type | Primary Agent | Supporting |
|-------------|---------------|------------|
| Factual contradiction | Eris | Wren (if canon) |
| Directional / geographic error | Eris | Wren |
| Character knowledge bleed | Morrow | Eris (validates) |
| Voice drift | Morrow | — |
| Dialogue mismatch | Morrow | Wren (cultural ref) |
| Pacing sag | Vael | Cael (craft diagnosis) |
| Emotional miss | Vael | Morrow (voice cause?) |
| Confusion point | Vael | Eris (continuity cause?) |
| Checklist violation | Cael | — |
| Enhance overshoot | Cael | Vael (did reader prefer draft?) |
| Canon divergence | Wren | Eris (if also internal contradiction) |
| New canon to record | Wren | — |
| Seed/payoff tracking | Eris | Cael (confirms against Book Map) |

---

## Priority Levels

| Priority | Description | Action |
|----------|-------------|--------|
| CRITICAL | Breaks continuity, violates POV rules, or contradicts established canon | Must fix before lock |
| WARNING | Reader might notice, voice drifts, or pacing sags | Human decides |
| NOTE | Minor observation, craft suggestion, or canon clarification | Optional |

---

## Output Archival

Review outputs are stored alongside the chapter. Suggested structure:

```
[Your chapters folder]/CXX/
  CXX - Title_draft.md          ← draft
  CXX - Title.md                ← enhanced/final
  CXX - Title_review.md         ← consolidated review report
```

---

## Important Constraints

- **No agent rewrites prose.** They identify issues and suggest directions. The author (Claude in session or human) decides how to fix.
- **No agent has veto power.** CRITICAL findings are strong recommendations, not blocks. The human is the final editor.
- **Vael's read is sacred.** She reads cold, without craft vocabulary, without other agents' findings. Her engagement map is the ground truth of reader experience.
- **Cael compares draft to enhanced.** If both versions exist, he must read both. The enhance pass can overcorrect — Cael is the safeguard.
- **Wren does not decide canon priority.** She reports divergences. The human decides which source wins and updates accordingly.
