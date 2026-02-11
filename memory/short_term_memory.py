# memory/short_term_memory.py

class ShortTermMemory:
    """
    Stores temporary context for the current session.
    """

    def __init__(self):
        self._memory = {}

    def store(self, key: str, value):
        self._memory[key] = value

    def retrieve(self, key: str):
        return self._memory.get(key)

    def clear(self):
        self._memory.clear()

    def get_all(self):
        return self._memory
