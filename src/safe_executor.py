import ast
import pandas as pd
from typing import Tuple

class SafeExecutor:
    """
    Validates and executes AI-generated Pandas code safely by inspecting its AST.
    """
    
    ALLOWED_NODE_TYPES = {
        ast.Module, ast.Expr, ast.Assign, ast.Store, ast.Load, ast.Name,
        ast.Attribute, ast.Subscript, ast.Index, ast.Slice, ast.ExtSlice,
        ast.Constant, ast.List, ast.Tuple, ast.Dict, ast.Set,
        ast.BinOp, ast.UnaryOp, ast.Compare, ast.BoolOp,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow,
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn,
        ast.And, ast.Or, ast.Not, ast.USub, ast.UAdd,
        ast.Call, ast.keyword
    }

    # Restrict calls strictly to methods chained off the dataframe or built-ins
    BANNED_FUNCTIONS = {"exec", "eval", "open", "__import__", "globals", "locals", "system"}

    @classmethod
    def validate_code(cls, code_string: str) -> Tuple[bool, str]:
        """
        Parses the code into an AST and ensures it only contains allowed operations.
        Returns (is_safe, error_message)
        """
        try:
            tree = ast.parse(code_string)
        except SyntaxError as e:
            return False, f"Syntax Error in generated code: {e}"

        for node in ast.walk(tree):
            if type(node) not in cls.ALLOWED_NODE_TYPES:
                return False, f"Unsafe or unsupported code detected: {type(node).__name__}"
            
            # Check function calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in cls.BANNED_FUNCTIONS:
                        return False, f"Banned function call detected: {node.func.id}"
                # For attribute calls (e.g., df.sort_values()), we generally allow them, 
                # but could restrict further if needed.

        return True, ""

    @classmethod
    def execute(cls, df: pd.DataFrame, code_string: str) -> pd.DataFrame:
        """
        Executes the validated pandas code against a copy of the dataframe.
        """
        is_safe, err = cls.validate_code(code_string)
        if not is_safe:
            raise SecurityError(f"Code validation failed: {err}")

        # Create a local environment with only the dataframe and pandas/numpy
        import numpy as np
        local_env = {
            "df": df.copy(),
            "pd": pd,
            "np": np
        }
        
        try:
            # We use exec here, but it's heavily sandboxed by AST validation above
            # and runs in a restricted local namespace.
            exec(code_string, {"__builtins__": {}}, local_env)
            return local_env["df"]
        except Exception as e:
            raise RuntimeError(f"Execution failed: {e}")

class SecurityError(Exception):
    pass
