"""v4 orchestration marker helper — declare/toggle/clear the swarm enforcement state.

The orchestrator runs this via Bash at the §4.1/§4.3 checkpoints:

  python orch_declare.py --repo <abs repo> declare --plan <abs plan.json>
  python orch_declare.py --repo <abs repo> open      # dispatching a batch
  python orch_declare.py --repo <abs repo> close     # batch landed
  python orch_declare.py --repo <abs repo> repair    # LADDER_EXHAUSTED repair window
  python orch_declare.py --repo <abs repo> clear     # run over -> enforcement off

State lives OUTSIDE the repo in <TEMP>/orch-active/<sha1(repo)[:12]>.json, read by
orch_enforce.py (the PreToolUse hook). No marker -> the hook allows everything.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path


def marker_path(repo: str) -> Path:
    key = hashlib.sha1(str(Path(repo).resolve()).lower().encode()).hexdigest()[:12]
    d = Path(tempfile.gettempdir()) / "orch-active"
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{key}.json"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", required=True)
    ap.add_argument("action", choices=["declare", "open", "close", "repair", "clear"])
    ap.add_argument("--plan", default="")
    a = ap.parse_args()
    mp = marker_path(a.repo)

    if a.action == "clear":
        mp.unlink(missing_ok=True)
        print(f"cleared {mp}")
        return 0

    if a.action == "declare":
        if not a.plan:
            print("declare requires --plan <abs plan.json>", file=sys.stderr)
            return 2
        state = {"repo": str(Path(a.repo).resolve()), "mode": "swarm",
                 "window": "closed", "plan": str(Path(a.plan).resolve()),
                 "orchestrator_session": ""}
    else:
        if not mp.exists():
            print("no active marker — run `declare` first", file=sys.stderr)
            return 2
        state = json.loads(mp.read_text(encoding="utf-8"))
        state["window"] = {"open": "open", "close": "closed", "repair": "repair"}[a.action]

    mp.write_text(json.dumps(state), encoding="utf-8")
    print(f"{a.action}: {mp} -> {state['window'] if 'window' in state else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
