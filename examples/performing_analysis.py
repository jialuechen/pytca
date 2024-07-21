import pytca

# Load data
stock_data = pytca.load_tick_data('path/to/stock_data.csv', data_type='stock')
forex_data = pytca.load_tick_data('path/to/forex_data.csv', data_type='forex')

# Analyze stock data
stock_analysis = pytca.analyze_stock_trade(stock_data, benchmark_data)
print("Stock Analysis Results:", stock_analysis)

# Analyze forex data
forex_analysis = pytca.analyze_forex_trade(forex_data, benchmark_data)
print("Forex Analysis Results:", forex_analysis)

# Calculate slippage
slippage = pytca.calculate_slippage(executed_price=100.05, benchmark_price=100.00)
print("Slippage:", slippage)

# Calculate VWAP
vwap = pytca.calculate_vwap(prices=[100.00, 100.05, 100.10], volumes=[1000, 2000, 1500])
print("VWAP:", vwap)