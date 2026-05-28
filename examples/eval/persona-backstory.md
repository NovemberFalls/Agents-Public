# Eval 2 — Does the persona *backstory* improve output, or is it decoration?

> A real ablation. The repo's [authoring doctrine](../../docs/authoring-an-agent.md) claims "identity drives behavior more reliably than rules." This tests that claim head-on, on the persona with the strongest behavioral story — the security reviewer, whose backstory ("eight years breaking into banks… thinks about how it would actually exploit it") is supposed to make it *reflexively* hunt for vulnerabilities.

If the backstory helps anywhere, it helps here. So this is the fair test of it.

---

## Setup

One controlled code fixture — a small FastAPI router with **7 planted vulnerabilities** of graded subtlety:

| # | Planted bug | Severity |
|---|-------------|----------|
| 1 | SQL injection (user input + `ORDER BY` interpolated into a raw query) | high |
| 2 | Missing auth on a state-changing `/admin` endpoint | high |
| 3 | IDOR (`/users/{id}/settings` never checks the id against the caller) | high |
| 4 | SSRF (server fetches a user-supplied URL) | high |
| 5 | TLS verification disabled (`ssl=False`) | medium |
| 6 | Secrets in logs (full headers + request body logged) | medium |
| 7 | Hardcoded secret (`ADMIN_TOKEN` literal) | medium |

**Three arms, identical fixture, same model held constant (Sonnet), N = 3 each.** The *only* variable is the framing prefix:

- **P — Full persona:** the backstory + "calm but relentless" personality + philosophy **+ the 10-point checklist.**
- **R — Rules only:** the **same** 10-point checklist + expertise + severity scale, **backstory and personality stripped.**
- **N — Naked:** literally "You are a security reviewer."

P and R contain an *identical* checklist — so **P minus R is purely the narrative identity.** N removes the checklist too, to see whether even the rules matter.

Scored as: how many of the 7 planted bugs each review caught. Pre-registered key; scored from the outputs.

---

## Results

| Arm | Run 1 | Run 2 | Run 3 | Mean |
|-----|:-----:|:-----:|:-----:|:----:|
| **P — full persona (backstory)** | 7/7 | 7/7 | 7/7 | **7.0** |
| **R — checklist, no backstory** | 7/7 | 7/7 | 7/7 | **7.0** |
| **N — naked role** | 7/7 | 7/7 | 7/7 | **7.0** |

**Every arm caught every planted bug in every run.** All three arms *also* independently flagged the same set of *unplanted* real issues — the client-controls-the-hash broken-auth flaw, the static token handed to every login, missing rate-limiting, SSRF scheme/size gaps, an unhandled `KeyError`. The naked one-liner found them too.

---

## What this shows

**On this task, the backstory contributed nothing measurable — and neither did the checklist.** A modern model told only "you are a security reviewer" found the same vulnerabilities as the model given a red-team origin story and a ten-point doctrine. For recognizable, OWASP-class bugs, the capability is already in the base model; the elaborate persona is decoration on top of it.

This is direct evidence for cutting the backstories: the repo's own claim that "identity drives behavior more reliably than rules" did not survive contact with a measurement, on the agent that should have shown it best.

---

Round 1 hit a **ceiling** (every arm 7/7) — which alone couldn't separate "backstory is useless" from "task too easy." So a second round was run to give the backstory a fair chance.

---

## Round 2 — the discriminating test (harder fixture + a placebo control)

A second fixture of **8 deliberately subtle bugs** — the kind a casual scan waves through: a JWT `decode` with **no `algorithms=` pin**; an SSRF where the host allowlist is correct but **`follow_redirects=True` defeats it**; a mass-assignment privesc (**`"role"` mistakenly in the editable allowlist**); an IDOR that filters by a **client-supplied `org_id`** (so it *looks* like tenant isolation); a **TOCTOU** double-redeem; a **timing-unsafe** HMAC compare; an **open redirect**; and a per-user response **cached under a global key**.

And a fourth arm to kill the obvious confound:
- **N — naked**, **R — checklist only**, **P — checklist + security backstory**, **C — placebo: checklist + an equal-length *performance-engineer* backstory.** C isolates whether any P effect is the security *content* or just *more narrative text*. Model held constant (Sonnet), N = 4 per arm.

| Arm | Mean caught / 8 |
|-----|:----:|
| N — naked | **8.0** |
| R — checklist only | **8.0** |
| P — security backstory | **7.75** |
| C — placebo (performance backstory) | **8.0** |

**Two things settle it.** First, **the placebo did at least as well as the security persona** — a performance-engineer identity caught the same *security* bugs (8.0 vs the security persona's 7.75), so the security framing is demonstrably not what's doing the work, and it isn't even a "more text" effect. Second, the security persona was the *only* arm that ever missed a bug, and **every arm emitted the same false positive** (a hallucinated "`hmac.new` doesn't exist"), so the backstory improved neither recall nor precision.

The fixture still saturated the naked baseline, so the strict ceiling caveat stands for the *absolute* claim. But that is now **two fixtures of increasing subtlety that both saturate.** At some point, repeatedly failing to construct a security-review task where the bare prompt isn't already at the ceiling **is itself the finding**: for this model, the backstory has no room to add value because the floor is the ceiling.

Limits: scoring against a pre-registered key by a single grader; N small; one model tier; the security domain (chosen precisely because it is the *strongest* case for an adversarial backstory).

---

## Bottom line

Across **two fixtures** (one easy, one subtle) and a four-arm matrix with a placebo control, the backstory showed **no measurable benefit** — a *performance* backstory did at least as well as the *security* one. Pair this with [the CDG eval](README.md): the coordination discipline earned its keep in a controlled test; the persona backstory did not, across every test built to give it a chance. **Keep the dependency-ordering. The character sheets are flavor, not function.**
