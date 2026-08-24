import streamlit as st
from src.data_processor import DataProcessor
from src.utils import apply_custom_theme

apply_custom_theme()

st.title("📊 Dashboard")

if st.session_state.get('current_df') is not None:
    df = st.session_state.current_df
    metadata = DataProcessor.get_metadata(df)
    
    # Calculate deltas from original dataset
    original_df = st.session_state.get('original_df')
    if original_df is not None:
        orig_metadata = DataProcessor.get_metadata(original_df)
        row_delta = metadata['rows'] - orig_metadata['rows']
        col_delta = metadata['cols'] - orig_metadata['cols']
        missing_delta = metadata['missing_values'] - orig_metadata['missing_values']
    else:
        row_delta = col_delta = missing_delta = None
    
    st.subheader("Dataset Overview")
    
    # KPI Cards with deltas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Rows", metadata['rows'], delta=f"{row_delta}" if row_delta else None, 
                  delta_color="normal")
    with col2:
        st.metric("Columns", metadata['cols'], delta=f"{col_delta}" if col_delta else None,
                  delta_color="normal")
    with col3:
        st.metric("Missing Values", metadata['missing_values'], 
                  delta=f"{missing_delta}" if missing_delta else None,
                  delta_color="inverse")
    with col4:
        history = st.session_state.get('history', [])
        st.metric("Operations Performed", len(history))
        
    st.divider()
    
    col_types1, col_types2, col_types3 = st.columns(3)
    with col_types1:
        st.metric("Numeric Columns", metadata['numeric_cols'])
    with col_types2:
        st.metric("Categorical Columns", metadata['categorical_cols'])
    with col_types3:
        st.metric("Date Columns", metadata['date_cols'])
        
else:
    st.warning("No dataset loaded. Please upload a dataset in the Macro Builder.")

