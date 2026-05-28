---
template: task-file
project: "[project-id]"
priority: P0 | P1 | P2
type: feature | bugfix | refactor | security | devops | ui
assigned_to: "[specialist] or auto"
requires_audit: false
---

# Task: [Short Title]

## What Needs to Happen

[Plain English description of what you want. Be as specific or as vague as you like — the Orchestrator will ask for clarification if anything is ambiguous before writing code. You do not need to know which files are involved.]

## Why

[Context that helps the Orchestrator make better decisions — the "why" behind the task. What problem does this solve? What does success look like for you?]

## Acceptance Criteria

[Optional but useful. What does "done" look like to you? If you have specific behaviors you want verified, list them here.]

- [ ] [criterion]
- [ ] [criterion]

## Files Likely Involved

[Optional — if you know which files. Leave blank if you don't.]

- `[path]` — [why]

## Do NOT Touch

[Optional — anything the Orchestrator should explicitly leave alone.]

## Notes / Constraints

[Optional — anything that affects implementation choices. E.g., "keep it compatible with Windows Terminal", "don't add new dependencies", "this needs to ship before the relay feature".]

---
<!--
HOW TO USE:
1. Fill in the fields above (only the "What Needs to Happen" section is required)
2. Save the file anywhere in your project — e.g., tasks/my-task.md
3. Run: /orchestrate <project> task:<path-to-task-file>
   Or:  /fix <project> task:<path-to-task-file>

The Orchestrator will read this file, cross-reference with any existing audit findings,
build the dependency graph, and proceed.
-->
