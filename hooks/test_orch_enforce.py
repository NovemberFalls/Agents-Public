"""Unit tests for orch_enforce.py — run the hook as the harness does: a real
subprocess with the event on stdin, marker state in an ISOLATED fake %TEMP%.

    python test_orch_enforce.py           # or: python -m unittest test_orch_enforce -v

Covers the floor (spawn below lane), the 2026-07-18 ceiling (first-attempt spawn
above lane without a named trap), the ladder exemption (attempt >= 2), the
orchestrator/worker edit split, window states, and fail-open behavior.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parent / "orch_enforce.py"


class HookCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="orchtest_"))
        self.repo = self.tmp / "repo"
        self.repo.mkdir()
        (self.repo / "lib").mkdir()
        self.scratch = self.tmp / "scratch"
        self.scratch.mkdir()
        self.plan = self.scratch / "plan.json"
        self.plan.write_text(json.dumps({"workers": [
            {"id": "W1", "lane": "opus", "files": ["lib/log.js"]},
            {"id": "W4", "lane": "haiku", "files": ["src/a.js"]},
            {"id": "W7", "lane": "sonnet", "files": ["src/b.js"]},
            {"id": "W9", "lane": "haiku", "files": ["src/c.js"],
             "trap": "instance-method logEvent must not change"},
        ]}), encoding="utf-8")
        self.marker_dir = self.tmp / "faketemp" / "orch-active"
        self.marker_dir.mkdir(parents=True)
        self.marker = self.marker_dir / "m.json"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def set_marker(self, **over):
        state = {"repo": str(self.repo), "mode": "swarm", "window": "closed",
                 "plan": str(self.plan), "orchestrator_session": "orch-sid"}
        state.update(over)
        self.marker.write_text(json.dumps(state), encoding="utf-8")

    def run_hook(self, event: dict) -> dict:
        env = dict(os.environ)
        env["TEMP"] = env["TMP"] = str(self.tmp / "faketemp")
        p = subprocess.run([sys.executable, str(HOOK)], input=json.dumps(event),
                           capture_output=True, text=True, env=env, timeout=30)
        self.assertEqual(p.returncode, 0, p.stderr)
        return json.loads(p.stdout)

    def decision(self, out: dict) -> str:
        return (out.get("hookSpecificOutput") or {}).get("permissionDecision", "allow")

    def edit_ev(self, path: Path, sid="orch-sid"):
        return {"tool_name": "Edit", "session_id": sid,
                "tool_input": {"file_path": str(path)}}

    def spawn_ev(self, model, desc, cwd=None):
        return {"tool_name": "Agent", "session_id": "orch-sid",
                "cwd": str(cwd or self.repo),
                "tool_input": {"model": model, "description": desc, "prompt": "x"}}

    # ── edits ────────────────────────────────────────────────────────────────
    def test_01_no_marker_allows_edit(self):
        self.assertEqual(self.decision(self.run_hook(self.edit_ev(self.repo / "lib/log.js"))), "allow")

    def test_02_orchestrator_edit_denied_when_closed(self):
        self.set_marker()
        self.assertEqual(self.decision(self.run_hook(self.edit_ev(self.repo / "lib/log.js"))), "deny")

    def test_03_open_window_allows_edit(self):
        self.set_marker(window="open")
        self.assertEqual(self.decision(self.run_hook(self.edit_ev(self.repo / "lib/log.js"))), "allow")

    def test_04_repair_window_allows_edit(self):
        self.set_marker(window="repair")
        self.assertEqual(self.decision(self.run_hook(self.edit_ev(self.repo / "lib/log.js"))), "allow")

    def test_05_worker_session_edit_allowed(self):
        self.set_marker()
        ev = self.edit_ev(self.repo / "lib/log.js", sid="worker-sid")
        self.assertEqual(self.decision(self.run_hook(ev)), "allow")

    def test_06_edit_outside_repo_allowed(self):
        self.set_marker()
        self.assertEqual(self.decision(self.run_hook(self.edit_ev(self.scratch / "notes.md"))), "allow")

    def test_07_plan_write_records_orchestrator(self):
        self.set_marker(orchestrator_session="")
        ev = self.edit_ev(self.plan, sid="first-writer")
        ev["tool_name"] = "Write"
        self.assertEqual(self.decision(self.run_hook(ev)), "allow")
        m = json.loads(self.marker.read_text(encoding="utf-8"))
        self.assertEqual(m["orchestrator_session"], "first-writer")

    # ── spawns: explicit model + floor ───────────────────────────────────────
    def test_08_spawn_without_model_denied(self):
        self.set_marker()
        ev = self.spawn_ev("", "W4 mundane sweep")
        self.assertEqual(self.decision(self.run_hook(ev)), "deny")

    def test_09_floor_violation_denied(self):
        self.set_marker()
        self.assertEqual(self.decision(self.run_hook(self.spawn_ev("sonnet", "W1 log core"))), "deny")

    def test_10_spawn_at_lane_allowed_and_logged(self):
        self.set_marker()
        self.assertEqual(self.decision(self.run_hook(self.spawn_ev("haiku", "W4 mundane sweep"))), "allow")
        m = json.loads(self.marker.read_text(encoding="utf-8"))
        self.assertEqual(m.get("spawn_log", {}).get("W4"), ["haiku"])

    def test_11_spawn_unmarked_cwd_allowed(self):
        self.set_marker()
        ev = self.spawn_ev("haiku", "W4 mundane sweep", cwd=self.scratch)
        self.assertEqual(self.decision(self.run_hook(ev)), "allow")

    # ── the ceiling (2026-07-18) ─────────────────────────────────────────────
    def test_12_first_attempt_uplane_without_trap_denied(self):
        self.set_marker()
        out = self.run_hook(self.spawn_ev("sonnet", "W4 mundane sweep"))
        self.assertEqual(self.decision(out), "deny")
        self.assertIn("ceiling", out["hookSpecificOutput"]["permissionDecisionReason"])

    def test_13_first_attempt_uplane_with_named_trap_allowed(self):
        self.set_marker()
        self.assertEqual(self.decision(self.run_hook(self.spawn_ev("sonnet", "W9 trapdense"))), "allow")

    def test_14_ladder_second_attempt_uplane_allowed(self):
        self.set_marker(spawn_log={"W4": ["haiku"]})
        self.assertEqual(self.decision(self.run_hook(self.spawn_ev("sonnet", "W4 mundane sweep"))), "allow")

    def test_15_fable_counts_as_uplane_for_ceiling(self):
        self.set_marker()
        self.assertEqual(self.decision(self.run_hook(self.spawn_ev("fable", "W4 mundane sweep"))), "deny")

    def test_16_unknown_model_string_fails_open(self):
        self.set_marker()
        self.assertEqual(self.decision(self.run_hook(self.spawn_ev("gpt-9", "W4 mundane sweep"))), "allow")

    # ── fail-open ────────────────────────────────────────────────────────────
    def test_17_malformed_stdin_allows(self):
        env = dict(os.environ)
        env["TEMP"] = env["TMP"] = str(self.tmp / "faketemp")
        p = subprocess.run([sys.executable, str(HOOK)], input="not json {",
                           capture_output=True, text=True, env=env, timeout=30)
        self.assertEqual(p.returncode, 0)
        self.assertEqual(self.decision(json.loads(p.stdout)), "allow")

    def test_18_missing_plan_file_fails_open_on_spawn(self):
        self.set_marker(plan=str(self.scratch / "gone.json"))
        self.assertEqual(self.decision(self.run_hook(self.spawn_ev("sonnet", "W4 mundane sweep"))), "allow")


if __name__ == "__main__":
    unittest.main(verbosity=2)
