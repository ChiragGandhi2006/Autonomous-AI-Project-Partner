from memory.memory_manager import MemoryManager
from services.code_generation_service import CodeGenerationService
from services.evaluation_service import EvaluationService
from services.error_analysis_service import ErrorAnalysisService

from agents.ideation_agent import IdeationAgent
from agents.planning_agent import PlanningAgent
from agents.coder_agent import CoderAgent
from agents.debugger_agent import DebuggerAgent
from agents.review_agent import ReviewAgent
from agents.feedback_agent import FeedbackAgent
from agents.memory_agent import MemoryAgent


def main():
    memory = MemoryManager()

    code_service = CodeGenerationService()
    eval_service = EvaluationService()
    error_service = ErrorAnalysisService()

    ideation = IdeationAgent(memory)
    planning = PlanningAgent(memory)
    coder = CoderAgent(memory, code_service)
    debugger = DebuggerAgent(memory, error_service)
    reviewer = ReviewAgent(memory, eval_service)
    feedback = FeedbackAgent(memory)
    memory_agent = MemoryAgent(memory)

    idea = ideation.act("Build an AI-powered chatbot")
    plan = planning.act()
    code = coder.act("Create a Flask REST API")
    review = reviewer.act(code)
    fix = debugger.act("IndexError: list index out of range")
    feedback_msg = feedback.act("Code quality is good")

    print("IDEA:", idea)
    print("PLAN:", plan)
    print("CODE:", code)
    print("REVIEW:", review)
    print("DEBUG FIX:", fix)
    print("MEMORY SNAPSHOT:", memory_agent.get_context())


if __name__ == "__main__":
    main()
