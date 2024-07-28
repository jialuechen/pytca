import pytest
from pytca.data.loaders.csv_loader import load_csv_data

def test_load_csv_data():
    data = load_csv_data('tests/data/sample_data.csv')
    assert not data.empty, "Data should not be empty"
