import numpy as np

def calculate_portfolio_variance(weights, cov_matrix):
    return np.dot(weights.T, np.dot(cov_matrix, weights))

def optimize_portfolio(returns, cov_matrix, risk_tolerance):
    num_assets = len(returns)
    weights = np.random.dirichlet(np.ones(num_assets), size=1)
    return weights
