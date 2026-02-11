from memory.memory_manager import MemoryManager

memory = MemoryManager()

print("---- SHORT TERM MEMORY ----")
memory.store_short("current_task", "project planning")
memory.store_short("active_agent", "PlanningAgent")
print(memory.retrieve_short("current_task"))
print(memory.retrieve_short("active_agent"))

print("\n---- LONG TERM MEMORY ----")
memory.store_long("preferred_language", "Python")
memory.store_long("coding_style", "Simple and readable")
print(memory.retrieve_long("preferred_language"))
print(memory.retrieve_long("coding_style"))

print("\n---- FULL MEMORY SNAPSHOT ----")
print(memory.get_full_memory())
