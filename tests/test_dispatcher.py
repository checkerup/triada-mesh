import json
import tempfile
import time
import unittest
from pathlib import Path

from triada.config import TriadaConfig
from triada.relay.dispatcher import RelayDispatcher


class TestDispatcher(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.tmp.name)
        self.config = TriadaConfig(
            root_dir=self.tmp_path,
            grace_min_sec=0,
            grace_max_sec=0,
        )
        self.config.ensure_directories()
        self.dispatcher = RelayDispatcher(self.config)

    def tearDown(self):
        self.tmp.cleanup()

    def test_cycle_order(self):
        self.assertEqual(self.dispatcher.next_agent_in_cycle("mark"), "kat")
        self.assertEqual(self.dispatcher.next_agent_in_cycle("kat"), "nika")
        self.assertEqual(self.dispatcher.next_agent_in_cycle("nika"), "mark")

    def test_handover_blocked_without_passing_tests(self):
        task_dir = self.config.tasks_dir / "task_untested"
        task_dir.mkdir(parents=True, exist_ok=True)
        status = {
            "agent": "mark",
            "task_id": "task_untested",
            "iteration": 1,
            "claims_done": True,
            "tests_run": False,
            "tests_passed": False,
        }
        (task_dir / "status.json").write_text(json.dumps(status), encoding="utf-8")

        res = self.dispatcher.process_task(task_dir, dry_run=True)
        self.assertEqual(res["status"], "blocked")
        self.assertTrue(any("tests_run" in r for r in res["reasons"]))

    def test_handover_success_when_green(self):
        task_dir = self.config.tasks_dir / "task_green"
        task_dir.mkdir(parents=True, exist_ok=True)
        status = {
            "agent": "mark",
            "task_id": "task_green",
            "iteration": 1,
            "claims_done": True,
            "tests_run": True,
            "tests_passed": True,
            "artifacts": [],
        }
        (task_dir / "status.json").write_text(json.dumps(status), encoding="utf-8")

        res = self.dispatcher.process_task(task_dir, dry_run=True)
        self.assertEqual(res["status"], "dispatched")
        self.assertEqual(res["from_agent"], "mark")
        self.assertEqual(res["to_agent"], "kat")
        self.assertTrue((task_dir / "handover.json").exists())


if __name__ == "__main__":
    unittest.main()
