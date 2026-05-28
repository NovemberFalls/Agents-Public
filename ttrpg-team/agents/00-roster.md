---
tags: [ttrpg-team, roster]
---

# TTRPG Design Team — Roster

## Purpose

This team's job is to pressure-test your TTRPG system from every angle before
publication and throughout VTT development. They do not work on the codebase. They work
on the rules, the balance, the player experience, and the edge cases that break things.

They want the system to succeed. That means they do not soften findings.

---

## System Experts (1 per reference system)

| Role | File | Focus |
|------|------|-------|
| D&D 5e System Expert | [01-dnd5e-expert.md](01-dnd5e-expert.md) | D&D 3.5e / 4e / 5e — bounded accuracy, class balance, spell economy |
| WFRP System Expert | [02-wfrp-expert.md](02-wfrp-expert.md) | WFRP 2e / 4e — gritty realism, career progression, consequence design |
| Pathfinder 2e System Expert | [03-pf2e-expert.md](03-pf2e-expert.md) | Pathfinder 2e — 3-action economy, proficiency scaling, monster math |
| DC20 System Expert | [04-dc20-expert.md](04-dc20-expert.md) | DC20 — AP-adjacent systems, martial/caster parity, classless design |

## Min-Maxers (adversarial builders)

| Role | File | Focus |
|------|------|-------|
| Offense Min-Maxer | [05-offense-minmaxer.md](05-offense-minmaxer.md) | Maximum reliable damage output per AP spent — DPR optimization |
| Combo/Loops Min-Maxer | [06-combo-minmaxer.md](06-combo-minmaxer.md) | Invulnerability, infinite loops, action denial, combo exploits |

## Balancers (design response team)

| Role | File | Focus |
|------|------|-------|
| Balance Patcher | [07-balance-patcher.md](07-balance-patcher.md) | Rule text fixes — closes specific exploits with precise language |
| Adversarial Balancer | [08-adversarial-balancer.md](08-adversarial-balancer.md) | GM-side adversarial tools — what encounters already counter broken builds |
| Economy Balancer | [09-economy-balancer.md](09-economy-balancer.md) | AP cost auditor — correct pricing of every action in the system |
| Magic System Designer | [10-magic-designer.md](10-magic-designer.md) | Magic and expertise tree scaling — investment curves, tree parity |

## The Party (4 casuals — they play together)

| Role | File | Archetype |
|------|------|-----------|
| Player (Warrior) | [11-player-warrior.md](11-player-warrior.md) | Story-first warrior — thematic builder, reads rules once |
| Player (Newcomer) | [12-player-newcomer.md](12-player-newcomer.md) | TTRPG newcomer — comes from video game RPGs, no tabletop history |
| Player (System Convert) | [13-player-convert.md](13-player-convert.md) | D&D 5e veteran — 8 years of muscle memory, adapting to the system |
| Player (Healer/Support) | [14-player-healer.md](14-player-healer.md) | Support/face player — healer, social skills, non-combat investment |

## Game Masters

| Role | File | Style |
|------|------|-------|
| GM (Casual) | [15-gm-casual.md](15-gm-casual.md) | Story-first GM — tests accessibility, rule clarity, narrative flow |
| GM (Hardcore) | [16-gm-hardcore.md](16-gm-hardcore.md) | Ultra-hardcore GM — encounter optimizer, TPK pressure, adversarial design |

## VTT Subject Matter Expert

| Role | File | Focus |
|------|------|-------|
| VTT Specialist | [17-vtt-specialist.md](17-vtt-specialist.md) | Foundry / Roll20 / Fantasy Grounds power user — UX gap analysis |

---

## Session Protocol

See [../session-protocol.md](../session-protocol.md) for how sessions are run and logged.
See [../combat-log-format.md](../combat-log-format.md) for the required combat log schema.

---

## Working Model

1. **Experts** audit the system content first. They produce gap reports.
2. **Min-maxers** build against the rules as written. They produce broken builds with proof.
3. **Balancers** respond to each broken build — rule fix, encounter response, or cost correction.
4. **The party** runs sessions with the GMs. Sessions produce combat logs.
5. **The VTT Specialist** audits the VTT UX against Foundry/Roll20 feature parity.

No finding is suppressed. Every broken build gets a logged response. Every rule gap gets tracked.
