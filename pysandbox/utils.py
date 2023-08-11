import os
import toml
from collections import ChainMap


class GameConfig:
    def __init__(self):
        self.config_file = "pysandbox/settings.toml"
        self._set_config()
    
    def _set_config(self):
        self.config = self._load_config(self.config_file)
        self.config_data = dict(ChainMap(*self.config.values()))

    @staticmethod
    def _load_config(config_file):
        with open(config_file, "r") as file:
            return toml.load(file)

    @staticmethod
    def _update_config(config_file, config_data):
        with open(config_file, "w") as file:
            toml.dump(config_data, file)

    def get(self, key):
        return self.config_data.get(key)

    def set(self, key, value):
        for k, v in self.config.items():
            if key in v.keys():
                self.config[k][key] = value
        self._update_config(self.config_file, self.config)
        self._set_config()


config = GameConfig()


def get_platform():
    if "ANDROID_ARGUMENT" in os.environ:
        return "mobile"
    elif os.environ.get("KIVY_BUILD", "") == "ios":
        return "mobile"
    else:
        return "desktop"
