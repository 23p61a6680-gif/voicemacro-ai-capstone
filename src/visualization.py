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

        if not numeric_cols:
            st.info("No numeric columns found for visualization.")
            return

        # Simple heuristic: If we have numeric columns, show distributions
        st.subheader("📊 Automatic Visualizations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribution of first numeric column
            target_col = numeric_cols[0]
            fig_hist = px.histogram(df, x=target_col, title=f"Distribution of {target_col}")
            st.plotly_chart(fig_hist, use_container_width=True)
            
        with col2:
            # If categorical exists, group by first categorical and sum first numeric
            if cat_cols and len(df[cat_cols[0]].unique()) < 20:
                cat_col = cat_cols[0]
                grouped = df.groupby(cat_col)[target_col].sum().reset_index()
                fig_bar = px.bar(grouped, x=cat_col, y=target_col, 
                                 title=f"Total {target_col} by {cat_col}")
                st.plotly_chart(fig_bar, use_container_width=True)
            elif len(numeric_cols) > 1:
                # Scatter plot if multiple numeric
                fig_scatter = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1],
                                         title=f"{numeric_cols[0]} vs {numeric_cols[1]}")
                st.plotly_chart(fig_scatter, use_container_width=True)
            else:
                st.info("Add categorical data for more chart types.")
