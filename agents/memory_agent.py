class MemoryAgent:
    def __init__(self, memory):
        self.memory = memory

    def get_context(self):
        return self.memory.get_memory_snapshot()
