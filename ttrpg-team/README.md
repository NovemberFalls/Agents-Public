# TTRPG Team

An 18-agent pressure-test team for homebrew TTRPG systems. The team stress-tests rules for balance, exploits, and playability across four reference-system experts, two adversarial min-maxers, four balancers, four casual party players, two game masters, and a VTT subject-matter expert. They do not work on the codebase — they work on the rules, the balance, the player experience, and the edge cases that break things.

---

## Team Members

### System Experts

| Agent | Focus | Profile |
|-------|-------|---------|
| **Aldric** | D&D 3.5e / 4e / 5e — bounded accuracy, class balance, spell economy | [01-aldric-dnd.md](agents/01-aldric-dnd.md) |
| **Morrigan** | WFRP 2e / 4e — gritty realism, career progression, consequence design | [02-morrigan-wfrp.md](agents/02-morrigan-wfrp.md) |
| **Sylvara** | Pathfinder 2e — 3-action economy, proficiency scaling, monster math | [03-sylvara-pf2e.md](agents/03-sylvara-pf2e.md) |
| **Vance** | DC20 — AP-adjacent systems, martial/caster parity, classless design | [04-vance-dc20.md](agents/04-vance-dc20.md) |

### Min-Maxers (adversarial builders)

| Agent | Focus | Profile |
|-------|-------|---------|
| **Skar** | Maximum reliable damage output per AP spent — DPR optimization | [05-skar-offense.md](agents/05-skar-offense.md) |
| **Cipher** | Invulnerability, infinite loops, action denial, combo exploits | [06-cipher-loops.md](agents/06-cipher-loops.md) |

### Balancers (design response team)

| Agent | Focus | Profile |
|-------|-------|---------|
| **Lyra** | Rule text fixes — closes specific exploits with precise language | [07-lyra-patcher.md](agents/07-lyra-patcher.md) |
| **Thane** | GM-side adversarial tools — what encounters already counter broken builds | [08-thane-adversarial.md](agents/08-thane-adversarial.md) |
| **Vesper** | AP cost auditor — correct pricing of every action in the system | [09-vesper-economy.md](agents/09-vesper-economy.md) |
| **Oryn** | Magic and expertise tree scaling — investment curves, tree parity | [10-oryn-magic.md](agents/10-oryn-magic.md) |

### The Party (casual players — they play together)

| Agent | Archetype | Profile |
|-------|-----------|---------|
| **Bram** | Story-first warrior — thematic builder, reads rules once | [11-bram-warrior.md](agents/11-bram-warrior.md) |
| **Talia** | TTRPG newcomer — comes from video game RPGs, no tabletop history | [12-talia-newcomer.md](agents/12-talia-newcomer.md) |
| **Roz** | D&D 5e veteran — 8 years of muscle memory, adapting to the system | [13-roz-convert.md](agents/13-roz-convert.md) |
| **Dane** | Support/face player — healer, social skills, non-combat investment | [14-dane-healer.md](agents/14-dane-healer.md) |

### Game Masters

| Agent | Style | Profile |
|-------|-------|---------|
| **Holt** | Story-first GM — tests accessibility, rule clarity, narrative flow | [15-holt-casual-gm.md](agents/15-holt-casual-gm.md) |
| **Vex** | Ultra-hardcore GM — encounter optimizer, TPK pressure, adversarial design | [16-vex-hardcore-gm.md](agents/16-vex-hardcore-gm.md) |

### VTT Subject Matter Expert

| Agent | Focus | Profile |
|-------|-------|---------|
| **Petra** | Foundry / Roll20 / Fantasy Grounds power user — UX gap analysis | [17-petra-vtt.md](agents/17-petra-vtt.md) |

---

## How It Works

1. **Experts** audit the system content first, producing gap reports routed to the Balancers.
2. **Min-maxers** build against the rules as written, submitting broken builds with proof.
3. **Balancers** respond to each broken build — rule fix, encounter counter, or cost correction.
4. **The party** runs sessions with a GM at each level bracket, producing combat logs and player experience reports.
5. **Petra** audits each VTT feature as it ships against Foundry and Roll20 benchmarks.

No finding is suppressed. Every broken build gets a logged response. Every rule gap gets tracked.

---

## Protocol and Formats

See [session-protocol.md](session-protocol.md) for how sessions are triggered, routed, and logged, and for finding priority levels (P0–P4).

See [combat-log-format.md](combat-log-format.md) for the required combat log schema that party sessions must produce.

See [agents/00-roster.md](agents/00-roster.md) for the full roster with per-agent focus descriptions.
