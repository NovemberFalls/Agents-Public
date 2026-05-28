---
template: task-brief
version: 1
---

# Task Brief — [SPECIALIST] / Tier [N]
**Issued by:** Nadia
**Date:** [YYYY-MM-DD]
**Project:** [project]
**Run:** [scope/run identifier]

---

## Assignment

**Specialist:** [name]
**Model:** [Opus | Sonnet] — [reason for model choice]
**Tier:** [N] of [M] in this execution plan

---

## Task

[Precise, specific task description. Not vague goals — exact outcomes.]

**Done looks like:** [Specific verifiable definition of completion. E.g., "The WebSocket endpoint at `/ws/terminal/{id}` validates session cookies using the same auth middleware as `/api/me`, and returns 401 with `{"error": "unauthorized"}` for unauthenticated requests."]

---

## Audit Reference

**Finding source:** [agent name, review date, specific section]
**Finding (quoted):** "[exact text from audit report]"

This task directly addresses the above finding. Do not gold-plate beyond the scope of the finding without flagging it to Nadia.

---

## Files to Read

Read these files in full before touching anything:

| File | Reason |
|------|--------|
| [path] | [what you need to understand from it] |
| [path] | [what you need to understand from it] |

---

## Integration Context

**CRITICAL: Read this section before touching any file.**

The following changes were finalized in previous tiers. Your work must be compatible with them. The current state of affected files (as of this tier starting) is what you see in the codebase — do not assume anything about pre-Tier-[N-1] state.

| File | Change Made in Tier [N-1] | Impact on Your Task |
|------|--------------------------|--------------------|
| [file] | [what changed] | [how it affects your work] |

**Specific compatibility requirements:**
- [e.g., "auth.py now exports `require_auth` as an async dependency. Your server.py changes must use `Depends(require_auth)` not the old `request.session.get('user')` pattern."]
- [e.g., "create_terminal() in pty_manager.py now takes `model` as a keyword-only argument. All call sites in server.py must use `create_terminal(model=...)`."]

---

## Files to Write

You are authorized to modify these files only:

| File | Scope of Change |
|------|----------------|
| [path] | [what to change — specific, bounded] |

**Blast radius — DO NOT TOUCH:**
- [file or component]: [reason — e.g., "modified by Zara in Tier 1; touching this will create a merge conflict"]
- [file or component]: [reason — e.g., "out of scope for this run; defer to next sprint"]

---

## Quality Requirements

- [ ] Addresses the audit finding exactly as described — no more, no less without flagging
- [ ] Compatible with all integration context changes listed above
- [ ] Every function/method you add or modify has correct error handling
- [ ] No hardcoded values that should be config
- [ ] Follows existing code conventions (see CLAUDE.md for project conventions)
- [ ] [Domain-specific quality requirements, e.g., "ARIA labels on all interactive elements" for Finn; "all DB queries parameterized" for Sage]

---

## Return Format

When complete, return a Specialist Report (see template) to Nadia. Include:
1. Files modified with line ranges
2. Explicit integration context compliance statement
3. What Sam should test (specific test cases, not vague "test the feature")
4. Any open questions requiring Nadia's decision

**If blocked:** Return a BLOCKED Specialist Report immediately — do not spin in place. Describe exactly what is blocking you and what you need to proceed.

---

## Iteration Notes

If this is revision round [N] after previous feedback:

**Previous feedback from [Atlas | Nadia]:**
[specific notes from previous round]

**What changed since last attempt:**
[to be filled in by specialist]
