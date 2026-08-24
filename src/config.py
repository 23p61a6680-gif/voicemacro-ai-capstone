import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# App Constants
APP_NAME = "VoiceMacro AI"
APP_VERSION = "1.0.0"

# Gemini Config
GEMINI_MODEL = "gemini-3.6-flash"  # Flash is fast and cheap, ideal for this use case
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Safety Config
ALLOWED_MODULES = ["pandas", "numpy", "datetime"]
MAX_DATASET_ROWS = 1000000 # Reasonable limit for browser-based tool

def get_api_key():
    import streamlit as st
    try:
        # Try to get from streamlit secrets first (deployment)
        key = st.secrets.get("GEMINI_API_KEY")
        if key:
            return key
    except Exception:
        pass
    
    # Fallback to env var
    return GEMINI_API_KEY
