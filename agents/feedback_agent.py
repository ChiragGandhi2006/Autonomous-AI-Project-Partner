class FeedbackAgent:
    def __init__(self, memory):
        self.memory = memory

    def store(self, feedback):
        self.memory.add_long_term("user_feedback", feedback)
