import pytest
import pandas as pd
from src.safe_executor import SafeExecutor, SecurityError

def test_safe_executor_valid_code():
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    code = "df = df[df['A'] > 1]"
    new_df = SafeExecutor.execute(df, code)
    
    assert len(new_df) == 2
    assert 1 not in new_df['A'].values

def test_safe_executor_banned_code():
    df = pd.DataFrame({'A': [1, 2, 3]})
    code = "import os; os.system('ls')"
    
    with pytest.raises(SecurityError):
        SafeExecutor.execute(df, code)

def test_safe_executor_eval_blocked():
    df = pd.DataFrame({'A': [1, 2, 3]})
    code = "df['B'] = eval('1+1')"
    
    with pytest.raises(SecurityError):
        SafeExecutor.execute(df, code)
