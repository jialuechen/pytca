from pytca.analysis.general.impact import calculate_slippage, calculate_market_impact

# Example data for market impact analysis
initial_price = 100.0  # Initial price of the asset
final_price = 105.0    # Final price after the trade
trade_volume = 1000    # Volume of the asset traded

# Calculate market impact
market_impact = calculate_market_impact(initial_price, final_price, trade_volume)
print(f"Market Impact: {market_impact}")

# Example data for slippage analysis
expected_price = 100.0  # Expected price of the asset
executed_price = 102.0  # Actual executed price

# Calculate slippage
slippage = calculate_slippage(expected_price, executed_price)
print(f"Slippage: {slippage}")
