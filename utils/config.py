import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

class Config:
    # API Keys
    GEMMA_26B_KEY = os.getenv("GEMMA_26B_API_KEY")
    GEMMA_31B_KEY = os.getenv("GEMMA_31B_API_KEY")
    
    # Model Identifiers (2026 Standard)
    MODEL_26B = "gemini/gemma-4-26b-it"
    MODEL_31B = "gemini/gemma-4-31b-it"
    
    # Local Settings
    LOCAL_MODEL = "ollama/gemma4-e2b"