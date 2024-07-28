import numpy as np

def calculate_beta(asset_returns, market_returns):
    covariance_matrix = np.cov(asset_returns, market_returns)
    covariance = covariance_matrix[0, 1]
    market_variance = covariance_matrix[1, 1]
    return covariance / market_variance
