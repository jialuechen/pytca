import pytest
from pytca.analysis.general.metrics import calculate_vwap

def test_calculate_vwap():
    prices = [100, 101, 102, 103, 104]
    volumes = [10, 15, 10, 5, 20]
    vwap = calculate_vwap(prices, volumes)
    assert vwap == pytest.approx(101.9091, 0.0001), "VWAP calculation error"
