import streamlit as st
import pandas as pd
from src.gemini_client import GeminiClient
from src.code_generator import CodeGenerator
from src.utils import apply_custom_theme

apply_custom_theme()

st.title("💡 AI Data Insights")

if st.session_state.get('current_df') is not None:
    df = st.session_state.current_df
    
    st.write("Ask the AI to analyze your dataset and explain it in plain English.")
    
    with st.expander("Preview Dataset"):
        st.dataframe(df.head(5))
        
    st.divider()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("General Analysis")
        st.write("Click here to get a high-level overview and trends of the current dataset.")
        if st.button("Generate General Analysis"):
            with st.spinner("Analyzing dataset..."):
                try:
                    gc = GeminiClient()
                    sys_inst = CodeGenerator.get_insights_system_instruction()
                    prompt = CodeGenerator.construct_insights_prompt(df)
                    
                    analysis = gc.generate_text_from_prompt(sys_inst, prompt)
                    st.session_state.last_analysis = analysis
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
                    
        st.divider()
        st.subheader("Ask a Specific Question")
        with st.form("custom_question_form"):
            user_q = st.text_area("e.g. 'Why is the average revenue so high in the North region?'")
            submit_q = st.form_submit_button("Ask AI")
            
            if submit_q and user_q:
                with st.spinner("Generating answer..."):
                    try:
                        gc = GeminiClient()
                        sys_inst = CodeGenerator.get_insights_system_instruction()
                        prompt = CodeGenerator.construct_insights_prompt(df, user_q)
                        
                        analysis = gc.generate_text_from_prompt(sys_inst, prompt)
                        st.session_state.last_analysis = analysis
                    except Exception as e:
                        st.error(f"Analysis failed: {e}")
                        
    with col2:
        st.subheader("AI Explanation")
        if 'last_analysis' in st.session_state:
            st.markdown(st.session_state.last_analysis)
        else:
            st.info("No analysis generated yet. Click the button or ask a question to begin.")
            
else:
    st.warning("No dataset loaded. Please upload a dataset in the Macro Builder first.")
