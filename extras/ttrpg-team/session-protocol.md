# TTRPG Design Team — Session Protocol

Defines how the team runs sessions, produces findings, and routes them to the right agents.

---

## Session Types

### Type 1 — Expert Audit (no play required)
**Who:** D&D 5e System Expert, WFRP System Expert, Pathfinder 2e System Expert, DC20 System Expert
**What:** Read the system content. Produce gap reports.
**When:** Triggered on system content update or new rules content added.
**Output:** Gap reports → routed to Balance Patcher (rule text), Economy Balancer (AP costs), Magic System Designer (magic trees)

### Type 2 — Build Submission
**Who:** Offense Min-Maxer, Combo/Loops Min-Maxer
**What:** Submit an optimized or exploit build with proof.
**When:** Triggered after system content is stable enough to build against.
**Output:** Build report → routed to Balance Patcher (fix), Adversarial Balancer (encounter counter), Economy Balancer (cost audit), Magic System Designer (tree audit if magic)

### Type 3 — Party Session
**Who:** Player (Warrior), Player (Newcomer), Player (System Convert), Player (Healer/Support) (party) + GM (Casual) or GM (Hardcore)
**What:** Run a session at a given level with 1-2 combat encounters and 1 social/skill encounter.
**When:** Scheduled per level bracket — 1, 3, 5, 8, 10, 13, 15, 18, 20.
**Output:** Full combat log (see [combat-log-format.md](combat-log-format.md)) + per-player session reports + GM session report

### Type 4 — Build Stress Test
**Who:** GM (Hardcore) + Min-Maxer build as the "party"
**What:** The GM (Hardcore) runs the broken build against the Adversarial Balancer's encounter counter.
**When:** After a Min-Maxer submits a build AND the Adversarial Balancer submits a counter.
**Output:** Counter validation report → back to Adversarial Balancer and Balance Patcher

### Type 5 — VTT Feature Audit
**Who:** VTT Specialist
**What:** Audit each VTT feature as it ships against Foundry/Roll20 benchmarks.
**When:** After each VTT milestone.
**Output:** Feature audit + missing features list → VTT backlog

---

## Party Character Roster

The party plays fixed characters across all sessions. Characters level up between level bracket sessions.

| Player Role | Character | Build Focus |
|-------------|-----------|-------------|
| Player (Warrior) | Bronn Ashvale | Two-handed martial, story-first |
| Player (Newcomer) | Kira | Fire evoker, newcomer build |
| Player (System Convert) | Sel | Ranged archer, system-convert build |
| Player (Healer/Support) | Evander | Healer/face, support focus |

Characters are updated with expertise investments after each level bracket session. Players choose their own advancement.

---

## Routing Map

Every finding routes to the right role:

| Finding Type | Primary | Secondary |
|-------------|---------|-----------|
| Exploit / broken build | Balance Patcher (rule fix) | Adversarial Balancer (encounter counter), Economy Balancer (cost) |
| Rule ambiguity | Balance Patcher | — |
| AP cost wrong | Economy Balancer | Balance Patcher (text fix) |
| Magic tree imbalance | Magic System Designer | Economy Balancer |
| D&D gap | D&D 5e System Expert → Balance Patcher | — |
| WFRP gap | WFRP System Expert → Balance Patcher | — |
| PF2e comparison | Pathfinder 2e System Expert → Economy Balancer | — |
| DC20 comparison | DC20 System Expert → Economy Balancer | — |
| GM tooling gap | Adversarial Balancer | GM (Casual) session logs |
| Player feel issue | Direct to project owner | — |
| VTT UX gap | VTT Specialist | Player (Newcomer) session reports |
| Rules confusion (player) | Balance Patcher | — |

---

## Finding Priority Levels

| Priority | Description | Response time |
|----------|-------------|---------------|
| P0 | System-breaking exploit — character is unkillable or infinite resource loop | Immediate rule fix required before further play |
| P1 | Significantly broken — one build dramatically dominates at any level bracket | Fix before that level bracket's party session |
| P2 | Balance issue — one option is noticeably better/worse than comparable options | Fix before publication |
| P3 | Feel issue — something works but feels bad | Fix if possible before publication |
| P4 | Polish / clarity — wording is fine but could be clearer | Fix before publication if scope allows |

---

## Session Cadence

This is a design team, not a weekly game group. Sessions are run when triggered, not on a calendar.

**Trigger conditions for Type 3 party sessions:**
- System content for that level bracket is complete and stable
- No P0 or P1 findings are unresolved for that level bracket
- At least one Type 2 build submission has been reviewed at that level bracket

**Do not run party sessions against broken rules.** The party's job is to find feel issues, not to rediscover known exploits.

---

## Output Archival

All outputs are stored in your project's session archive. Suggested structure:

```
[your-project]/ttrpg-team/sessions/
  [YYYY-MM-DD]-[session-type]-[level]-[short-title]/
    combat-log.md
    [character]-report.md
    gm-report.md
    findings.md
```

All exploit findings are tracked in your project's exploit log:

```
[your-project]/ttrpg-team/exploits/
  [YYYY-MM-DD]-[offense|combo]-[exploit-name].md
```
