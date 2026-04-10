import json
import yaml
import os


class ConfigManager:
    _instance = None

    def __new__(cls, filepath="./config.yml"):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._config = cls._load_config(filepath) if filepath else {}
        return cls._instance

    @staticmethod
    def _load_config(filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Configuration file '{filepath}' not found.")

        file_ext = os.path.splitext(filepath)[1]
        with open(filepath, "r", encoding="utf-8") as file:
            if file_ext == ".json":
                return json.load(file)
            elif file_ext in [".yml", ".yaml"]:
                return yaml.safe_load(file)
            else:
                raise ValueError("Unsupported file format. Please use JSON or YAML.")

    def get(self, key):
        return self._config.get(key)
        # return copy.deepcopy(self._config.get(key))

    def get_all(self):
        return self._config
        # return copy.deepcopy(self._config)


# Example usage
# config_manager = ConfigManager('path_to_config_file.json')
# value = config_manager.get('some_key')
# all_config = config_manager.get_all()


# Example usage:
if __name__ == "__main__":
    config_manager = ConfigManager("config.yml")
    # Access configuration values
    config_data = config_manager.get_all()
    print(config_data)
