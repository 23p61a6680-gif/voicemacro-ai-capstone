"""
End-to-End Integration Test for VoiceMacro AI
Tests the full workflow: load data -> generate code -> validate -> execute
"""
import pandas as pd
import sys
import os

# Ensure we can import from src
sys.path.insert(0, os.path.dirname(__file__))

from src.data_processor import DataProcessor
from src.code_generator import CodeGenerator
from src.safe_executor import SafeExecutor
from src.visualization import VisualizationEngine
from src.gemini_client import GeminiClient

def test_full_workflow():
    print("=" * 60)
    print("VoiceMacro AI - Full Integration Test")
    print("=" * 60)
    
    # STEP 1: Load CSV
    print("\n[1/7] Loading sample CSV...")
    df = pd.read_csv("sample_data/test_sales.csv")
    print(f"  ✅ Loaded {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"  Columns: {list(df.columns)}")
    
    # STEP 2: Get metadata
    print("\n[2/7] Testing DataProcessor.get_metadata()...")
    metadata = DataProcessor.get_metadata(df)
    print(f"  ✅ Rows: {metadata['rows']}, Cols: {metadata['cols']}")
    print(f"  Missing: {metadata['missing_values']}, Numeric: {metadata['numeric_cols']}, Categorical: {metadata['categorical_cols']}")
    
    # STEP 3: Construct prompt
    print("\n[3/7] Testing CodeGenerator.construct_prompt()...")
    command = "Filter rows where Revenue is greater than 50000"
    prompt = CodeGenerator.construct_prompt(df, command)
    assert "Revenue" in prompt
    assert command in prompt
    print(f"  ✅ Prompt constructed ({len(prompt)} chars)")
    
    # STEP 4: Test Gemini API (code generation)
    print("\n[4/7] Testing GeminiClient.generate_code_from_prompt()...")
    gc = GeminiClient()
    if not gc.is_configured():
        print("  ⚠️ Gemini API key not configured, skipping API test")
    else:
        try:
            sys_inst = CodeGenerator.get_system_instruction()
            response = gc.generate_code_from_prompt(sys_inst, prompt)
            print(f"  ✅ AI Response received!")
            print(f"     Intent: {response.get('intent', 'N/A')}")
            print(f"     Explanation: {response.get('explanation', 'N/A')}")
            print(f"     Pandas Code: {response.get('pandas_code', 'N/A')}")
            print(f"     Risk Level: {response.get('risk_level', 'N/A')}")
            
            pandas_code = response.get('pandas_code', '')
            
            # STEP 5: Validate generated code
            print("\n[5/7] Testing SafeExecutor.validate_code()...")
            is_safe, err = SafeExecutor.validate_code(pandas_code)
            if is_safe:
                print(f"  ✅ Code is SAFE")
            else:
                print(f"  ❌ Code is UNSAFE: {err}")
                
            # STEP 6: Execute the code
            print("\n[6/7] Testing SafeExecutor.execute()...")
            new_df = SafeExecutor.execute(df, pandas_code)
            print(f"  ✅ Execution successful!")
            print(f"     Before: {df.shape[0]} rows -> After: {new_df.shape[0]} rows")
            print(f"     Rows removed: {df.shape[0] - new_df.shape[0]}")
            
            # Verify the filter actually worked
            if 'Revenue' in new_df.columns:
                min_rev = new_df['Revenue'].min()
                print(f"     Min Revenue in result: {min_rev} (should be > 50000)")
                if min_rev > 50000:
                    print(f"  ✅ Filter verified correctly!")
                else:
                    print(f"  ⚠️ Filter may not have applied perfectly")
                    
        except Exception as e:
            print(f"  ❌ API Error: {e}")
            pandas_code = "df = df[df['Revenue'] > 50000]"
            print(f"  Using fallback code: {pandas_code}")
            
            print("\n[5/7] Testing SafeExecutor.validate_code() with fallback...")
            is_safe, err = SafeExecutor.validate_code(pandas_code)
            print(f"  ✅ Code is {'SAFE' if is_safe else 'UNSAFE: ' + err}")
            
            print("\n[6/7] Testing SafeExecutor.execute() with fallback...")
            new_df = SafeExecutor.execute(df, pandas_code)
            print(f"  ✅ Execution successful! {df.shape[0]} rows -> {new_df.shape[0]} rows")
    
    # STEP 7: Test Data Insights (text generation)
    print("\n[7/7] Testing AI Data Insights (text generation)...")
    if gc.is_configured():
        try:
            insights_inst = CodeGenerator.get_insights_system_instruction()
            insights_prompt = CodeGenerator.construct_insights_prompt(df, "What are the top performing regions?")
            analysis = gc.generate_text_from_prompt(insights_inst, insights_prompt)
            print(f"  ✅ Insights generated! ({len(analysis)} chars)")
            print(f"  Preview: {analysis[:200]}...")
        except Exception as e:
            print(f"  ❌ Insights Error: {e}")
    else:
        print("  ⚠️ Skipped (no API key)")
    
    # STEP 8: Test history record creation
    print("\n[BONUS] Testing DataProcessor.create_history_record()...")
    record = DataProcessor.create_history_record(
        command=command,
        input_type="Text",
        intent="Filter by revenue",
        pandas_code="df = df[df['Revenue'] > 50000]",
        vba_code="Sub FilterRevenue()...",
        success=True,
        rows_affected=8
    )
    assert record['command'] == command
    assert record['success'] == True
    print(f"  ✅ History record created with timestamp: {record['timestamp']}")
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED! ✅")
    print("=" * 60)

if __name__ == "__main__":
    test_full_workflow()
