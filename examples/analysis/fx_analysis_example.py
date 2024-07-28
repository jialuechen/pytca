from pytca.analysis.fx.fx_metrics import calculate_fx_spread

# Example data
bid_prices = [1.105, 1.106, 1.107]
ask_prices = [1.110, 1.111, 1.112]

spreads = [calculate_fx_spread(bid, ask) for bid, ask in zip(bid_prices, ask_prices)]
print(f"Calculated FX Spreads: {spreads}")
