import pytest
import pandas as pd
from io import BytesIO
from src.data_processor import DataProcessor

def test_get_metadata():
    df = pd.DataFrame({
        'A': [1, 2, None],
        'B': ['x', 'y', 'z'],
        'C': pd.to_datetime(['2020-01-01', '2020-01-02', '2020-01-03'])
    })
    
    metadata = DataProcessor.get_metadata(df)
    
    assert metadata['rows'] == 3
    assert metadata['cols'] == 3
    assert metadata['missing_values'] == 1
    assert metadata['numeric_cols'] == 1
    assert metadata['categorical_cols'] == 1
    assert metadata['date_cols'] == 1

def test_create_history_record():
    record = DataProcessor.create_history_record(
        command="test",
        input_type="Text",
        intent="Testing",
        pandas_code="df=df",
        vba_code="",
        success=True,
        rows_affected=5
    )
    
    assert record['command'] == "test"
    assert record['success'] is True
    assert record['rows_affected'] == 5
    assert 'timestamp' in record
