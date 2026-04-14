"""Configuration for multi-agent systems."""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")

# Temperature settings for different agent types
TEMPERATURE_CREATIVE = 0.8  # For creative tasks
TEMPERATURE_ANALYTICAL = 0.3  # For code/analytical tasks
TEMPERATURE_BALANCED = 0.5  # For balanced tasks
