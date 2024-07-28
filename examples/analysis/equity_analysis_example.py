from pytca.analysis.equities.equity_metrics import calculate_beta

# Example data
asset_returns = [0.01, 0.02, -0.01, 0.03]
market_returns = [0.015, 0.025, -0.005, 0.035]

beta = calculate_beta(asset_returns, market_returns)
print(f"Calculated Beta: {beta}")
