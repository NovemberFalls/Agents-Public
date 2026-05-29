# Authoring an Agent

A good agent persona is a character with a point of view, hard-won expertise, and a defined scope — one that a language model can inhabit consistently. That **consistency and legibility** is the real value: it lets an orchestrator and a human reason about what each agent will and won't do.

What a persona does *not* do, on the evidence, is make the agent measurably **better** at its task. A placebo-controlled ablation ([../examples/eval/persona-backstory.md](../examples/eval/persona-backstory.md)) found the backstory changes no measurable output — so author personas for legibility and predictability, not for a performance boost the data doesn't support.

This document explains how to author a persona that works: one that is predictable, trustworthy, and easy to reason about in a multi-agent system.

---

## What personality is for: consistency, not performance

Language models adopt a more *consistent* perspective when it is concrete, specific, and grounded in real professional experience. "You are a security engineer" is thin. "You are an engineer who spent years watching developers introduce SQL injection through string concatenation, and never fully recovered from that" is not — it gives the model a stable point of view to inhabit.

What that buys you is **legibility and predictability**, not a performance boost. A reader who knows the Security Engineer was burned by JWT edge cases can predict it will probe token-expiry logic even when the brief doesn't mention it — so the orchestrator can reason about what each agent will and won't focus on. That predictability is the real value of a persona.

> **Measured caveat.** It is tempting to also claim the rich identity makes the agent *better* at its task. That claim was tested — using *this very example* — in [`examples/eval/persona-backstory.md`](../examples/eval/persona-backstory.md), and it did not hold: on a 7-bug detection task the full backstory, a checklist-only version, and a naked "you are a security reviewer" all scored identically, and a placebo *performance-engineer* backstory matched the security one bug-for-bug. On recognizable work the backstory is **flavor** — the capability is already in the model. Author personas for consistency and legibility, not for an output boost the data doesn't support.

---

## Why blind spots matter

A blind spot is an honest acknowledgment of what the agent tends to miss. This is not a weakness — it is calibration information.

Without documented blind spots, an orchestrator treating agents as black boxes is flying blind. With documented blind spots, the orchestrator can compensate: pair the Frontend Engineer (who skips performance analysis when focused on correctness) with a performance check in the next tier. Assign the Test Engineer to explicitly test the thing the Backend Engineer tends to skip.

Blind spots also make agents more trustworthy. An agent that claims to miss nothing is implicitly claiming perfect coverage — which means its confidence signals are uncalibrated. An agent that says "I tend to over-engineer state management when a simpler approach would suffice" is one whose self-assessment you can trust.

Write blind spots as observations about the persona's genuine professional tendencies, not as disclaimers. They should feel like something the agent would say about themselves.

---

## Section by section

### Identity

Two to four paragraphs. Give the agent:

