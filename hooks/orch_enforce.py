"""v4 orchestration enforcement — PreToolUse hook (live-install layer, optional).

Turns the v4 mandate from prose into a denied tool call:
  1. While a swarm plan is ACTIVE for a repo, product-file Edit/Write by the
     ORCHESTRATOR session is denied (workers pass — by session identity when the
     harness distinguishes them, else by the batch-window protocol).
  2. Agent spawns must carry an explicit `model`, and a spawn whose description
     names a planned worker id may not run BELOW its planned lane (the floor).
  3. CEILING (2026-07-18): a worker's FIRST spawn may not run ABOVE its planned
     lane unless the plan names the promoting trap (workers[i].trap) — silent
     up-laning is where the haiku lane went in v4.0, and sonnet-drift on mundane
     clusters was the routed-mandate arm's measured leak. Attempt >= 2 up-lane is
     always allowed (that's the escalation ladder); attempts are counted in the
     marker's spawn_log, which `declare` resets and window toggles preserve.

Fail-open by design: no active marker -> allow; any internal error -> allow.
A hook must never brick a normal session; it only adds friction inside a declared
swarm. Deactivate any time: `python orch_declare.py --repo <path> clear`.

Marker files live in <TEMP>/orch-active/<sha1(repo)[:12]>.json (see orch_declare.py):
  {"repo": "C:/abs/repo", "mode": "swarm", "window": "closed"|"open"|"repair",
   "plan": "C:/abs/plan.json", "orchestrator_session": "<sid or empty>"}
"""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from pathlib import Path

LANE_RANK = {"haiku": 0, "sonnet": 1, "opus": 2, "fable": 3}
EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
SPAWN_TOOLS = {"Agent", "Task"}


def _allow() -> None:
    print(json.dumps({}))
    sys.exit(0)


def _deny(reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def _marker_dir() -> Path:
    return Path(tempfile.gettempdir()) / "orch-active"


def _load_markers() -> list[dict]:
    out = []
    d = _marker_dir()
    if not d.is_dir():
        return out
    for f in d.glob("*.json"):
        try:
            m = json.loads(f.read_text(encoding="utf-8"))
            m["_path"] = str(f)
            out.append(m)
        except (OSError, json.JSONDecodeError):
            continue
    return out


def _under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except (ValueError, OSError):
        return False


def _marker_for(path: Path, markers: list[dict]) -> dict | None:
    for m in markers:
        if m.get("mode") == "swarm" and m.get("repo") and _under(path, Path(m["repo"])):
            return m
    return None


def _record_spawn(marker: dict, wid: str, model: str) -> None:
    """Append to the marker's spawn log — the ceiling rule's attempt counter.
    Best-effort: a failed write only weakens the ceiling, never blocks a spawn."""
    try:
        p = Path(marker["_path"])
        m = json.loads(p.read_text(encoding="utf-8"))
        m.setdefault("spawn_log", {}).setdefault(wid, []).append(model)
        p.write_text(json.dumps(m), encoding="utf-8")
    except (OSError, json.JSONDecodeError, AttributeError, TypeError):
        pass


def _record_orchestrator(marker: dict, sid: str) -> None:
    """First session that writes the plan.json is the orchestrator; remember it."""
    if not sid or marker.get("orchestrator_session"):
        return
    try:
        p = Path(marker["_path"])
        m = json.loads(p.read_text(encoding="utf-8"))
        m["orchestrator_session"] = sid
        p.write_text(json.dumps(m), encoding="utf-8")
    except (OSError, json.JSONDecodeError):
        pass


def main() -> None:
    try:
        ev = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        _allow()
    tool = ev.get("tool_name") or ""
    tin = ev.get("tool_input") or {}
    sid = ev.get("session_id") or ""
    markers = _load_markers()
    if not markers:
        _allow()

    if tool in EDIT_TOOLS:
        fp = tin.get("file_path") or tin.get("notebook_path") or ""
        if not fp:
            _allow()
        path = Path(fp)
        # Writing the plan file itself identifies the orchestrator session.
        if path.name == "plan.json":
            for m in markers:
                if m.get("plan") and Path(m["plan"]).resolve() == path.resolve():
                    _record_orchestrator(m, sid)
            _allow()
        m = _marker_for(path, markers)
        if not m:
            _allow()
        osid = m.get("orchestrator_session") or ""
        if osid and sid and sid != osid:
            _allow()  # a worker (distinct session) — workers implement, that's the point
        window = m.get("window", "closed")
        if window in ("open", "repair"):
            _allow()  # batch in flight (workers share sid on this harness) or declared repair
        _deny(
            "v4 swarm plan is ACTIVE for this repo and the batch window is CLOSED: the "
            "orchestrator does not implement. Dispatch this change to a worker via the "
            "Agent tool (see plan.json), or — only for a LADDER_EXHAUSTED repair — run "
            "`python orch_declare.py --repo <repo> repair` and log it in reconciliation."
        )

    if tool in SPAWN_TOOLS:
        cwd = ev.get("cwd") or ""
        m = _marker_for(Path(cwd), markers) if cwd else None
        if not m:
            _allow()
        model = (tin.get("model") or "").lower()
        if not model:
            _deny("v4 mandate: pass `model` explicitly on every spawn (haiku|sonnet|opus) "
                  "per the plan's lane — never inherit.")
        desc = tin.get("description") or ""
        try:
            plan = json.loads(Path(m["plan"]).read_text(encoding="utf-8"))
            for w in plan.get("workers", []):
                wid = str(w.get("id", ""))
                lane = str(w.get("lane", "")).lower()
                if wid and lane in LANE_RANK and wid in desc:
                    mrank, lrank = LANE_RANK.get(model, 99), LANE_RANK[lane]
                    if mrank < lrank:
                        _deny(f"v4 lane violation: {wid} is planned {lane}; spawning it on "
                              f"{model} routes BELOW its lane. Escalating up is allowed; "
                              "down is not.")
                    if 99 > mrank > lrank:
                        prior = len((m.get("spawn_log") or {}).get(wid, []))
                        trap = str(w.get("trap") or "").strip()
                        if prior == 0 and not trap:
                            _deny(f"v4 ceiling: {wid} is planned {lane} and this is its FIRST "
                                  f"spawn — running it on {model} silently erases the cheap "
                                  "lane (the v4.0 defect). Spawn at the planned lane, or name "
                                  f"the promoting trap in plan.json (workers[{wid}].trap) and "
                                  "re-dispatch. Up-lane after a failed attempt (the ladder) is "
                                  "allowed automatically.")
                    _record_spawn(m, wid, model)
                    break
        except (OSError, json.JSONDecodeError, KeyError, AttributeError, TypeError):
            pass
        _allow()

    _allow()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:  # noqa: BLE001 — a hook must never brick the session
        _allow()
