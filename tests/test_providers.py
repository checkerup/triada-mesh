import os
import unittest

from triada.pacer.pacer import load_provider
from triada.providers.env_provider import EnvKeyPoolProvider


class TestProviders(unittest.TestCase):
    def test_env_provider(self):
        os.environ["TEST_JEV_KEYS"] = "key_a,key_b"
        provider = EnvKeyPoolProvider(env_var="TEST_JEV_KEYS")
        self.assertEqual(provider.available_keys_count(), 2)

        k1 = provider.get_key()
        k2 = provider.get_key()
        self.assertEqual(k1, "key_a")
        self.assertEqual(k2, "key_b")

        provider.report_exhausted("key_a")
        self.assertEqual(provider.available_keys_count(), 1)
        self.assertEqual(provider.get_key(), "key_b")

    def test_load_provider_builtin(self):
        p = load_provider("env")
        self.assertIsInstance(p, EnvKeyPoolProvider)


if __name__ == "__main__":
    unittest.main()
