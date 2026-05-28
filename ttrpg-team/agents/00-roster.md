---
name: TTRPG Team Roster
type: reference
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

| Agent | File | Focus |
|-------|------|-------|
| Aldric | [01-aldric-dnd.md](agents/01-aldric-dnd.md) | D&D 3.5e / 4e / 5e — bounded accuracy, class balance, spell economy |
| Morrigan | [02-morrigan-wfrp.md](agents/02-morrigan-wfrp.md) | WFRP 2e / 4e — gritty realism, career progression, consequence design |
| Sylvara | [03-sylvara-pf2e.md](agents/03-sylvara-pf2e.md) | Pathfinder 2e — 3-action economy, proficiency scaling, monster math |
| Vance | [04-vance-dc20.md](agents/04-vance-dc20.md) | DC20 — AP-adjacent systems, martial/caster parity, classless design |

## Min-Maxers (adversarial builders)

| Agent | File | Focus |
|-------|------|-------|
| Skar | [05-skar-offense.md](agents/05-skar-offense.md) | Maximum reliable damage output per AP spent — DPR optimization |
| Cipher | [06-cipher-loops.md](agents/06-cipher-loops.md) | Invulnerability, infinite loops, action denial, combo exploits |

## Balancers (design response team)

| Agent | File | Focus |
|-------|------|-------|
| Lyra | [07-lyra-patcher.md](agents/07-lyra-patcher.md) | Rule text fixes — closes specific exploits with precise language |
| Thane | [08-thane-adversarial.md](agents/08-thane-adversarial.md) | GM-side adversarial tools — what encounters already counter broken builds |
| Vesper | [09-vesper-economy.md](agents/09-vesper-economy.md) | AP cost auditor — correct pricing of every action in the system |
| Oryn | [10-oryn-magic.md](agents/10-oryn-magic.md) | Magic and expertise tree scaling — investment curves, tree parity |

## The Party (4 casuals — they play together)

| Agent | File | Archetype |
|-------|------|-----------|
| Bram | [11-bram-warrior.md](agents/11-bram-warrior.md) | Story-first warrior — thematic builder, reads rules once |
| Talia | [12-talia-newcomer.md](agents/12-talia-newcomer.md) | TTRPG newcomer — comes from video game RPGs, no tabletop history |
| Roz | [13-roz-convert.md](agents/13-roz-convert.md) | D&D 5e veteran — 8 years of muscle memory, adapting to the system |
| Dane | [14-dane-healer.md](agents/14-dane-healer.md) | Support/face player — healer, social skills, non-combat investment |

## Game Masters

| Agent | File | Style |
|-------|------|-------|
| Holt | [15-holt-casual-gm.md](agents/15-holt-casual-gm.md) | Story-first GM — tests accessibility, rule clarity, narrative flow |
| Vex | [16-vex-hardcore-gm.md](agents/16-vex-hardcore-gm.md) | Ultra-hardcore GM — encounter optimizer, TPK pressure, adversarial design |

## VTT Subject Matter Expert

| Agent | File | Focus |
|-------|------|-------|
| Petra | [17-petra-vtt.md](agents/17-petra-vtt.md) | Foundry / Roll20 / Fantasy Grounds power user — UX gap analysis |

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
5. **Petra** audits the VTT UX against Foundry/Roll20 feature parity.

No finding is suppressed. Every broken build gets a logged response. Every rule gap gets tracked.
