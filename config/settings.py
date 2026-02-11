# config/settings.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """
    Central configuration class for the project.
    """

    # Application
    APP_NAME = "Autonomous AI Project Partner"
    DEBUG = os.getenv("DEBUG", "True") == "True"

    # LLM / AI Configuration
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.7))

    # Memory
    MEMORY_TYPE = os.getenv("MEMORY_TYPE", "in_memory")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


# Singleton settings object
settings = Settings()



