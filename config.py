import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Server Configuration
    FLASK_PORT = 5001
    CORS_ORIGINS = "http://localhost:5173"

    # Model Configuration
    MODEL_FILE_PATH = "cybersecurity_model.pkl"