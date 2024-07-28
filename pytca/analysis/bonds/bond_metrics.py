def calculate_duration(cash_flows, yield_to_maturity):
    return sum(cf / (1 + yield_to_maturity)**(t+1) for t, cf in enumerate(cash_flows))
