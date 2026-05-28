# TTRPG Design Team — Session Protocol

Defines how the team runs sessions, produces findings, and routes them to the right agents.

---

## Session Types

### Type 1 — Expert Audit (no play required)
**Who:** Aldric, Morrigan, Sylvara, Vance
**What:** Read the system content. Produce gap reports.
**When:** Triggered on system content update or new rules content added.
**Output:** Gap reports → routed to Lyra (rule text), Vesper (AP costs), Oryn (magic trees)

### Type 2 — Build Submission
**Who:** Skar, Cipher
**What:** Submit an optimized or exploit build with proof.
**When:** Triggered after system content is stable enough to build against.
**Output:** Build report → routed to Lyra (fix), Thane (encounter counter), Vesper (cost audit), Oryn (tree audit if magic)

### Type 3 — Party Session
**Who:** Bram, Talia, Roz, Dane (party) + Holt or Vex (GM)
**What:** Run a session at a given level with 1-2 combat encounters and 1 social/skill encounter.
**When:** Scheduled per level bracket — 1, 3, 5, 8, 10, 13, 15, 18, 20.
**Output:** Full combat log (see [combat-log-format.md](combat-log-format.md)) + per-player session reports + GM session report

### Type 4 — Build Stress Test
**Who:** Vex (GM) + Skar/Cipher build as the "party"
**What:** Vex runs the broken build against Thane's encounter counter.
**When:** After Skar/Cipher submit a build AND Thane submits a counter.
**Output:** Counter validation report → back to Thane and Lyra

### Type 5 — VTT Feature Audit
**Who:** Petra
**What:** Audit each VTT feature as it ships against Foundry/Roll20 benchmarks.
**When:** After each VTT milestone.
**Output:** Feature audit + missing features list → VTT backlog

---

## Party Character Roster

The party plays fixed characters across all sessions. Characters level up between level bracket sessions.

| Player | Character | Build Focus |
|--------|-----------|-------------|
| Bram | Bronn Ashvale | Two-handed martial, story-first |
| Talia | Kira | Fire evoker, newcomer build |
| Roz | Sel | Ranged archer, D&D-convert build |
| Dane | Evander | Healer/face, support focus |

Characters are updated with expertise investments after each level bracket session. Players choose their own advancement.

---

## Routing Map

Every finding routes to the right person:

| Finding Type | Primary | Secondary |
|-------------|---------|-----------|
| Exploit / broken build | Lyra (rule fix) | Thane (encounter counter), Vesper (cost) |
| Rule ambiguity | Lyra | — |
| AP cost wrong | Vesper | Lyra (text fix) |
| Magic tree imbalance | Oryn | Vesper |
| D&D gap | Aldric → Lyra | — |
| WFRP gap | Morrigan → Lyra | — |
| PF2e comparison | Sylvara → Vesper | — |
| DC20 comparison | Vance → Vesper | — |
| GM tooling gap | Thane | Holt session logs |
| Player feel issue | Direct to project owner | — |
| VTT UX gap | Petra | Talia session reports |
| Rules confusion (player) | Lyra | — |

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
  [YYYY-MM-DD]-[skar|cipher]-[exploit-name].md
```
