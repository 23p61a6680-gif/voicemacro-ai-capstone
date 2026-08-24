import streamlit as st
import pandas as pd
from src.data_processor import DataProcessor
from src.gemini_client import GeminiClient
from src.audio_processor import AudioProcessor
from src.code_generator import CodeGenerator
from src.safe_executor import SafeExecutor
from src.visualization import VisualizationEngine
from src.utils import apply_custom_theme

apply_custom_theme()

st.title("⚙️ Macro Builder")

# --- DATA UPLOAD ---
st.header("1. Upload Dataset")
uploaded_file = st.file_uploader("Upload CSV or Excel file", type=['csv', 'xlsx', 'xls'])

if uploaded_file is not None:
    if st.session_state.get('uploaded_filename') != uploaded_file.name:
        try:
            df = DataProcessor.load_data(uploaded_file)
            st.session_state.original_df = df.copy()
            st.session_state.current_df = df.copy()
            st.session_state.uploaded_filename = uploaded_file.name
            st.session_state.history = []
            if 'last_generated' in st.session_state:
                del st.session_state.last_generated
            st.success("New file uploaded successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Error loading file: {e}")
if st.session_state.get('current_df') is not None:
    df = st.session_state.current_df
    
    with st.expander("Preview Current Dataset"):
        st.dataframe(df.head(10))
        
    # --- COMMAND INPUT ---
    st.header("2. Describe Operation")
    
    input_method = st.radio("Choose Input Method", ["Text", "Voice", "Camera 📷"])
    command = ""
    
    if input_method == "Text":
        with st.form("text_command_form"):
            text_input = st.text_input("What would you like to do?")
            submitted = st.form_submit_button("Generate Automation")
            if submitted and text_input:
                command = text_input
    elif input_method == "Voice":
        st.info("Click the microphone below to record your command.")
        # Native Streamlit audio input (requires modern Streamlit)
        audio_val = st.audio_input("Record Command")
        if audio_val:
            st.audio(audio_val)
            if st.button("Transcribe & Generate Automation"):
                with st.spinner("Transcribing..."):
                    try:
                        ap = AudioProcessor()
                        command = ap.transcribe_audio(audio_val.getvalue())
                        st.success(f"Transcribed: '{command}'")
                    except Exception as e:
                        st.error(f"Transcription failed: {e}")
    else:
        # Camera Input - Gemini Vision multimodality
        st.info("📷 Take a photo of a handwritten or printed spreadsheet command. Gemini Vision will read it for you!")
        camera_image = st.camera_input("Capture your command")
        if camera_image:
            st.image(camera_image, caption="Captured Image", width=300)
            if st.button("Read & Generate Automation"):
                with st.spinner("Reading image with Gemini Vision..."):
                    try:
                        gc = GeminiClient()
                        from google.genai import types
                        vision_response = gc.client.models.generate_content(
                            model="gemini-3.6-flash",
                            contents=[
                                types.Part.from_bytes(
                                    data=camera_image.getvalue(),
                                    mime_type="image/jpeg"
                                ),
                                "Read the text in this image. It contains a data operation command for a spreadsheet. Extract ONLY the command text, nothing else."
                            ]
                        )
                        command = vision_response.text.strip()
                        st.success(f"Vision Read: '{command}'")
                    except Exception as e:
                        st.error(f"Vision reading failed: {e}")

    # --- AI GENERATION ---
    if command:
        st.header("3. AI Generation")
        with st.spinner("Analyzing request..."):
            try:
                gc = GeminiClient()
                prompt = CodeGenerator.construct_prompt(df, command)
                sys_inst = CodeGenerator.get_system_instruction()
                
                response_json = gc.generate_code_from_prompt(sys_inst, prompt)
                
                if response_json:
                    st.session_state.last_generated = response_json
                    st.session_state.last_command = command
                    st.session_state.last_input_type = input_method
                    
            except Exception as e:
                st.error(f"AI Generation Failed: {e}")
                
    # --- PREVIEW & EXECUTION ---
    if 'last_generated' in st.session_state:
        gen = st.session_state.last_generated
        
        st.subheader("💡 AI Understanding")
        st.info(f"**Intent:** {gen.get('intent', 'Unknown')}\n\n**What this will do:** {gen.get('explanation', '')}")
        
        with st.expander("🛠️ Technical Details (For Engineers)"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### Pandas Code")
                st.code(gen.get("pandas_code", ""), language="python")
            with col2:
                st.markdown("### Excel VBA Equivalent")
                st.code(gen.get("excel_vba_code", ""), language="vba")
            
        risk = gen.get("risk_level", "UNKNOWN")
        if risk == "HIGH":
            st.warning("⚠️ High Risk Operation Detected. Review carefully.")
        
        st.write("---")
        if st.button("✨ Apply Changes", type="primary"):
            pandas_code = gen.get("pandas_code", "")
            try:
                # Execution
                rows_before = df.shape[0]
                new_df = SafeExecutor.execute(df, pandas_code)
                rows_after = new_df.shape[0]
                
                # Update State
                st.session_state.current_df = new_df
                
                # Initialize history if missing
                if 'history' not in st.session_state:
                    st.session_state.history = []
                
                # Log History
                record = DataProcessor.create_history_record(
                    st.session_state.last_command,
                    st.session_state.last_input_type,
                    gen.get("intent", ""),
                    pandas_code,
                    gen.get("excel_vba_code", ""),
                    True,
                    abs(rows_after - rows_before)
                )
                st.session_state.history.append(record)
                
                # Clear generated state
                del st.session_state.last_generated
                st.success("✅ Changes applied successfully!")
                st.rerun()
                
            except Exception as e:
                st.error(f"Execution Error: {e}")
                
                if 'history' not in st.session_state:
                    st.session_state.history = []
                    
                record = DataProcessor.create_history_record(
                    st.session_state.last_command,
                    st.session_state.last_input_type,
                    gen.get("intent", ""),
                    pandas_code,
                    gen.get("excel_vba_code", ""),
                    False,
                    0,
                    str(e)
                )
                st.session_state.history.append(record)

    # --- VISUALIZATION ---
    st.divider()
    VisualizationEngine.recommend_and_render(df)
    
    # --- RESET ---
    st.divider()
    if st.button("Reset Dataset to Original"):
        st.session_state.current_df = st.session_state.original_df.copy()
        st.session_state.history = []
        if 'last_generated' in st.session_state:
            del st.session_state.last_generated
        st.success("Dataset reset!")
        st.rerun()
