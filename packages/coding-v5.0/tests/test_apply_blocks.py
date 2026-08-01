"""apply_blocks tests: fidelity, residue discipline, and EOL drift.

The contract under test is the one the v5.0 apply-tier rests on: a block applies
iff its SEARCH matches EXACTLY ONCE, and residue is NEVER force-applied.

Run: python -m pytest tools/clean/tests -q
"""
import json
import os
import subprocess
import sys

import pytest

from conftest import HERE, write

import apply_blocks as ab

APPLIER = os.path.join(HERE, "..", "tools", "apply_blocks.py")


def block(path, search, replace):
    return (f"FILE: {path}\n<<<<<<< SEARCH\n{search}\n=======\n{replace}\n>>>>>>> REPLACE\n")


# --- parsing -------------------------------------------------------------

def test_parses_single_block():
    blocks = ab.parse_blocks(block("a.py", "old", "new"))
    assert len(blocks) == 1
    assert blocks[0].path == "a.py"
    assert blocks[0].search == "old"
    assert blocks[0].replace == "new"


def test_file_header_governs_until_next():
    text = (block("a.py", "one", "1")
            + "<<<<<<< SEARCH\ntwo\n=======\n2\n>>>>>>> REPLACE\n"
            + block("b.py", "three", "3"))
    blocks = ab.parse_blocks(text)
    assert [b.path for b in blocks] == ["a.py", "a.py", "b.py"]


def test_multiline_search_preserved_verbatim():
    blocks = ab.parse_blocks(block("a.py", "def f():\n    return 1", "def f():\n    return 2"))
    assert blocks[0].search == "def f():\n    return 1"


@pytest.mark.parametrize("bad,msg", [
    ("<<<<<<< SEARCH\nx\n=======\ny\n>>>>>>> REPLACE\n", "no preceding 'FILE:'"),
    ("FILE: a.py\n<<<<<<< SEARCH\nx\n", "unterminated SEARCH"),
    ("FILE: a.py\n<<<<<<< SEARCH\nx\n=======\ny\n", "unterminated block"),
    ("FILE: a.py\n<<<<<<< SEARCH\nx\n>>>>>>> REPLACE\n", "before '======='"),
    ("FILE: a.py\n", "no SEARCH block"),
])
def test_malformed_blocks_raise(bad, msg):
    with pytest.raises(ab.BlockParseError) as exc:
        ab.parse_blocks(bad)
    assert msg in str(exc.value)


# --- application ---------------------------------------------------------

def test_applies_unique_match(tmp_path):
    write(tmp_path, "a.py", "x = 1\ny = 2\n")
    rep = ab.apply_blocks(ab.parse_blocks(block("a.py", "x = 1", "x = 99")), root=str(tmp_path))
    assert rep["clean"] and rep["counts"]["applied"] == 1
    assert (tmp_path / "a.py").read_text() == "x = 99\ny = 2\n"


def test_nonunique_is_residue_and_file_untouched(tmp_path):
    write(tmp_path, "a.py", "dup\ndup\n")
    rep = ab.apply_blocks(ab.parse_blocks(block("a.py", "dup", "fixed")), root=str(tmp_path))
    assert rep["counts"]["nonunique"] == 1
    assert not rep["clean"]
    assert (tmp_path / "a.py").read_text() == "dup\ndup\n", "residue must never force-apply"


def test_nomatch_is_residue(tmp_path):
    write(tmp_path, "a.py", "actual\n")
    rep = ab.apply_blocks(ab.parse_blocks(block("a.py", "imagined", "new")), root=str(tmp_path))
    assert rep["counts"]["nomatch"] == 1
    assert (tmp_path / "a.py").read_text() == "actual\n"


def test_missing_file_is_error_not_crash(tmp_path):
    rep = ab.apply_blocks(ab.parse_blocks(block("ghost.py", "a", "b")), root=str(tmp_path))
    assert rep["counts"]["error"] == 1
    assert "not found" in rep["residue"][0]["detail"]


def test_sequential_blocks_see_prior_edits(tmp_path):
    write(tmp_path, "a.py", "a = 1\nb = 2\n")
    text = block("a.py", "a = 1", "a = 10") + block("a.py", "b = 2", "b = 20")
    rep = ab.apply_blocks(ab.parse_blocks(text), root=str(tmp_path))
    assert rep["counts"]["applied"] == 2
    assert (tmp_path / "a.py").read_text() == "a = 10\nb = 20\n"


def test_block_made_unique_by_a_prior_block(tmp_path):
    """A later block may become unique only after an earlier one rewrites its twin."""
    write(tmp_path, "a.py", "call()\ncall()\n")
    text = block("a.py", "call()\ncall()", "first()\ncall()") + block("a.py", "call()", "second()")
    rep = ab.apply_blocks(ab.parse_blocks(text), root=str(tmp_path))
    assert rep["clean"], rep["residue"]
    assert (tmp_path / "a.py").read_text() == "first()\nsecond()\n"


def test_partial_apply_writes_the_good_blocks(tmp_path):
    write(tmp_path, "a.py", "good\ndup\ndup\n")
    text = block("a.py", "good", "great") + block("a.py", "dup", "x")
    rep = ab.apply_blocks(ab.parse_blocks(text), root=str(tmp_path))
    assert rep["counts"] == {"applied": 1, "nomatch": 0, "nonunique": 1, "error": 0}
    assert (tmp_path / "a.py").read_text() == "great\ndup\ndup\n"


