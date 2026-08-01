"""Package integrity: the manifest must survive git's line-ending rewrite.

This repo pins `* text=auto eol=lf`, so a file committed from Windows is CRLF on
the author's disk and LF in every fresh clone. A manifest built from raw bytes
therefore fails verification on every machine except the author's, and
`install.py` refuses to install -- the package would be dead on arrival for
everyone who cloned it.

Run: python -m pytest tests -q
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.join(HERE, "..")
sys.path.insert(0, PKG)

import install  # noqa: E402


def test_checksum_is_eol_independent(tmp_path):
    """The same content with CRLF and with LF must hash identically."""
    lf = tmp_path / "lf.py"
    crlf = tmp_path / "crlf.py"
    with open(lf, "wb") as fh:
        fh.write(b"def f():\n    return 1\n")
    with open(crlf, "wb") as fh:
        fh.write(b"def f():\r\n    return 1\r\n")
    assert install.sha256(str(lf)) == install.sha256(str(crlf))


def test_checksum_still_detects_real_changes(tmp_path):
    a = tmp_path / "a.py"
    b = tmp_path / "b.py"
    a.write_bytes(b"x = 1\n")
    b.write_bytes(b"x = 2\n")
    assert install.sha256(str(a)) != install.sha256(str(b))


def test_manifest_matches_the_shipped_files():
    """Regenerate with `python install.py --build-manifest` if this fails."""
    assert install.verify_source() == []


def test_manifest_covers_every_shipped_file():
    manifest = install.load_manifest()
    assert manifest is not None
    expected = {f"commands/{n}" for n in install.COMMANDS} | \
               {f"tools/{n}" for n in install.TOOLS}
    assert set(manifest["files"]) == expected


def test_manifest_version_matches_installer():
    assert install.load_manifest()["version"] == install.VERSION


def test_manifest_hashes_match_lf_normalized_content():
    """What a fresh clone will compute -- pinned explicitly, not via sha256()."""
    manifest = install.load_manifest()
    for rel, want in manifest["files"].items():
        path = os.path.join(PKG, rel.replace("/", os.sep))
        with open(path, "rb") as fh:
            data = fh.read()
        got = hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()
        assert got == want, f"{rel}: manifest is not the LF-normalized hash"


def test_manifest_is_valid_json_and_sorted():
    with open(os.path.join(PKG, "MANIFEST.json"), encoding="utf-8") as fh:
        raw = fh.read()
    data = json.loads(raw)
    assert list(data["files"]) == sorted(data["files"])
