# Dr. Reyes — CTO Review: Lumina

> Fictional example for illustration — not a real project, company, or person.

---

```
[AGENT REVIEW]
Agent: Dr. Reyes
Role: CTO — Technical Architecture
Project: Lumina (fictional open-source Markdown note-taking app)
Review cycle: Initial
Score: 6 / 10
Confidence: Medium-high (reviewed architecture docs, plugin API spec, and source samples)
```

---

## Summary

Lumina has a solid architectural foundation. The local-first storage model is a sensible default for a desktop note-taking tool, and the decision to build sync as an optional layer rather than a core assumption shows good design judgment. The plugin renderer system is the right call for extensibility.

The gaps are in three areas: the sync protocol is under-specified in ways that will create edge cases at scale; the plugin API exposes too much internal state with no stability guarantees; and the test architecture is weak for a project that encrypts user data.

This is a project I would ship to public beta with targeted remediation. It is not ready for a 1.0 release today.

---

## Strengths

**Local-first architecture.** The decision to make the local store the source of truth, with sync as a one-way push to an optional remote, is architecturally sound. It means offline behavior is a first-class citizen, not an afterthought. The conflict resolution strategy (last-write-wins with an explicit merge prompt for detected conflicts) is simple and honest about its limitations.

**Plugin renderer isolation.** Plugins run in a sandboxed renderer process, not in the main application process. This is the right call. A plugin that crashes takes down its renderer, not the application. The IPC boundary between core and plugins is explicit and narrow.

**Structured note format.** The internal note format is a versioned superset of CommonMark. Notes carry a schema version field. This gives the team a migration path when the format evolves — something many note-taking apps do not think about until they need it.

---

## Gaps

### Gap 1 — Sync protocol edge cases (severity: HIGH)

The sync protocol specification covers the happy path (push local changes, pull remote changes, merge by timestamp) but does not specify behavior for:

- Clock skew between devices (timestamps are device-generated with no NTP enforcement)
- Sync interrupted mid-batch (partial uploads — which notes are considered synced?)
- Remote deletion of a note that has been modified locally since last sync

These are not theoretical edge cases. They are the cases that will produce data loss for real users. The sync protocol needs explicit conflict resolution rules for each of these before the sync feature goes to production.

**Recommendation:** Write a sync protocol specification that covers these three failure modes explicitly, with decision rules (not "TBD"). Then write integration tests that deliberately induce each failure mode.

### Gap 2 — Plugin API stability (severity: MEDIUM)

The plugin API currently exposes the internal `NoteStore` object directly. Plugins can read the full note graph, including metadata and attachments, not just the note content they are rendering. This is a security concern (any plugin can read all notes) and an API stability concern (the internal `NoteStore` shape is not declared stable, so any internal refactor breaks plugins).

**Recommendation:** Define a minimal, stable plugin API surface. Plugins should receive only the note content and declared metadata they need for rendering. The core should not expose internal objects. Define a plugin API version, and commit to a deprecation policy before the plugin system goes public.

### Gap 3 — Test architecture for encrypted data (severity: HIGH)

The end-to-end encryption sync layer has unit tests for the encryption and decryption functions individually, but no integration tests that verify the round-trip: encrypt on device A, sync to remote, decrypt on device B. This is the failure mode that matters, and it is untested.

The test suite also has no tests for the key derivation path on initial setup or on device re-authorization. Key derivation bugs produce silent data loss.

**Recommendation:** Before releasing the sync feature, write integration tests for the full E2E encrypt/sync/decrypt round-trip. Include at least one test for re-authorization (new device, existing account). These tests are non-negotiable for a product that makes an encryption promise to users.

### Gap 4 — Observability for desktop distribution (severity: LOW)

The application ships with no crash reporting or telemetry (which is a reasonable default for a privacy-oriented tool). But there is also no mechanism for users to opt into diagnostics, and no error logging that persists across crashes. When things go wrong in production, the team will have no signal.

**Recommendation:** Add opt-in crash reporting with a clear privacy disclosure. Log errors to a local file by default so users can share diagnostics when filing issues.

---

## Technical Architecture Score

| Dimension | Assessment | Weight |
|-----------|-----------|--------|
| Architecture soundness | Strong local-first model, good plugin isolation | |
| Scalability | Sync protocol gaps create ceiling before scale matters | |
| Technical debt | Light — young codebase, not much accumulated debt | |
| Engineering practices | Testing gap for the most critical path (E2E encryption) | |
| Build vs. buy | Appropriate — using established Markdown parsers, custom only where needed | |

**Score: 6 / 10**

The foundation is good. The sync protocol gaps and the E2E encryption test gap are the blockers to a higher score. Both are addressable before a 1.0 release — they require engineering time, not architectural rethinking.

---

## Top Recommendations

1. (HIGH) Write and test the sync protocol conflict resolution rules before the sync feature ships.
2. (HIGH) Add E2E encrypt/sync/decrypt integration tests. Key derivation must be tested.
3. (MEDIUM) Define a stable, minimal plugin API surface and commit to a deprecation policy.
4. (LOW) Add opt-in crash reporting with local error logging.

```
[/AGENT REVIEW]
```
