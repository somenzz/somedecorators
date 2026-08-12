import copy
import json
import os
from typing import Any, Dict, Optional
import yaml


class ConfigManager:
    """
    Singleton configuration manager for loading JSON or YAML config files.
    """
    _instance: Optional["ConfigManager"] = None
    _filepath: Optional[str] = None
    _config: Dict[str, Any] = {}

    def __new__(cls, filepath: Optional[str] = "./config.yml") -> "ConfigManager":
        if cls._instance is None or (filepath is not None and filepath != cls._filepath):
            instance = super(ConfigManager, cls).__new__(cls)
            if filepath:
                instance._config = cls._load_config(filepath)
                instance._filepath = filepath
            else:
                instance._config = {}
                instance._filepath = None
            cls._instance = instance
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Reset the singleton instance (useful for unit tests and reloading)."""
        cls._instance = None
        cls._filepath = None
        cls._config = {}

    @staticmethod
    def _load_config(filepath: str) -> Dict[str, Any]:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Configuration file '{filepath}' not found.")

        file_ext = os.path.splitext(filepath)[1].lower()
        with open(filepath, "r", encoding="utf-8") as file:
            if file_ext == ".json":
                data = json.load(file)
            elif file_ext in [".yml", ".yaml"]:
                data = yaml.safe_load(file)
            else:
                raise ValueError(f"Unsupported file format '{file_ext}'. Please use JSON or YAML.")

        return data if isinstance(data, dict) else {}

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key. Returns a deep copy of the value.
        """
        val = self._config.get(key, default)
        return copy.deepcopy(val)

    def get_all(self) -> Dict[str, Any]:
        """
        Get all configuration options. Returns a deep copy of the configuration dictionary.
        """
        return copy.deepcopy(self._config)
