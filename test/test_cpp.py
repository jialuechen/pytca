import pytest
import numpy as np
from pytca.cpp import calculate_vwap

def test_calculate_vwap():
    # Test data
    prices = np.array([100.0, 101.0, 102.0, 103.0, 104.0])
    volumes = np.array([10.0, 15.0, 10.0, 5.0, 20.0])

    # Expected VWAP calculation
    expected_vwap = (100.0 * 10.0 + 101.0 * 15.0 + 102.0 * 10.0 + 103.0 * 5.0 + 104.0 * 20.0) / (10.0 + 15.0 + 10.0 + 5.0 + 20.0)

    # Calculate VWAP using the C++ module
    vwap = calculate_vwap(prices, volumes)

    # Assertion to check if the VWAP calculated by the C++ module is correct
    assert np.isclose(vwap, expected_vwap, atol=1e-6), f"VWAP calculation error: expected {expected_vwap}, got {vwap}"
