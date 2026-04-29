from core.orchestrator import Orchestrator
from services.image_service import ImageService
from services.code_generation_service import CodeGenerationService

orchestrator = Orchestrator()
image_service = ImageService()
code_service = CodeGenerationService()

# Global state
project_state = {
    "initialized": False,
    "last_image": None   # 🔥 for future editing support
}


def handle_user_input(user_input, llm):
    """
    Handles:
    - First message → Idea + Plan + Workflow
    - Normal chat
    - Code → Gemini
    - Image → OpenAI
    """

    text = user_input.lower()

    # 🔹 KEYWORDS
    plan_keywords = ["plan", "workflow", "idea", "architecture"]
    image_keywords = ["image", "draw", "picture", "generate image", "create image"]
    code_keywords = ["code", "program", "function", "script"]

    # 🔹 IMAGE GENERATION (OpenAI)
    if any(word in text for word in image_keywords):
        image_path = image_service.generate_image(user_input)

        # store last image
        project_state["last_image"] = image_path

        return {
            "type": "image",
            "data": image_path
        }

    # 🔹 CODE GENERATION (Gemini)
    elif any(word in text for word in code_keywords):
        code = code_service.generate_code(user_input)

        return {
            "type": "code",
            "data": code
        }

    # 🔹 PLAN / WORKFLOW MODE
    if not project_state["initialized"]:
        mode = "init"
        project_state["initialized"] = True

    elif any(word in text for word in plan_keywords):
        mode = "init"

    else:
        mode = "chat"

    # 🔹 PROMPT BUILDING
    if mode == "init":
        prompt = f"""
You are an AI Project Planner.

User request:
{user_input}

Generate:
1. Project Idea (if relevant)
2. Step-by-step Plan
3. Workflow

Keep it clear and structured.
"""

    else:
        prompt = f"""
You are a helpful AI assistant.

Answer normally like ChatGPT.
Do NOT generate idea/plan/workflow unless user explicitly asks.

User: {user_input}
"""

    # 🔹 LLM RESPONSE (your existing model)
    response = llm.generate(prompt)

    return {
        "type": "text",
        "data": response
    }