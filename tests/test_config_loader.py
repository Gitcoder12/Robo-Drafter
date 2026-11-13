import tempfile
import unittest
from pathlib import Path

from robo_drafter.config_loader import get_param, load_policy_config, load_yaml, save_policy_config
from robo_drafter.types import PolicyConfig


class ConfigLoaderTests(unittest.TestCase):
    def test_load_default_policy(self):
        config = load_policy_config()
        self.assertEqual(config.name, "default_policy")
        self.assertEqual(config.params["speed"], 0.6)

    def test_load_yaml_rejects_non_mapping_root(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.yaml"
            path.write_text("- item\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_yaml(path)

    def test_get_param_returns_value_and_default(self):
        config = PolicyConfig(params={"speed": 0.8})
        self.assertEqual(get_param(config, "speed"), 0.8)
        self.assertEqual(get_param(config, "missing", 7), 7)

    def test_save_and_reload_policy_config(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "policy.yaml"
            expected = PolicyConfig(name="test", version="2", params={"speed": 0.9})
            save_policy_config(expected, path)
            actual = load_policy_config(path)
            self.assertEqual(actual.name, expected.name)
            self.assertEqual(actual.version, expected.version)
            self.assertEqual(actual.params, expected.params)


if __name__ == "__main__":
    unittest.main()
