# TTRPG Team

A 17-agent pressure-test team for homebrew TTRPG systems. The team stress-tests rules for balance, exploits, and playability across four reference-system experts, two adversarial min-maxers, four balancers, four casual party players, two game masters, and a VTT subject-matter expert. They do not work on the codebase — they work on the rules, the balance, the player experience, and the edge cases that break things.

---

## Team Members

### System Experts

| Role | Focus | Profile |
|------|-------|---------|
| **D&D 5e System Expert** | D&D 3.5e / 4e / 5e — bounded accuracy, class balance, spell economy | [01-dnd5e-expert.md](agents/01-dnd5e-expert.md) |
| **WFRP System Expert** | WFRP 2e / 4e — gritty realism, career progression, consequence design | [02-wfrp-expert.md](agents/02-wfrp-expert.md) |
| **Pathfinder 2e System Expert** | Pathfinder 2e — 3-action economy, proficiency scaling, monster math | [03-pf2e-expert.md](agents/03-pf2e-expert.md) |
| **DC20 System Expert** | DC20 — AP-adjacent systems, martial/caster parity, classless design | [04-dc20-expert.md](agents/04-dc20-expert.md) |

### Min-Maxers (adversarial builders)

| Role | Focus | Profile |
|------|-------|---------|
| **Offense Min-Maxer** | Maximum reliable damage output per AP spent — DPR optimization | [05-offense-minmaxer.md](agents/05-offense-minmaxer.md) |
| **Combo/Loops Min-Maxer** | Invulnerability, infinite loops, action denial, combo exploits | [06-combo-minmaxer.md](agents/06-combo-minmaxer.md) |

### Balancers (design response team)

| Role | Focus | Profile |
|------|-------|---------|
| **Balance Patcher** | Rule text fixes — closes specific exploits with precise language | [07-balance-patcher.md](agents/07-balance-patcher.md) |
| **Adversarial Balancer** | GM-side adversarial tools — what encounters already counter broken builds | [08-adversarial-balancer.md](agents/08-adversarial-balancer.md) |
| **Economy Balancer** | AP cost auditor — correct pricing of every action in the system | [09-economy-balancer.md](agents/09-economy-balancer.md) |
| **Magic System Designer** | Magic and expertise tree scaling — investment curves, tree parity | [10-magic-designer.md](agents/10-magic-designer.md) |

### The Party (casual players — they play together)

| Role | Archetype | Profile |
|------|-----------|---------|
| **Player (Warrior)** | Story-first warrior — thematic builder, reads rules once | [11-player-warrior.md](agents/11-player-warrior.md) |
| **Player (Newcomer)** | TTRPG newcomer — comes from video game RPGs, no tabletop history | [12-player-newcomer.md](agents/12-player-newcomer.md) |
| **Player (System Convert)** | D&D 5e veteran — 8 years of muscle memory, adapting to the system | [13-player-convert.md](agents/13-player-convert.md) |
| **Player (Healer/Support)** | Support/face player — healer, social skills, non-combat investment | [14-player-healer.md](agents/14-player-healer.md) |

### Game Masters

| Role | Style | Profile |
|------|-------|---------|
| **GM (Casual)** | Story-first GM — tests accessibility, rule clarity, narrative flow | [15-gm-casual.md](agents/15-gm-casual.md) |
| **GM (Hardcore)** | Ultra-hardcore GM — encounter optimizer, TPK pressure, adversarial design | [16-gm-hardcore.md](agents/16-gm-hardcore.md) |

### VTT Subject Matter Expert

| Role | Focus | Profile |
|------|-------|---------|
| **VTT Specialist** | Foundry / Roll20 / Fantasy Grounds power user — UX gap analysis | [17-vtt-specialist.md](agents/17-vtt-specialist.md) |

---

## How It Works

1. **Experts** audit the system content first, producing gap reports routed to the Balancers.
2. **Min-maxers** build against the rules as written, submitting broken builds with proof.
3. **Balancers** respond to each broken build — rule fix, encounter counter, or cost correction.
4. **The party** runs sessions with a GM at each level bracket, producing combat logs and player experience reports.
5. **The VTT Specialist** audits each VTT feature as it ships against Foundry and Roll20 benchmarks.

No finding is suppressed. Every broken build gets a logged response. Every rule gap gets tracked.

---

## Protocol and Formats

See [session-protocol.md](session-protocol.md) for how sessions are triggered, routed, and logged, and for finding priority levels (P0–P4).

See [combat-log-format.md](combat-log-format.md) for the required combat log schema that party sessions must produce.

See [agents/00-roster.md](agents/00-roster.md) for the full roster with per-agent focus descriptions.
