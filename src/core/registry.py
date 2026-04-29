import json
from src.utils.config import REG_FILE


class VariableRegistry:
    def __init__(self):
        self.path = REG_FILE
        self.data = self._load()

    def _load(self):
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except:
            return {}

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    def set_key(self, key, val):
        self.data[key] = val
        self._save()

    def get_key(self, key):
        return self.data.get(key)

    def all_keys(self):
        return self.data