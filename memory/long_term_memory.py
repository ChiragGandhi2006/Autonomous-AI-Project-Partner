# memory/long_term_memory.py

import json
import os


class LongTermMemory:
    """
    Stores long-term memory persistently in a JSON file.
    """

    def __init__(self, file_path="memory_store.json"):
        self.file_path = file_path
        self._memory = self._load()

    def _load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)
        return {}

    def _save(self):
        with open(self.file_path, "w") as f:
            json.dump(self._memory, f, indent=4)

    def store(self, key: str, value):
        self._memory[key] = value
        self._save()

    def retrieve(self, key: str):
        return self._memory.get(key)

    def get_all(self):
        return self._memory
