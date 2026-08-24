import streamlit as st
from src.data_processor import DataProcessor
from src.utils import apply_custom_theme

apply_custom_theme()

st.title("🔍 Dataset Explorer")

if st.session_state.get('current_df') is not None:
    df = st.session_state.current_df
    
    st.subheader("Data Types")
    st.dataframe(df.dtypes.astype(str).reset_index().rename(columns={'index': 'Column', 0: 'Type'}), use_container_width=True)
    
    st.subheader("Descriptive Statistics")
    st.dataframe(df.describe(include='all'), use_container_width=True)
    
    st.subheader("Interactive Data Editor")
    st.caption("You can directly edit cell values below. Click **Save Edits** to apply your changes.")
    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    
    if st.button("💾 Save Edits", type="primary"):
        st.session_state.current_df = edited_df
        st.success("✅ Edits saved to current dataset!")
        st.rerun()
    
    # Export
    st.divider()
    csv_data = DataProcessor.get_csv_download_link(df)
    st.download_button(
        label="Download Transformed Data (CSV)",
        data=csv_data,
        file_name="transformed_data.csv",
        mime="text/csv"
    )
else:
    st.warning("No dataset loaded. Please upload a dataset in the Macro Builder.")
