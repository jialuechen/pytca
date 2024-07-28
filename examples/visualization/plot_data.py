from pytca.visualization.plotter import plot_candlestick
import pandas as pd

# Example data
data = pd.DataFrame({
    'Date': pd.date_range(start='2021-01-01', periods=5, freq='D'),
    'Close': [100, 102, 104, 103, 105]
})

plot_candlestick(data)
