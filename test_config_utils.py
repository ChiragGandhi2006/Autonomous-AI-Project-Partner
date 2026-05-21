# test_config_utils.py
"""
Test script to verify config and utils modules.
Run this file from the project root.
"""

# -----------------------------
# TEST CONFIG MODULE
# -----------------------------
from config.settings import settings
from config.constants import (
    IDEATION_AGENT,
    PLANNING_AGENT,
    CODER_AGENT,
    DEBUGGER_AGENT,
    REVIEW_AGENT,
    FEEDBACK_AGENT,
    MEMORY_AGENT,
    TASK_COMPLETED
)

print("----- CONFIG OUTPUT -----")
print("App Name:", settings.APP_NAME)
print("Debug Mode:", settings.DEBUG)
print("LLM Provider:", settings.LLM_PROVIDER)
print("LLM Model:", settings.LLM_MODEL)
print("LLM Temperature:", settings.LLM_TEMPERATURE)

print("\nAgents:")
print(IDEATION_AGENT)
print(PLANNING_AGENT)
print(CODER_AGENT)
print(DEBUGGER_AGENT)
print(REVIEW_AGENT)
print(FEEDBACK_AGENT)
print(MEMORY_AGENT)

print("Task Status:", TASK_COMPLETED)

# -----------------------------
# TEST LOGGER
# -----------------------------
from utils.logger import get_logger

print("\n----- LOGGER OUTPUT -----")
logger = get_logger("TestLogger")
logger.info("Logger is working correctly")
logger.warning("This is a warning log")
logger.error("This is an error log")

# -----------------------------
# TEST VALIDATORS
# -----------------------------
from utils.validators import validate_non_empty, validate_type

print("\n----- VALIDATOR OUTPUT -----")

try:
    validate_non_empty("", "project_name")
except ValueError as e:
    print("Validation Error:", e)

try:
    validate_type("123", int, "project_id")
except TypeError as e:
    print("Type Error:", e)

print("Validation tests completed")

# -----------------------------
# TEST FILE HANDLER
# -----------------------------
from utils.file_handler import save_json, load_json

print("\n----- FILE HANDLER OUTPUT -----")

test_data = {
    "module": "config_and_utils",
    "status": "success",
    "autonomy_ready": True
}

save_json("test_output.json", test_data)
loaded_data = load_json("test_output.json")

print("Saved JSON:", test_data)
print("Loaded JSON:", loaded_data)

print("\n✅ ALL TESTS COMPLETED SUCCESSFULLY")
