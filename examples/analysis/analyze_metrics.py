from pytca.analysis.general.metrics import calculate_vwap
from pytca.analysis.equities.equity_metrics import calculate_beta
import numpy as np

# Example data for VWAP calculation
prices = np.array([100.0, 101.0, 102.0, 103.0, 104.0])
volumes = np.array([10.0, 15.0, 10.0, 5.0, 20.0])

# Calculate VWAP
vwap = calculate_vwap(prices, volumes)
print(f"Volume Weighted Average Price (VWAP): {vwap}")

# Example data for Beta calculation
# Asset returns and market returns over the same period
asset_returns = np.array([0.01, 0.02, -0.01, 0.03, 0.04])
market_returns = np.array([0.015, 0.025, -0.005, 0.035, 0.045])

# Calculate Beta
beta = calculate_beta(asset_returns, market_returns)
print(f"Beta: {beta}")
