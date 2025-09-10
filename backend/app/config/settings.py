"""
Application configuration settings
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # Qdrant configuration
    QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
    
    # Gemini configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # Application settings
    APP_NAME = "RevenueLeakageDetection"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()