import streamlit as st
import os
from src.utils import apply_custom_theme

apply_custom_theme()

st.title("ℹ️ About VoiceMacro AI")

# Load and display the README.md content
readme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "README.md")
try:
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()
    st.markdown(readme_content)
except Exception as e:
    st.error(f"Could not load README: {e}")
