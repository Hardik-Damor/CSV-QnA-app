import pytest
import pandas as pd
from pathlib import Path
from src.data.csv_handler import CSVHandler

@pytest.fixture
def sample_csv(tmp_path):
    df = pd.DataFrame({
        'price': [10000, 20000, 30000],
        'year': [2020, 2021, 2022],
        'model': ['A', 'B', 'C']
    })
    csv_path = tmp_path / "test.csv"
    df.to_csv(csv_path, index=False)
    return csv_path

def test_valid_csv_load(sample_csv):
    handler = CSVHandler()
    assert handler.load_csv(str(sample_csv)) is True
    assert handler.df is not None

def test_file_not_found():
    handler = CSVHandler()
    assert handler.load_csv('nonexistent.csv') is False

def test_get_column_info(sample_csv):
    handler = CSVHandler()
    handler.load_csv(str(sample_csv))
    info = handler.get_column_info()
    assert 'columns' in info
    assert 'dtypes' in info
    assert 'summary' in info