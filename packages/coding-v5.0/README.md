# coding-v5.0

The **v5.0 apply-tier coding skill**, packaged with the applier it depends on.

Install it, and `/orch-anth-5.0` works as measured. Copy the markdown alone and it
does not — the skill's central mechanism calls a tool that would not be there.

```bash
python install.py            # install
python install.py --check    # verify; exit 1 on drift
python install.py --uninstall
```

---

## Why this is a package and not two files

The skill and the applier are **one contract**. v5.0 emits SEARCH/REPLACE blocks in
exactly one format; the applier parses that format and applies a block **iff its SEARCH
matches exactly once**. Separate them and they drift — someone pairs the skill with a
hand-rolled applier that force-applies on a fuzzy match, the determinism is gone, and
the skill still advertises it.

That failure is measured, not hypothetical. From [FINDINGS.md](../../FINDINGS.md) §4.7:

| what was applied | score |
|---|---|
| verbatim SEARCH/REPLACE, deterministic apply | **532/532 blocks clean** |
| lossy old/new pairs, deterministic apply | 5/16 |
| lossy old/new pairs, *model* applying | 8/16 |
| same model, no patch, just the spec | 10/20 |

A model handed a flawed "exact" patch scored **below** the same model working from the
spec. **A bad diff is worse than no diff.** So the applier is not an optimization you can
substitute — an approximate one is worse than not installing it at all.

`install.py` checksums every file against `MANIFEST.json` before writing, and `--check`
tells you if an installed copy has drifted.

---

## What it installs

| file | destination | what it is |
|---|---|---|
| `commands/orch-anth-5.0.md` | `<claude>/commands/` | the skill → `/orch-anth-5.0` |
| `commands/fix.md` | `<claude>/commands/` | single-issue path → `/fix` |
| `tools/apply_blocks.py` | `<claude>/tools/orch-apply/` | the deterministic applier |

`<claude>` is `$CLAUDE_CONFIG_DIR`, else `~/.claude`.

**Nothing else is touched.** This package registers no hooks and does not edit
`settings.json`. If a destination file already exists with different content, it is
backed up alongside as `.bak` before being replaced.

Requires **Python 3.8+**, standard library only. No dependencies, no build step, no
network access.

---

## Using it

Invoke `/orch-anth-5.0 <task>` as normal. On DIFFABLE work the skill computes the change,
writes SEARCH/REPLACE blocks to a plan file, and lands them with:

```bash
python ~/.claude/tools/orch-apply/apply_blocks.py plan.blocks --root . --json apply.json
```

Windows/PowerShell: `python "$env:USERPROFILE\.claude\tools\orch-apply\apply_blocks.py" ...`

| exit | meaning |
|---|---|
| `0` | every block applied cleanly |
| `1` | residue (`nomatch` / `nonunique`) — escalate per skill §4.9 step 3 |
| `2` | malformed blocks — fix the emit, never force it |

Also: `--dry-run` (report, write nothing) · `--atomic` (all-or-nothing) · `--root` (repo
root the `FILE:` paths resolve against).

**The applier never force-applies.** A block whose SEARCH is missing or ambiguous is
reported, not guessed. That refusal is the guarantee — do not add a `--fuzzy` flag.

---

## Verify it

```bash
python -m pytest tests -q     # 27 tests, no install required
```

They pin the contract the skill depends on: exactly-once matching, residue never
force-applied, atomic abort, byte-exact indentation, CRLF/LF preservation, unicode
round-trip, and sequential blocks seeing prior edits.

---

## Naming

This installs as **`/orch-anth-5.0`**, matching this repo and
[boord-its.com/skills](https://boord-its.com/skills). If you prefer a different command
name, rename the file in `<claude>/commands/` — the skill body does not reference its own
name. (The author's local checkout calls it `/orch-code-anth`; same skill.)

---

## What is deliberately NOT here

- **`/orch-clean` and the §9 clean phase.** Built, but not yet through the arena. This
  repo's claim is *measured, not asserted*, so unmeasured work does not ship in the
  champion package. It will land in `coding-v5.1` once it has numbers.
- **Hooks.** `hooks/` in the repo root is opt-in and separate on purpose; this package
  will not edit your `settings.json`.

## Provenance

v5.0 graduated 2026-07-26 on the mechanism (k=25) and the whole skill (k=3):
~1.7× faster / ~2.6× cheaper on isolated mechanism, 1.9× / 2.0× end-to-end,
correctness-equal to v4.1, and a clean superset on generative work (3/3, 22/22).
Full evidence in [FINDINGS.md](../../FINDINGS.md) §4.7.

The packaged skill differs from the benchmarked text in exactly one way: §4.9 step 2
names the applier's installed path and exit codes. The benchmarked snapshot describes the
applier abstractly, which is precisely why an installing user could not run it.
