<div align=center>
<img src="assets/img/pytca-logo.png" width="40%" loc>
</div>

<div align=center>

# PyTCA: Python Library for Transaction Cost Analysis

</div>
<div align=center>

[![PyPI - Version](https://img.shields.io/pypi/v/pytca)](https://pypi.org/project/pytca/)
[![Python Versions](https://img.shields.io/badge/python-3.6%2B-green)](https://pypi.org/project/pytca/)
![PyPI downloads](https://img.shields.io/pypi/dm/pytca)
[![Documentation Status](https://readthedocs.org/projects/pytca/badge/?version=latest)](https://pytca.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/badge/License-BSD%202--Clause-orange.svg)](https://opensource.org/licenses/BSD-2-Clause)
[![Coverage Status](https://coveralls.io/repos/github/jialuechen/pytca/badge.svg?branch=main)](https://coveralls.io/github/jialuechen/pytca?branch=main)

</div>

PyTCA is a Python package for transaction cost analysis in financial markets, supporting both stock and forex data at the tick level.

## Features

- Load and process tick-level data for stocks and forex
- Perform various analyses including slippage, market impact, and timing cost
- Calculate key metrics such as VWAP and implementation shortfall
- Generate visualizations and reports
- RESTful API for integration with other systems
- Support for Excel and KDB data sources

## Installation

```bash
pip install pytca
```

## Quick Start

```python
import pytca

# Load tick data
tick_data = pytca.load_tick_data('path/to/tick_data.csv', data_type='stock')

# Analyze tick data
analysis_results = pytca.analyze_tick_data(tick_data)
print("Tick Data Analysis Results:", analysis_results)

# Visualize tick data
fig = pytca.plot_tick_data(tick_data, plot_type='summary')
fig.write_html('tick_data_summary.html')
```

## More Examples

### Loading Data from Different Sources

```python
import pytca

# Load data from CSV
csv_data = pytca.load_tick_data('path/to/tick_data.csv', data_type='stock')

# Load data from Excel
excel_data = pytca.read_excel('path/to/tick_data.xlsx', sheet_name='Tick Data')

# Load data from KDB
kdb_handler = pytca.KDBHandler(host='localhost', port=5000)
kdb_data = kdb_handler.load_tick_data('tickdata', '2023.07.15T09:30:00.000', '2023.07.15T16:00:00.000')
```

### Performing Analysis

```python
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
```

### Generating Visualizations

```python
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

# Create summary dashboard
summary_fig = pytca.plot_tick_data(tick_data, plot_type='summary')
summary_fig.write_html('summary_dashboard.html')
```

### Using the RESTful API

```python
import pytca

# Start the API server
pytca.run_api(host='localhost', port=5000)

# Now you can make HTTP requests to the API endpoints, for example:
# POST http://localhost:5000/analyze_tick_data
# with JSON body: {"table_name": "tickdata", "start_time": "2023.07.15T09:30:00.000", "end_time": "2023.07.15T16:00:00.000", "symbols": ["AAPL", "GOOGL"]}
```

## Documentation

For full documentation, please visit [Read the Docs](https://pytca.readthedocs.io/).

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for more details.

## License

This project is licensed under the BSD-2-Clause License - see the [LICENSE](LICENSE) file for details.
