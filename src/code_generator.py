import pandas as pd
from typing import Dict, Any

class CodeGenerator:
    @staticmethod
    def get_system_instruction() -> str:
        return """You are VoiceMacro AI, an expert Python Pandas and Excel automation engineer.
Your task is to convert natural language commands into safe, valid Pandas DataFrame operations and equivalent Excel VBA code.
You must output ONLY structured JSON following this exact schema:

{
    "intent": "Brief summary of what the code will do",
    "explanation": "Human-readable explanation of the operation",
    "pandas_code": "The pandas python code. MUST act on a dataframe named 'df'. Only generate the assignment or operation, do NOT include print statements or imports.",
    "excel_vba_code": "The equivalent VBA macro code, if applicable.",
    "required_columns": ["col1", "col2"],
    "risk_level": "LOW, MEDIUM, or HIGH",
    "expected_result": "Description of the resulting dataset"
}

RULES FOR pandas_code:
1. The input dataframe is always named `df`.
2. Do NOT wrap the code in a function.
3. The output MUST be assigned back to `df` if it modifies the whole dataframe (e.g., `df = df[df['A'] > 5]`).
4. Only use standard Pandas data manipulation operations.
5. Code must be single-line or basic multi-line without complex logic loops.
6. DO NOT generate ANY plotting or visualization code (no matplotlib, no seaborn, no df.plot). The system automatically renders charts based on the resulting dataframe. Only output data transformation code.
"""

    @staticmethod
    def construct_prompt(df: pd.DataFrame, command: str) -> str:
        # Extract basic metadata
        columns = list(df.columns)
        dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}
        
        # Get a small sample to help the LLM understand the data format
        sample_data = df.head(3).to_dict(orient="records")
        
        prompt = f"""
I have a pandas DataFrame named `df`.

DATASET METADATA:
Columns: {columns}
Data Types: {dtypes}
Sample Data (First 3 rows):
{sample_data}
Shape: {df.shape}

USER COMMAND:
"{command}"

Generate the JSON response to fulfill this command safely.
"""
        return prompt

    @staticmethod
    def get_insights_system_instruction() -> str:
        return """You are an expert Data Analyst working with VoiceMacro AI.
Your job is to analyze the statistical summary of a dataset and explain it in plain, human-readable language.
Do NOT generate code. Do NOT output JSON. Use markdown formatting to make your explanation readable, clear, and engaging.
Highlight interesting trends, potential anomalies, or basic takeaways."""

    @staticmethod
    def construct_insights_prompt(df: pd.DataFrame, custom_question: str = "") -> str:
        metadata = {
            "shape": df.shape,
            "columns": list(df.columns),
            "missing_values": df.isna().sum().to_dict()
        }
        
        summary_stats = df.describe(include='all').to_string()
        
        prompt = f"""
Here is the summary of the current dataset:

METADATA:
{metadata}

SUMMARY STATISTICS:
{summary_stats}

"""
        if custom_question:
            prompt += f"\nThe user asked the following specific question about this data: '{custom_question}'\nPlease answer this question using the provided data."
        else:
            prompt += "\nPlease provide a general human-readable analysis of this dataset."
            
        return prompt
