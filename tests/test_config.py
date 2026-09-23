import os
import tempfile
import unittest
from pathlib import Path

from triada.config import TriadaConfig, get_default_triada_root


class TestConfig(unittest.TestCase):
    def test_default_paths(self):
        root = get_default_triada_root()
        self.assertIsNotNone(root)
        config = TriadaConfig(root_dir=root)
        self.assertEqual(config.vault_dir, root / "vault")
        self.assertEqual(config.tasks_dir, root / "tasks")
        self.assertEqual(config.logs_dir, root / "logs")

    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            config = TriadaConfig(
                root_dir=tmp_path,
                log_level="DEBUG",
                jev_provider="env",
            )
            cfg_file = tmp_path / "config.json"
            config.save(cfg_file)

            loaded = TriadaConfig.load(cfg_file)
            self.assertEqual(loaded.log_level, "DEBUG")
            self.assertEqual(loaded.root_dir, tmp_path)


if __name__ == "__main__":
    unittest.main()
