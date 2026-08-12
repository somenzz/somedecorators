import json
import os
import tempfile
import unittest
import yaml
from somedecorators.config import ConfigManager


class TestConfigManager(unittest.TestCase):
    def setUp(self):
        ConfigManager.reset()

    def tearDown(self):
        ConfigManager.reset()

    def test_json_config_loading(self):
        config_data = {"app_name": "TestApp", "port": 8080, "debug": True}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tf:
            json.dump(config_data, tf)
            temp_path = tf.name

        try:
            cm = ConfigManager(temp_path)
            self.assertEqual(cm.get("app_name"), "TestApp")
            self.assertEqual(cm.get("port"), 8080)
            self.assertTrue(cm.get("debug"))
            self.assertEqual(cm.get("non_existent", "default"), "default")
            self.assertEqual(cm.get_all(), config_data)
        finally:
            os.remove(temp_path)

    def test_yaml_config_loading(self):
        config_data = {"database": {"host": "localhost", "port": 5432}}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as tf:
            yaml.dump(config_data, tf)
            temp_path = tf.name

        try:
            cm = ConfigManager(temp_path)
            self.assertEqual(cm.get("database"), {"host": "localhost", "port": 5432})
            self.assertEqual(cm.get_all(), config_data)
        finally:
            os.remove(temp_path)

    def test_defensive_copy(self):
        config_data = {"items": [1, 2, 3]}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tf:
            json.dump(config_data, tf)
            temp_path = tf.name

        try:
            cm = ConfigManager(temp_path)
            items = cm.get("items")
            items.append(4)
            self.assertEqual(cm.get("items"), [1, 2, 3])  # Internal config unchanged
        finally:
            os.remove(temp_path)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            ConfigManager("non_existent_file_path.json")

    def test_unsupported_format(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tf:
            tf.write("hello=world")
            temp_path = tf.name

        try:
            with self.assertRaises(ValueError):
                ConfigManager(temp_path)
        finally:
            os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()
