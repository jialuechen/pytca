import pytca

# Load data
tick_data = pytca.load_tick_data('path/to/tick_data.csv', data_type='stock')

# Create basic plot
basic_fig = pytca.plot_tick_data(tick_data, plot_type='basic')
basic_fig.savefig('basic_plot.png')

# Create candlestick chart
candlestick_fig = pytca.plot_tick_data(tick_data, plot_type='candlestick', interval='5min')
candlestick_fig.write_html('candlestick.html')

# Create order book depth chart
depth_fig = pytca.plot_tick_data(tick_data, plot_type='depth')
depth_fig.write_html('depth_chart.html')

# Create trade flow chart
trade_flow_fig = pytca.plot_tick_data(tick_data, plot_type='trade_flow', window='5min')
trade_flow_fig.write_html('trade_flow.html')