def test_atomic_aborts_the_whole_write(tmp_path):
    write(tmp_path, "a.py", "good\ndup\ndup\n")
    text = block("a.py", "good", "great") + block("a.py", "dup", "x")
    rep = ab.apply_blocks(ab.parse_blocks(text), root=str(tmp_path), atomic=True)
    assert rep["atomic_aborted"] and rep["wrote"] == []
    assert (tmp_path / "a.py").read_text() == "good\ndup\ndup\n"


def test_dry_run_writes_nothing(tmp_path):
    write(tmp_path, "a.py", "x = 1\n")
    rep = ab.apply_blocks(ab.parse_blocks(block("a.py", "x = 1", "x = 2")), root=str(tmp_path),
                          dry_run=True)
    assert rep["clean"] and rep["wrote"] == []
    assert (tmp_path / "a.py").read_text() == "x = 1\n"


def test_multi_file_report(tmp_path):
    write(tmp_path, "a.py", "a\n")
    write(tmp_path, "sub/b.py", "b\n")
    text = block("a.py", "a", "A") + block("sub/b.py", "b", "B")
    rep = ab.apply_blocks(ab.parse_blocks(text), root=str(tmp_path))
    assert rep["files"] == 2 and rep["clean"]
    assert (tmp_path / "sub" / "b.py").read_text() == "B\n"


# --- line endings (Windows-first) ----------------------------------------

def test_crlf_file_preserves_crlf(tmp_path):
    write(tmp_path, "a.py", "x = 1\ny = 2\n", newline="\r\n")
    rep = ab.apply_blocks(ab.parse_blocks(block("a.py", "x = 1", "x = 9")), root=str(tmp_path))
    assert rep["clean"]
    with open(tmp_path / "a.py", "r", encoding="utf-8", newline="") as fh:
        assert fh.read() == "x = 9\r\ny = 2\r\n"


def test_lf_search_against_crlf_file_counts_as_eol_kind(tmp_path):
    """Multi-line LF SEARCH vs a CRLF file: recovered, but counted as drift."""
    write(tmp_path, "a.py", "def f():\n    return 1\n", newline="\r\n")
    text = block("a.py", "def f():\n    return 1", "def f():\n    return 2")
    rep = ab.apply_blocks(ab.parse_blocks(text), root=str(tmp_path))
    assert rep["clean"]
    assert rep["applied_kinds"]["eol"] == 1, "EOL recovery must stay visible in the report"
    with open(tmp_path / "a.py", "r", encoding="utf-8", newline="") as fh:
        assert fh.read() == "def f():\r\n    return 2\r\n"


def test_indentation_is_byte_exact(tmp_path):
    write(tmp_path, "a.py", "if x:\n        deep = 1\n")
    rep = ab.apply_blocks(ab.parse_blocks(block("a.py", "    deep = 1", "    deep = 2")),
                          root=str(tmp_path))
    assert rep["counts"]["applied"] == 1
    assert (tmp_path / "a.py").read_text() == "if x:\n        deep = 2\n"


def test_unicode_roundtrip(tmp_path):
    write(tmp_path, "a.py", "s = 'caf\u00e9 \u2014 na\u00efve'\n")
    rep = ab.apply_blocks(
        ab.parse_blocks(block("a.py", "caf\u00e9 \u2014 na\u00efve", "caf\u00e9 \u2014 ok")),
        root=str(tmp_path))
    assert rep["clean"]
    assert "caf\u00e9 \u2014 ok" in (tmp_path / "a.py").read_text(encoding="utf-8")


def test_empty_replace_deletes_text(tmp_path):
    write(tmp_path, "a.py", "keep\nDROP\n")
    rep = ab.apply_blocks(ab.parse_blocks(block("a.py", "DROP\n", "")), root=str(tmp_path))
    assert rep["clean"]
    assert (tmp_path / "a.py").read_text() == "keep\n"


# --- CLI -----------------------------------------------------------------

def run_cli(tmp_path, blocks_text, *extra):
    bf = tmp_path / "plan.blocks"
    bf.write_text(blocks_text, encoding="utf-8")
    out = tmp_path / "report.json"
    proc = subprocess.run(
        [sys.executable, APPLIER, str(bf), "--root", str(tmp_path), "--json", str(out), *extra],
        capture_output=True, text=True)
    report = json.loads(out.read_text()) if out.exists() else None
    return proc, report


def test_cli_exit_zero_on_clean(tmp_path):
    write(tmp_path, "a.py", "x\n")
    proc, rep = run_cli(tmp_path, block("a.py", "x", "y"))
    assert proc.returncode == 0 and rep["clean"]


def test_cli_exit_one_on_residue(tmp_path):
    write(tmp_path, "a.py", "x\n")
    proc, rep = run_cli(tmp_path, block("a.py", "nope", "y"))
    assert proc.returncode == 1 and rep["counts"]["nomatch"] == 1
    assert "RESIDUE" in proc.stdout


def test_cli_exit_two_on_parse_error(tmp_path):
    proc, _ = run_cli(tmp_path, "FILE: a.py\n<<<<<<< SEARCH\nunterminated\n")
    assert proc.returncode == 2 and "PARSE ERROR" in proc.stderr


def test_cli_reads_stdin(tmp_path):
    write(tmp_path, "a.py", "x\n")
    proc = subprocess.run(
        [sys.executable, APPLIER, "-", "--root", str(tmp_path)],
        input=block("a.py", "x", "y"), capture_output=True, text=True)
    assert proc.returncode == 0
    assert (tmp_path / "a.py").read_text() == "y\n"
