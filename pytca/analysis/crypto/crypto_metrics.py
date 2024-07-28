import pandas as pd

def calculate_volatility(prices, window):
    return pd.Series(prices).rolling(window=window).std()
