import streamlit as st
import pandas as pd
from src.utils import apply_custom_theme

apply_custom_theme()

st.title("🕒 Execution History")

history = st.session_state.get('history', [])

if history:
    st.write("Review all operations performed on your dataset during this session.")
    
    # Create DataFrame from history for nice table display
    history_df = pd.DataFrame(history)
    
    # Reorder/rename columns for display
    display_df = history_df[['timestamp', 'command', 'input_type', 'intent', 'success', 'rows_affected']].copy()
    
    st.dataframe(display_df, use_container_width=True)
    
    st.divider()
    
    st.subheader("Detailed Logs")
    for i, record in enumerate(reversed(history)):
        with st.expander(f"Operation {len(history) - i}: {record['intent']}"):
            st.write(f"**Command:** {record['command']} ({record['input_type']})")
            st.write(f"**Timestamp:** {record['timestamp']}")
            st.write(f"**Success:** {'✅' if record['success'] else '❌'}")
            if not record['success']:
                st.error(f"Error: {record['error_message']}")
            else:
                st.write(f"**Rows Affected:** {record['rows_affected']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.code(record['pandas_code'], language='python')
            with col2:
                if record['vba_code']:
                    st.code(record['vba_code'], language='vba')
else:
    st.info("No operations have been executed yet.")

