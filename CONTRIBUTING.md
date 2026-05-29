# Contributing

Thank you for contributing to Agents-Public. This repository is a library of AI-agent persona files and orchestration patterns. Contributions fall into three categories: new agents, new teams, and improvements to existing personas or documentation.

The CI secret-scan gate (gitleaks) runs on every push and pull request. A PR cannot be merged if secrets or real PII are present anywhere in the diff. See [Secret hygiene](#secret-hygiene) below.

---

## Adding a new agent to an existing team

### Filename convention

Agent files use the pattern `NN-role.md` where `NN` is a zero-padded two-digit sequence number within the team folder. Agents are identified by role, not by personal name — there are NO personal names anywhere in this repository.

Examples:
- `03-backend-engineer.md`
- `07-gap-analyst.md`
- `11-infrastructure-engineer.md`

The sequence number determines display order in rosters. If you are inserting an agent between two existing numbers, renumber adjacent files and update the roster.

### Required YAML frontmatter

Every agent file must begin with a YAML front-matter block. Claude Code reads three fields:

```yaml
---
name: backend-engineer        # kebab-case slug: lowercase letters and hyphens only (no capitals, no spaces). This is the invocation slug / subagent_type.
description: Use for server-side logic, data models, and API design on changes touching the backend.   # REQUIRED. Tells Claude WHEN to delegate to this agent (drives auto-delegation). A file with no description DOES NOT LOAD.
model: sonnet                 # optional; alias only — sonnet | opus | haiku | inherit. NOT a full model ID.
---
```

- **`name`** must be a kebab-case slug (lowercase letters and hyphens only). It is the slug Claude Code uses to invoke the agent (the `subagent_type`).
- **`description`** is required. It is how Claude decides when to delegate, so phrase it as a one-sentence trigger. A subagent file with no `description` does not load.
- **`model`** is optional and accepts an alias only (`sonnet`, `opus`, `haiku`, `inherit`), never a full model ID. It reflects the agent's default model. If the agent escalates under specific conditions, document that in the **Model Selection** section of the persona body.
- **`tools:`** is optional (comma- or space-separated); omit it to inherit all tools.
- Any other keys (such as `role` or `tags`) are silently ignored by Claude Code, so they are harmless but have no effect. Advisory-board agents may add an optional `score_weight` for their scoring formula.

### Persona section structure

Each persona file must contain all of the following sections in order:

1. **Identity** — Who this agent is. Give them a concrete background: years of experience, a defining professional scar, the thing they care most about. Identity drives consistent behavior more reliably than a list of rules.

2. **Core Philosophy** — One to three sentences (or a short quote) capturing the agent's fundamental worldview about their domain. This is the lens through which they interpret every task.

3. **Domain Expertise** — A structured list of what this agent knows deeply. Be specific. "React 18+" is more useful than "frontend." Include sub-bullets for notable specializations.

4. **What They Always Do** — Numbered list of concrete, unconditional behaviors. These are invariants: things the agent does on every task regardless of scope. Keep each item action-oriented and testable. Aim for 4–8 items.

5. **Invocation Protocol** — How this agent is spawned and what it expects. Include: how the task brief arrives (inline prompt, workspace file, etc.); what the agent does on startup; what the agent's final message contains; whether the agent is one-shot or can iterate.

6. **Report Format** — The exact structure of the agent's completion report, including the verbatim block markers (e.g., `[COMPLETION REPORT]`). The orchestrator parses this block from the agent's return message — the structure must be stable.

7. **Blind Spots** — An honest list of what this agent tends to miss, over-weight, or skip. Blind spots make agents more useful: they help the orchestrator know which gaps to watch for and help other agents know what to double-check. An agent with no documented blind spots is less trustworthy than one with three honest ones.

### Persona quality bar

- The agent should feel like a real specialist with opinions, not a generic assistant.
- The "What They Always Do" rules should be concrete enough that you could write a test for each one.
- The report format block should be copy-pasteable into the agent's final message with no ambiguity about what goes where.
- Blind spots should be real — things the persona's strengths naturally cause them to miss.

---

## Proposing a new team

The repo root is kept focused on the validated `/orchestrate` core. A new team that applies the pattern to a **different domain** (not the coding loop) belongs under `extras/`, not the root. Such a PR includes:

1. A new folder: `extras/team-name/`
2. A `extras/team-name/README.md` describing: what the team does, when to use it, the full roster with roles and model assignments, and the team's primary workflow.
3. A `extras/team-name/agents/00-roster.md` with the complete roster table.
4. At least two agent files following the conventions above.
5. A one-line entry in `extras/README.md` (the root `README.md` stays scoped to the `/orchestrate` core).
6. An entry in `docs/architecture.md` only if the team introduces a genuinely new, validated orchestration pattern.

### Team design principles

- Teams should have a clear, bounded purpose that does not duplicate an existing team's scope.
- Agents within a team should have differentiated perspectives — if two agents would always agree, one of them is redundant.
- The team's report format should be defined at the team level (in the README or a `templates/` folder) so consumers know what to expect.
- Teams that produce scored output should define their scoring formula explicitly.

---

## Secret hygiene

This is a public repository. The secret-scan CI gate (`.github/workflows/secret-scan.yml`) runs gitleaks on every push and pull request. A failed scan blocks merging.

Do not include in any file:

- API keys, tokens, passwords, or secrets of any kind
- Personal names of any kind — agents are identified by role labels only (e.g., "the Backend Engineer"), never by a first name
- Real company names, domains, or trademarks (use `example.com` and fictional placeholders)
- Real infrastructure addresses, IP ranges, cloud account IDs, or resource names
- Any PII

If you are adapting a persona from a private configuration, strip all project-specific context before submitting. Agent personas should describe general expertise and behavior, not specifics about any real system.

---

## PR etiquette

- One logical change per PR. If you are adding a new agent and fixing a typo in an existing one, open two PRs.
- PR title format: `add: NN-role to team-name` / `fix: persona section in NN-role` / `docs: update architecture.md`
- The description should explain the agent's purpose and how they complement the existing roster — not just what files changed.
- If your PR changes the orchestration loop, scoring formula, or report format for an existing team, call that out explicitly in the PR description. Those are breaking changes for anyone consuming that team's output format.
- All new agent files must pass the gitleaks scan. The scan is not optional and cannot be bypassed.
