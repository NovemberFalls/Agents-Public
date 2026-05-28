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

## The honest caveat (this is why the eval isn't finished)

All three arms hit **7/7 — a ceiling.** That means this test **cannot distinguish "the backstory is useless" from "the task was too easy to need any help."** When every arm maxes out, you learn that the floor (naked role) is already high — not that the persona could never add value on a harder problem.

The discriminating test — the one that would actually be fair to the backstory — uses bugs **subtle enough that the naked baseline misses some**, then checks whether the persona (or even just the checklist) *recovers* the missed ones. Candidates: a second-order injection through a stored value, an auth check that's present but order-dependent and bypassable, a TOCTOU race, a logic flaw in a multi-step flow. Until such a test shows the backstory recovering bugs the naked role misses, **the burden of proof sits with the backstory** — and this round gives it none.

Other limits: N = 3 (a pilot); one fixture; one persona (security — chosen precisely because it's the *strongest* case for backstory); model held at Sonnet (a different tier could move the floor, but the relative comparison is what matters).

---

## Bottom line

Pair this with [the CDG eval](README.md): the two together say the same thing from opposite directions. The **coordination discipline (the CDG) earned its keep in a controlled test; the persona backstory did not.** Keep the dependency-ordering. Treat the character sheets as flavor, not function — and if you want to defend them, the harder eval above is how you'd have to do it.
