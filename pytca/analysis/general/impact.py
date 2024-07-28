def calculate_slippage(expected_price, actual_price):
    return actual_price - expected_price

def calculate_market_impact(initial_price, final_price, volume):
    return (final_price - initial_price) * volume
