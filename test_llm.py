from services.llm_service import LLMService

llm = LLMService()
print(llm.generate_response("Write a simple Flask REST API"))
