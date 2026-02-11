class MemoryManager:
    def __init__(self):
        self.short_term = {}
        self.long_term = {}

    # -----------------------------
    # SHORT TERM MEMORY
    # -----------------------------
    def add_short_term(self, key, value):
        self.short_term[key] = value

    def get_short_term(self, key):
        return self.short_term.get(key)

    # -----------------------------
    # LONG TERM MEMORY (optional)
    # -----------------------------
    def add_long_term(self, key, value):
        self.long_term[key] = value

    def get_long_term(self, key):
        return self.long_term.get(key)

    # -----------------------------
    # CLEAR MEMORY (IMPORTANT)
    # -----------------------------
    def clear_all(self):
        self.short_term.clear()
        self.long_term.clear()
