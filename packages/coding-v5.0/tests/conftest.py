"""Shared helpers for the coding-v5.0 package tests.

Self-contained on purpose: this package must be verifiable by someone who has
only cloned swarmsmith, with no other checkout and nothing installed.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.join(HERE, "..", "tools")
sys.path.insert(0, TOOLS)


def write(root, rel, content, newline="\n"):
    """Write a file with EXACT bytes -- newline translation off.

    Line endings are load-bearing here: the applier's fidelity guarantee is a
    byte-for-byte SEARCH match, so a test harness that silently rewrote \\n to
    \\r\\n would be testing something other than the contract.
    """
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as fh:
        fh.write(content.replace("\n", newline) if newline != "\n" else content)
    return p