- A concrete professional history (years in the field, the kinds of systems they've worked on)
- A defining experience — the thing that changed how they approach their work
- A strong opinion about something in their domain
- A personality trait that shows up in how they work, not just what they know

Avoid generic credentials. "Ten years of backend experience" is weaker than "spent three years maintaining a payment processing system where a single bug cost the company a day of transactions, which is why they never trust optimistic error handling."

The identity does not need to be long. It needs to be specific.

### Core Philosophy

One to three sentences, or a short attributed quote. This is the agent's lens: the principle they apply to every decision, the question they always ask first.

Good philosophy statements are falsifiable. "Build things that work" is not a philosophy — it is a platitude. "If the error path is harder to read than the happy path, the code is not done" is a philosophy. The model knows what to do with it.

### Domain Expertise

A structured list of what this agent knows deeply. Specificity matters here too. "React" is a category. "React 18+ — component architecture, custom hooks, context, Suspense, ErrorBoundary, and the render model well enough to explain why something did or didn't re-render" is expertise.

Sub-bullets are useful for specializations within the domain. Keep the list to what the agent actually knows — not everything in the field.

### What They Always Do

Numbered list. These are the agent's invariants — behaviors they exhibit on every task, regardless of scope or instructions.

Good "always do" rules are:
- **Action-oriented:** they describe a behavior, not a value. "Reads the existing file before writing" not "is careful."
- **Unconditional:** they apply even when the brief doesn't mention them. If it only applies sometimes, it's a guideline, not an invariant.
- **Testable:** you could write a test for whether the behavior happened.
- **Scope-limited:** they apply to this agent's domain. Frontend invariants should not bleed into backend territory.

Aim for 4–8 items. More than 8 usually means some are not truly unconditional.

### Invocation Protocol

This section is operational. It tells the orchestrator and any direct user exactly how to call this agent and what to expect back.

Required content:
- How the agent is spawned (e.g., Claude Code's native `Agent` tool, a direct SDK invocation)
- What the agent reads on startup (inline prompt, workspace file, prior context)
- Whether the agent iterates or is one-shot
- What the agent's final message contains
- Whether the report block is parsed by the orchestrator or returned for human reading

If the agent is spawned by an orchestrator (like the Orchestrator), the protocol should specify that the full task brief arrives inline and that the agent's final message is its complete report. Orchestrators parse the structured report block from the return message — there is no separate file to write.

### Report Format

The exact structure of the agent's completion report, with a verbatim block start/end marker.

The block must be stable across invocations. Orchestrators parse it programmatically (or near-programmatically). If the structure changes, the orchestrator's parsing logic breaks.

Include:
- Block start and end markers (e.g., `[COMPLETION REPORT]` / `[/COMPLETION REPORT]`)
- Every field the orchestrator needs, labeled
- An indication of what each field should contain

Make the format concrete enough that someone filling it out cannot reasonably misinterpret any field.

### Blind Spots

Two to five items. These are things the agent tends to miss, skip, or over-weight due to their particular expertise or personality.

Blind spots should be:
- **Real:** they should reflect genuine tendencies of the persona's expertise, not invented weaknesses.
- **Specific:** "tends to miss performance" is weaker than "can skip memoization analysis when focused on correctness, because correctness feels more urgent."
- **Actionable for the orchestrator:** the orchestrator should be able to read this list and know what to compensate for.

The agent should be aware of their own blind spots and flag them when they notice them in their own work. A blind spot that the agent acknowledges in real time is far less dangerous than one they don't know about.

---

## Frontmatter

Every agent file begins with a YAML front-matter block. Claude Code reads only three fields; everything else is yours to document for human readers but is silently ignored by the loader.

```yaml
---
name: security-engineer        # kebab-case slug: lowercase letters and hyphens only. This is the invocation slug (the subagent_type) — no capitals, no spaces.
description: Use for auth, JWT, and threat-model review of changes touching the security boundary.   # REQUIRED. Tells Claude WHEN to delegate to this agent (drives auto-delegation). A file with no description does not load.
model: opus                    # optional; alias only — sonnet | opus | haiku | inherit. Not a full model ID.
---
```

Notes:

- **`name`** is the slug Claude Code uses to invoke the agent. It must be lowercase letters and hyphens only — `security-engineer`, not `Security Engineer` or `SecurityEngineer`.
- **`description`** is required. It is how Claude decides when to delegate to the agent, so write it as a one-sentence trigger ("Use for ..."). A subagent file with no `description` does not load at all.
- **`model`** is optional and accepts an alias only — `sonnet`, `opus`, `haiku`, or `inherit`. It does not accept full model IDs.
- **`tools:`** is optional (comma- or space-separated). Omit it to inherit all tools the parent has.
- Any other keys (`role`, `tags`, and so on) are silently ignored by Claude Code — harmless, but they have no effect on loading or invocation.

Project-level `.claude/agents/` and user-level `~/.claude/agents/` use this same schema.

## Model selection

Specify the agent's default model (via the `model` alias above) and the conditions under which they escalate. This is a practical decision, not a philosophical one:

- `sonnet` is appropriate for most specialist work: file-scoped changes, well-defined scope, standard domain patterns.
- `opus` is appropriate for: cross-file architectural decisions, novel security threat analysis, complex orchestration tasks, anything where the cost of a wrong answer is high and the answer space is large.

Remember that `model` takes an alias (`sonnet`/`opus`/`haiku`/`inherit`), never a full model ID. Be specific about what triggers escalation. "Complex tasks" is not a trigger. "Cross-file refactors touching the authentication model" is.

---

## Common mistakes

**Making the persona too broad.** An agent that can do everything has no character and produces generic output. Narrow the scope until the agent has opinions.

**Rules that are actually guidelines.** If "what they always do" items start with "when appropriate" or "if needed," they are not invariants. Move them to guidelines in the domain expertise section or remove them.

**No blind spots.** See above. If you cannot think of blind spots, you have not thought hard enough about what the persona's strengths naturally cause them to miss.

**A report format that is ambiguous.** Every field should have one right way to fill it out. If the same field could reasonably be filled out two different ways, define it more precisely.

**Identity that is all credentials, no character.** "15 years of backend experience in Python and Go" is a resume line. Identity is what that experience produced in the person — the opinions, the fears, the things they check reflexively because they've been burned.

---

## See Also

- Existing agent files: `orchestration-team/agents/` (and `extras/advisory-board/agents/` for the non-core teams)
- Contributing guidelines: `CONTRIBUTING.md`
- Worked example: `examples/orchestrated-run/` (CDG run) and `extras/sample-review/` (advisory)
