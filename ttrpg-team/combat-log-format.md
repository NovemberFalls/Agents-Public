# TTRPG Design Team — Combat Log Format

All simulated sessions produce a combat log following this schema exactly.
This format is required for every combat encounter. No exceptions.

---

## Header Block

```
═══════════════════════════════════════════════════════════════
COMBAT LOG — [Encounter Name]
Date: [simulation date]
Session: [Session reference ID]
GM: [Holt (Casual) | Vex (Hardcore)]
Party Level: [X]
═══════════════════════════════════════════════════════════════
PARTY:
  Bronn Ashvale (Bram)   — Human, [attribute spread]
                            HP: [current]/[max]  AP: [max]/turn
  Kira (Talia)           — [Race], [attribute spread]
                            HP: [current]/[max]  AP: [max]/turn
  Sel (Roz)              — [Race], [attribute spread]
                            HP: [current]/[max]  AP: [max]/turn
  Evander (Dane)         — [Race], [attribute spread]
                            HP: [current]/[max]  AP: [max]/turn

ENEMIES:
  [Name] (×[count])      — [Type], HP: [X], AC: [X], AP: [X]/turn
  [Name]                 — [Type], HP: [X], AC: [X], AP: [X]/turn

SETUP:
  Terrain: [Description — cover, hazards, elevation, choke points]
  Starting positions: [Brief]
  GM intent: [What the GM is trying to accomplish with this encounter]
═══════════════════════════════════════════════════════════════
```

---

## Initiative Block

```
INITIATIVE ROLL
───────────────────────────────────────────────────────────────
  [Character] — d20 ([roll]) + AGI mod ([X]) + initiative bonus ([X]) = [TOTAL]
  [Character] — d20 ([roll]) + ...
  ...

INITIATIVE ORDER (descending): [Name (total)] → [Name (total)] → ...
```

---

## Round Block (repeat per round)

```
══════════════════════════════════════════════════════════════
ROUND [N]
State: Party HP [Bram: X/Y | Talia: X/Y | Roz: X/Y | Dane: X/Y]
       Enemy HP [Enemy1: X/Y | Enemy2: X/Y]
Active conditions: [Character: condition(s) | none]
══════════════════════════════════════════════════════════════

▶ [CHARACTER NAME] — [X] AP available
  ─────────────────────────────────
  Action 1 ([X] AP): [Action description]
    → [Roll details if applicable: d20 + modifier = total vs. DC/AC]
    → [Result: HIT/MISS/SAVE/FAIL + damage/effect]
    → [Target HP: X/Y → X/Y]

  Action 2 ([X] AP): [Action description]
    → [Details]

  AP spent this turn: [X] / [max]
  AP remaining: [X] (held / expended)
  Conditions applied this turn: [none | list]
  Conditions removed this turn: [none | list]
  Resources expended: [HP | spell use | expertise ability | short rest use | none]

▶ [ENEMY NAME] — [X] AP available
  ─────────────────────────────────
  [Same format as above]
  GM tactic note: [Brief — why the GM chose this action]

[... repeat for all combatants in initiative order ...]

──────────────────────────────────────────────────────────────
END OF ROUND [N]
  Damage dealt to party: [X total] ([breakdown by source])
  Damage dealt to enemies: [X total] ([breakdown by source])
  Healing received by party: [X]
  Net party HP change: [+X / -X]
  AP efficiency (party): [X AP spent on damage] / [X AP spent on support] / [X AP spent on movement]
  Notable moments: [Conditions applied, critical hits, saves made/failed, abilities triggered]
──────────────────────────────────────────────────────────────
```

---

## Encounter Resolution Block

```
══════════════════════════════════════════════════════════════
ENCOUNTER RESOLUTION — [Round N]
Outcome: PARTY VICTORY | PARTY DEFEAT | RETREAT | STALEMATE
Rounds taken: [N]
══════════════════════════════════════════════════════════════

FINAL STATE:
  Bram HP: [X/Y] | Talia HP: [X/Y] | Roz HP: [X/Y] | Dane HP: [X/Y]
  Party members downed at any point: [list or none]
  Resources expended: [List all spell uses, expertise activations, short rest abilities used]

DAMAGE SUMMARY:
  Total damage dealt by party: [X]
  Total damage taken by party: [X]
  Ratio: [X:Y]

AP SUMMARY:
  Total party AP spent: [X]
  Breakdown: [X on attacks] / [X on spells] / [X on movement] / [X on support] / [X on abilities]
  Most AP-efficient action this encounter: [Action + AP/output ratio]
  Least AP-efficient action: [Action + why]

CONDITIONS APPLIED:
  [Condition → Target → Rounds active → Effect on outcome]

CRITICAL MOMENTS:
  [Round N] — [Event that materially changed the encounter direction]
```

---

## Post-Encounter Analysis Block

```
══════════════════════════════════════════════════════════════
POST-ENCOUNTER ANALYSIS
══════════════════════════════════════════════════════════════

GM NOTES ([Holt/Vex]):
  [What went as planned]
  [What surprised the GM]
  [Was the encounter difficulty appropriate for party level: YES | LOW | HIGH | BRUTAL]
  [Would a casual GM have the tools to design this encounter: YES | NEEDS GUIDANCE | NO]

PLAYER NOTES (per character):
  Bram: [Key observation from Bram's perspective — mechanical feel, frustration, high point]
  Talia: [Same]
  Roz: [Same]
  Dane: [Same]

BALANCE FLAGS:
  [Any action or ability that felt over/undertuned — flag to Vesper/Oryn]
  [Any condition that felt un-fun vs. appropriately threatening — flag to Lyra]
  [Any moment where the GM had no good options — flag to Thane]

RULES AMBIGUITIES ENCOUNTERED:
  [Rule that was unclear mid-encounter → How it was resolved → Flag to Lyra]
```

---

## Notes on Simulation Standards

- **Dice rolls:** Roll actual dice (or use explicit RNG) — do not assume average results except in analysis sections
- **GM intelligence:** Vex plays to win tactically. Holt plays story-first but not stupidly.
- **Resource tracking:** Track HP and AP exactly. No approximations in the log itself.
- **Spell prepared list:** Include the full prepared spell list at session start for any caster
- **Expertise abilities:** Note when tier abilities are activated — these are limited resources
- **Conditions:** Track duration explicitly per round. Do not let conditions silently expire.
