import json
import tempfile
import unittest
from pathlib import Path

from triada.config import TriadaConfig
from triada.pacer.pacer import JevPacer
from triada.providers.env_provider import EnvKeyPoolProvider


class TestPacer(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.tmp.name)
        self.config = TriadaConfig(root_dir=self.tmp_path)
        self.config.ensure_directories()
        self.provider = EnvKeyPoolProvider()
        self.pacer = JevPacer(self.config, provider=self.provider)

    def tearDown(self):
        self.tmp.cleanup()

    def test_untested_claims_done_triggers_kick(self):
        task_dir = self.config.tasks_dir / "task_false_finish"
        task_dir.mkdir(parents=True, exist_ok=True)
        status = {
            "agent": "mark",
            "task_id": "task_false_finish",
            "iteration": 1,
            "claims_done": True,
            "tests_run": False,
            "tests_passed": False,
        }
        (task_dir / "status.json").write_text(json.dumps(status), encoding="utf-8")

        kick = self.pacer.evaluate_task(task_dir)
        self.assertIsNotNone(kick)
        self.assertEqual(kick.stalled_location, "untested_code")
        self.assertTrue((task_dir / "kicks" / "kick_001.json").exists())

    def test_green_claims_done_no_kick(self):
        task_dir = self.config.tasks_dir / "task_green"
        task_dir.mkdir(parents=True, exist_ok=True)
        status = {
            "agent": "mark",
            "task_id": "task_green",
            "iteration": 1,
            "claims_done": True,
            "tests_run": True,
            "tests_passed": True,
        }
        (task_dir / "status.json").write_text(json.dumps(status), encoding="utf-8")

        kick = self.pacer.evaluate_task(task_dir)
        self.assertIsNone(kick)


if __name__ == "__main__":
    unittest.main()
