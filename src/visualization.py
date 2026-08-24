import plotly.express as px
import pandas as pd
import streamlit as st

class VisualizationEngine:
    @staticmethod
    def recommend_and_render(df: pd.DataFrame):
        """Automatically recommends and renders charts based on dataframe schema."""
        if df.empty:
            st.info("Dataset is empty. No visualizations available.")
            return

        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        cat_cols = df.select_dtypes(include=['object', 'category', 'str']).columns.tolist()

        st.subheader("📊 Data Visualizations")
        
        tab1, tab2 = st.tabs(["Auto Graphs", "Custom Graph Builder"])
        
        with tab1:
            if not numeric_cols:
                st.info("No numeric columns found for automatic visualization. Use the Custom Graph Builder to manually create charts (e.g., counting categories).")
            else:
                st.caption("Automatic distributions based on your data.")
                col1, col2 = st.columns(2)
                with col1:
                    target_col = numeric_cols[0]
                    fig_hist = px.histogram(df, x=target_col, title=f"Distribution of {target_col}")
                    st.plotly_chart(fig_hist, use_container_width=True)
                    
                with col2:
                    if cat_cols and len(df[cat_cols[0]].unique()) < 40:
                        cat_col = cat_cols[0]
                        grouped = df.groupby(cat_col)[target_col].sum().reset_index()
                        fig_bar = px.bar(grouped, x=cat_col, y=target_col, 
                                         title=f"Total {target_col} by {cat_col}")
                        st.plotly_chart(fig_bar, use_container_width=True)
                    elif len(numeric_cols) > 1:
                        fig_scatter = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1],
                                                 title=f"{numeric_cols[0]} vs {numeric_cols[1]}")
                        st.plotly_chart(fig_scatter, use_container_width=True)
                    else:
                        st.info("Add categorical data for more automatic charts.")
                    
        with tab2:
            st.caption("Build your own custom graph from the current dataset.")
            chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart"])
            
            col_x, col_y = st.columns(2)
            with col_x:
                x_axis = st.selectbox("X-Axis", df.columns.tolist())
            with col_y:
                y_axis = st.selectbox("Y-Axis", df.columns.tolist(), index=min(1, len(df.columns)-1))
                
            if st.button("Generate Custom Graph"):
                try:
                    if chart_type == "Bar Chart":
                        fig = px.bar(df, x=x_axis, y=y_axis)
                    elif chart_type == "Line Chart":
                        fig = px.line(df, x=x_axis, y=y_axis)
                    elif chart_type == "Scatter Plot":
                        fig = px.scatter(df, x=x_axis, y=y_axis)
                    elif chart_type == "Pie Chart":
                        fig = px.pie(df, names=x_axis, values=y_axis)
                        
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Could not generate graph: {e}")
