import pandas as pd
import io
from typing import Optional, Tuple
from datetime import datetime

class DataProcessor:
    @staticmethod
    def load_data(uploaded_file) -> pd.DataFrame:
        """Loads a CSV or Excel file into a pandas DataFrame."""
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(uploaded_file)
        else:
            raise ValueError("Unsupported file format. Please upload CSV or Excel.")
        return df
        
    @staticmethod
    def get_metadata(df: pd.DataFrame) -> dict:
        """Returns metadata about the DataFrame for the dashboard."""
        return {
            "rows": df.shape[0],
            "cols": df.shape[1],
            "missing_values": int(df.isna().sum().sum()),
            "numeric_cols": len(df.select_dtypes(include='number').columns),
            "categorical_cols": len(df.select_dtypes(include=['object', 'category', 'str']).columns),
            "date_cols": len(df.select_dtypes(include='datetime').columns)
        }
        
    @staticmethod
    def get_csv_download_link(df: pd.DataFrame) -> str:
        """Returns CSV string for downloading."""
        return df.to_csv(index=False)
        
    @staticmethod
    def create_history_record(command: str, input_type: str, intent: str, 
                              pandas_code: str, vba_code: str, success: bool, 
                              rows_affected: int, error_msg: str = "") -> dict:
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "command": command,
            "input_type": input_type,
            "intent": intent,
            "pandas_code": pandas_code,
            "vba_code": vba_code,
            "success": success,
            "rows_affected": rows_affected,
            "error_message": error_msg
        }
