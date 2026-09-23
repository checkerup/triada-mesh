import tempfile
import unittest
from pathlib import Path

from triada.relay.protocol import HandoverPackage


class TestHandover(unittest.TestCase):
    def test_serialization(self):
        pkg = HandoverPackage(
            handover_id="h1",
            task_id="t1",
            from_agent="mark",
            to_agent="kat",
            iteration=1,
            git_base_sha="abc1234",
            artifacts=["file1.py"],
            acceptance_criteria=["tests exit 0"],
        )
        d = pkg.to_dict()
        self.assertEqual(d["from_agent"], "mark")
        self.assertEqual(d["to_agent"], "kat")

        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "handover.json"
            pkg.save(p)
            loaded = HandoverPackage.load(p)
            self.assertEqual(loaded.handover_id, "h1")
            self.assertEqual(loaded.artifacts, ["file1.py"])


if __name__ == "__main__":
    unittest.main()
