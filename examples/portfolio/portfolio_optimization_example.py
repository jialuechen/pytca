from pytca.portfolio.optimization import optimize_portfolio

# Example data
expected_returns = [0.1, 0.2, 0.15]
cov_matrix = [[0.01, 0.0018, 0.0011],
              [0.0018, 0.04, 0.0023],
              [0.0011, 0.0023, 0.02]]

weights = optimize_portfolio(expected_returns, cov_matrix, 0.1)
print(f"Optimized Weights: {weights}")
