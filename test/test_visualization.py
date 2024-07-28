import pytest
from pytca.visualization.plotter import plot_candlestick
import pandas as pd

def test_plot_candlestick():
    data = pd.DataFrame({
        'Date': pd.date_range(start='2021-01-01', periods=5, freq='D'),
        'Close': [100, 102, 104, 103, 105]
    })
    fig = plot_candlestick(data)
    assert fig, "Plot should be generated"
