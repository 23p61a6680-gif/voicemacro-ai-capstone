import pytest
from src.code_generator import CodeGenerator
import pandas as pd

def test_system_instruction_contains_json_requirement():
    instruction = CodeGenerator.get_system_instruction()
    assert "JSON" in instruction
    assert "pandas_code" in instruction

def test_prompt_construction():
    df = pd.DataFrame({'A': [1, 2], 'B': ['x', 'y']})
    command = "Filter A > 1"
    
    prompt = CodeGenerator.construct_prompt(df, command)
    
    assert "A" in prompt
    assert "B" in prompt
    assert command in prompt
    assert "Shape" in prompt
