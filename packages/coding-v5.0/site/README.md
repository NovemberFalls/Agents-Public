# site/ — the two files boord-its.com/skills serves

These are the **download targets** for the site's v5.0 card. They are not the same
artifacts as `../commands/` and `../tools/`, and the difference is deliberate.

| | `packages/coding-v5.0/` | `site/` |
|---|---|---|
| audience | someone who cloned swarmsmith | someone who clicked Download |
| install | `install.py`, checksummed | save two files by hand |
| command name | `/orch-anth-5.0` | `/orchestrate` |
| frontmatter | none | `name:` + `description:` |
| evidence sections | full | trimmed |

## Why the site file is not just a copy of `../commands/orch-anth-5.0.md`

Serving the package file directly would have broken two promises the site already makes:

1. **Frontmatter.** The site says the file *"ships with the frontmatter for both"* — so it
   works as `~/.claude/commands/orchestrate.md` **or** `~/.claude/skills/orchestrate/SKILL.md`.
   The package file has no frontmatter; serving it would silently break skill-style
   discovery and make a second site claim false while we were fixing the first.
2. **Weight.** The public file was deliberately trimmed. The package file carries the full
   evidence sections, which belong in a repo, not in a context window on every run.

So the site file is the **published public text plus the applier wiring**, nothing else:
+18 lines into §4.9 step 2 giving the path, the exit codes, the do-not-substitute rule with
its 8/16-vs-10/20 evidence, and the stop-if-missing instruction.

## Published checksums (LF-normalized, as served)

```
orchestrate-anthropic-v5.0-public.md  ae6e82828e202009ad3f1ec895f4045d67424b4b69a41ad816ce4c32b6f3d1e8
apply_blocks.py                       83ebeebc1618a9fdadd4503e51e84f61084b497677a547d81fbcab30b4dd837a
```

Hashes are LF-normalized on purpose: git serves LF, Windows checkouts hold CRLF, and a raw
byte hash would fail verification for most of the people checking it. Same trap that made
this package's own manifest unusable on every fresh clone earlier the same day.

## Keeping them in step

`apply_blocks.py` here is a byte copy of `../tools/apply_blocks.py`. If that file changes,
copy it again and republish both hashes — a served applier that has drifted from the
tested one is exactly the substitution this whole design exists to prevent.

Verify before publishing:

```bash
python -m pytest ../tests -q      # 34 tests, covers the served applier
```
