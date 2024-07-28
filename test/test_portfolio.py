import pytest
import numpy as np
from pytca.portfolio.optimization import calculate_portfolio_variance, optimize_portfolio

def test_calculate_portfolio_variance():
    weights = np.array([0.4, 0.3, 0.3])
    cov_matrix = np.array([[0.01, 0.0018, 0.0011],
                           [0.0018, 0.04, 0.0023],
                           [0.0011, 0.0023, 0.02]])
    
    expected_variance = 0.00483  # Pre-calculated expected variance
    variance = calculate_portfolio_variance(weights, cov_matrix)
    
    assert np.isclose(variance, expected_variance, atol=1e-6), f"Variance calculation error: expected {expected_variance}, got {variance}"

def test_optimize_portfolio():
    returns = [0.1, 0.2, 0.15]
    cov_matrix = np.array([[0.01, 0.0018, 0.0011],
                           [0.0018, 0.04, 0.0023],
                           [0.0011, 0.0023, 0.02]])
    risk_tolerance = 0.1
    
    weights = optimize_portfolio(returns, cov_matrix, risk_tolerance)
    
    assert len(weights) == len(returns), "Number of weights should match number of assets"
    assert np.isclose(np.sum(weights), 1, atol=1e-6), f"Weights should sum to 1, got sum {np.sum(weights)}"
    assert all(w >= 0 for w in weights), "All weights should be non-negative"
