import streamlit as st
import pandas as pd
from src.utils import apply_custom_theme

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="VoiceMacro AI",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_custom_theme()

# Initialize core session state variables
if 'original_df' not in st.session_state:
    st.session_state.original_df = None
if 'current_df' not in st.session_state:
    st.session_state.current_df = None
if 'history' not in st.session_state:
    st.session_state.history = []

def main():
    st.title("🎙️ VoiceMacro AI")
    st.markdown("### Welcome to your AI-Powered Spreadsheet Automation Assistant")
    
    st.write("""
    VoiceMacro AI eliminates the steep learning curve of Pandas and Excel VBA by allowing you to manipulate data using simple natural language commands. 
    Simply upload your dataset in the **Macro Builder**, tell the AI what you want to achieve, and watch as it generates and safely applies the transformations.
    """)
    
    st.info("👈 Please select a page from the sidebar to begin.")
    
    # Feature Highlights
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🗣️ Voice & Text")
        st.write("Interact with your data using natural speech or by typing commands.")
        
    with col2:
        st.subheader("🛡️ Safe Execution")
        st.write("Generated code is parsed and validated before execution to prevent malicious actions.")
        
    with col3:
        st.subheader("📊 Visual Analytics")
        st.write("Automatically recommends and renders interactive charts based on your data.")

if __name__ == "__main__":
    main()
